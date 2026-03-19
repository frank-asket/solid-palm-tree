"""Compute financial insights from user transactions."""
from collections import defaultdict
from typing import Any

from app.models.transaction import Transaction


def compute_insights(transactions: list[Transaction]) -> dict[str, Any]:
    """Total income vs expenses, category breakdown, savings, health message."""
    total_income = 0.0
    total_expense = 0.0
    by_category: dict[str, float] = defaultdict(float)

    for t in transactions:
        if t.type == "income":
            total_income += t.amount
        else:
            total_expense += t.amount
            cat = t.category or "other"
            by_category[cat] += t.amount

    savings = total_income - total_expense
    if total_income > 0:
        savings_rate = round(100 * savings / total_income, 1)
    else:
        savings_rate = 0.0

    # Simple health message
    if total_income == 0 and total_expense == 0:
        health = "Add income and expenses to see your financial picture."
    elif savings < 0:
        health = "⚠️ You are spending more than you earn. Try to reduce expenses or increase income."
    elif savings_rate >= 20:
        health = "✅ You're saving well. Keep it up!"
    elif savings_rate > 0:
        health = "✅ You're saving a bit. Consider increasing savings when possible."
    else:
        health = "⚠️ You are spending more than you earn."

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "savings": round(savings, 2),
        "savings_rate_percent": savings_rate,
        "by_category": dict(sorted(by_category.items(), key=lambda x: -x[1])),
        "health": health,
    }


def format_insights_reply(insights: dict[str, Any]) -> str:
    """Turn insights dict into a short WhatsApp-friendly message."""
    lines = [
        f"📊 *Summary*",
        f"Income: {insights['total_income']}",
        f"Expenses: {insights['total_expense']}",
        f"Savings: {insights['savings']} ({insights['savings_rate_percent']}%)",
        "",
        insights["health"],
    ]
    if insights.get("by_category"):
        lines.append("")
        lines.append("By category:")
        for cat, amount in list(insights["by_category"].items())[:8]:
            lines.append(f"  • {cat}: {amount}")
    return "\n".join(lines)
