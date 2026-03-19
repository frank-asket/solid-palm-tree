"""WhatsApp webhook: verify (GET) and handle incoming messages (POST)."""
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.core.config import VERIFY_TOKEN
from app.core.deps import get_db
from app.services import (
    compute_insights,
    create_transaction,
    extract_transaction_from_message,
    format_insights_reply,
    get_or_create_user_by_phone,
    get_transactions_for_user,
)
from app.utils.whatsapp import send_text_message

router = APIRouter(prefix="/webhook", tags=["whatsapp"])


@router.get("")
async def verify_webhook(
    mode: str | None = Query(None, alias="hub.mode"),
    token: str | None = Query(None, alias="hub.verify_token"),
    challenge: str | None = Query(None, alias="hub.challenge"),
):
    """Meta uses GET to verify the webhook URL. Return hub.challenge if token matches."""
    if mode == "subscribe" and token == VERIFY_TOKEN and challenge is not None:
        return PlainTextResponse(content=challenge)
    return PlainTextResponse(content="Forbidden", status_code=403)


@router.post("")
async def handle_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle incoming WhatsApp messages: extract transaction, save, reply with insight."""
    body = await request.json()

    # Only process message events (ignore status, etc.)
    try:
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    # Sender wa_id is usually in msg["from"], but guard against missing payload fields.
                    from_id = msg.get("from")
                    if not from_id:
                        contacts = value.get("contacts") or []
                        from_id = contacts[0].get("wa_id") if contacts else None
                    if not from_id:
                        continue
                    if msg.get("type") != "text":
                        send_text_message(from_id, "Please send a text message (e.g. 'I spent 50 on food' or 'Got 200 from salary').")
                        continue
                    text = (msg.get("text") or {}).get("body", "").strip()
                    if not text:
                        continue

                    # Resolve user by phone (WhatsApp ID is phone without +)
                    user = get_or_create_user_by_phone(db, from_id)

                    # Extract transaction
                    extracted = extract_transaction_from_message(text)
                    if extracted:
                        create_transaction(
                            db,
                            user_id=user.id,
                            type_=extracted["type"],
                            amount=extracted["amount"],
                            category=extracted.get("category"),
                            note=extracted.get("note"),
                        )
                        transactions = get_transactions_for_user(db, user.id)
                        insights = compute_insights(list(transactions))
                        reply = format_insights_reply(insights)
                    else:
                        # Greeting or non-transaction
                        if any(w in text.lower() for w in ("hi", "hello", "hey", "summary", "insight", "stats")):
                            transactions = get_transactions_for_user(db, user.id)
                            insights = compute_insights(list(transactions))
                            reply = format_insights_reply(insights)
                        else:
                            reply = "Send an expense or income in words, e.g. 'I spent 50 on food' or 'Got 200 from salary'. Say 'summary' for your stats."
                    send_text_message(from_id, reply)
    except Exception:
        pass  # Avoid 5xx to prevent Meta retries; log in production
    return {"ok": True}
