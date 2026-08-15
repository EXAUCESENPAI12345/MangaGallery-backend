import os
import json
from urllib import request

token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
backend = os.getenv("PUBLIC_BACKEND_URL", "").strip().rstrip("/")
secret = os.getenv("TELEGRAM_WEBHOOK_SECRET", "").strip()

if not token or not backend or not secret:
    raise SystemExit("TELEGRAM_BOT_TOKEN, PUBLIC_BACKEND_URL et TELEGRAM_WEBHOOK_SECRET sont requis.")

url = f"https://api.telegram.org/bot{token}/setWebhook"
payload = {
    "url": backend + "/api/telegram/webhook",
    "secret_token": secret,
    "allowed_updates": ["message"],
    "drop_pending_updates": False,
}
req = request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with request.urlopen(req, timeout=15) as r:
    print(r.read().decode())
