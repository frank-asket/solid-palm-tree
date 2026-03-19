"""WhatsApp Cloud API: send text messages."""
import httpx

from app.core.config import PHONE_NUMBER_ID, WHATSAPP_TOKEN

GRAPH_URL = "https://graph.facebook.com/v21.0"


def send_text_message(to_wa_id: str | None, text: str) -> bool:
    """Send a text message to a WhatsApp user. Returns True on success."""
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        return False
    if not to_wa_id:
        return False
    url = f"{GRAPH_URL}/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to_wa_id.replace("+", "").replace(" ", ""),
        "type": "text",
        "text": {"body": text[:4096]},
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.post(url, json=payload, headers=headers)
            return r.status_code == 200
    except Exception:
        return False
