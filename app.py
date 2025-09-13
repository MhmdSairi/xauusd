import os
import json
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("signal-bot")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # e.g., @YourChannel or -1001234567890
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" if TELEGRAM_TOKEN else None

def format_signal(payload: dict) -> str:
    symbol = payload.get("symbol", "UNKNOWN")
    side = str(payload.get("side", "")).upper()
    price = payload.get("price")
    sl = payload.get("sl")
    tp = payload.get("tp")
    tf = payload.get("timeframe") or payload.get("tf") or ""
    note = payload.get("note") or payload.get("comment") or ""

    lines = [
        "📣 *TRADING SIGNAL*",
        f"• Pair: *{symbol}*",
        f"• Arah: *{side}*",
    ]
    if price is not None:
        lines.append(f"• Entry: *{price}*")
    if sl is not None:
        lines.append(f"• SL: *{sl}*")
    if tp is not None:
        lines.append(f"• TP: *{tp}*")
    if tf:
        lines.append(f"• TF: *{tf}*")
    if note:
        lines.append(f"• Catatan: {note}")
    lines.append("—")
    lines.append("_Auto-post by Bot_")
    return "\n".join(lines)

@app.get("/")
def health():
    return "OK", 200

@app.post("/tv-webhook")
def tv_webhook():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return jsonify({"ok": False, "error": "Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID env"}), 500

    try:
        data = request.get_json(force=True, silent=False)
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object")
    except Exception as e:
        logger.exception("Invalid JSON payload")
        return jsonify({"ok": False, "error": f"Invalid JSON: {e}"}), 400

    message = format_signal(data)
    try:
        resp = requests.post(TELEGRAM_API_URL, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=15)
        if resp.status_code != 200:
            logger.error("Telegram error: %s", resp.text)
            return jsonify({"ok": False, "tg_error": resp.text}), 502
        return jsonify({"ok": True}), 200
    except Exception as e:
        logger.exception("Failed sending to Telegram")
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
