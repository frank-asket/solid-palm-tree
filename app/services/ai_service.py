"""AI extraction: parse natural language into structured transaction data."""
import json
import re
from typing import Any

from openai import OpenAI

from app.core.config import OPENAI_API_KEY

EXTRACTION_PROMPT = """You extract financial transaction data from short user messages.
Return ONLY valid JSON, no other text. Use this exact schema:
{"type": "income" or "expense", "amount": number, "category": "string or null", "note": "string or null"}

If the message is not about a transaction (e.g. greeting, question, unclear), return: {"type": null, "amount": null, "category": null, "note": null}

Examples:
"I spent 50 on food" -> {"type": "expense", "amount": 50, "category": "food", "note": null}
"Got 200 from salary" -> {"type": "income", "amount": 200, "category": "salary", "note": null}
"Hello" -> {"type": null, "amount": null, "category": null, "note": null}

User message: """


def extract_transaction_from_message(message: str) -> dict[str, Any] | None:
    """Call OpenAI to extract type, amount, category, note. Returns None on failure or non-transaction."""
    if not OPENAI_API_KEY:
        return _fallback_extract(message)

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": EXTRACTION_PROMPT + message}],
            temperature=0,
        )
        text = (response.choices[0].message.content or "").strip()
        # Allow JSON inside markdown code blocks
        if "```" in text:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
            if match:
                text = match.group(1).strip()
        data = json.loads(text)
        if data.get("type") is None or data.get("amount") is None:
            return None
        if data["type"] not in ("income", "expense"):
            return None
        amount = float(data["amount"])
        if amount <= 0:
            return None
        return {
            "type": data["type"],
            "amount": amount,
            "category": data.get("category") or None,
            "note": data.get("note") or None,
        }
    except Exception:
        return _fallback_extract(message)


def _fallback_extract(message: str) -> dict[str, Any] | None:
    """Simple regex fallback when API is unavailable."""
    message_lower = message.lower().strip()
    # "spent X on Y", "paid X", "X for Y"
    expense = re.search(r"(?:spent|paid|\-)\s*(\d+(?:\.\d+)?)\s*(?:on|for)?\s*(\w+)?", message_lower)
    if expense:
        return {
            "type": "expense",
            "amount": float(expense.group(1)),
            "category": (expense.group(2) or "other").lower() if expense.group(2) else None,
            "note": None,
        }
    # "got X", "received X", "+ X"
    income = re.search(r"(?:got|received|\+)\s*(\d+(?:\.\d+)?)\s*(?:from)?\s*(\w+)?", message_lower)
    if income:
        return {
            "type": "income",
            "amount": float(income.group(1)),
            "category": (income.group(2) or "other").lower() if income.group(2) else None,
            "note": None,
        }
    return None
