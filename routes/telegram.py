from flask import Blueprint, request, jsonify
from config import Config
from services.telegram_service import handle_update, _telegram_call
from utils.authz import require_admin

telegram_bp = Blueprint("telegram", __name__)


@telegram_bp.post("/webhook")
def telegram_webhook():
    secret = Config.TELEGRAM_WEBHOOK_SECRET

    if secret:
        received = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if received != secret:
            return jsonify(success=False, message="Unauthorized"), 401

    update = request.get_json(silent=True)
    if not isinstance(update, dict):
        return jsonify(success=False, message="Invalid Telegram update"), 400

    try:
        handle_update(update)
    except Exception:
        # Never expose Telegram/API/database details to Telegram.
        from flask import current_app
        current_app.logger.exception("Telegram webhook processing failed")
        return jsonify(success=False, message="Webhook processing failed"), 500

    return jsonify(success=True), 200


@telegram_bp.get("/status")
def telegram_status():
    return jsonify(
        success=True,
        service="Telegram Bot",
        configured=bool(Config.TELEGRAM_BOT_TOKEN),
        bot_username=Config.TELEGRAM_BOT_USERNAME or None,
        mini_app_configured=bool(Config.TELEGRAM_MINI_APP_URL),
        webhook_configured=bool(
            Config.PUBLIC_BACKEND_URL and Config.TELEGRAM_WEBHOOK_SECRET
        ),
    ), 200


@telegram_bp.post("/set-webhook")
@require_admin
def set_webhook():
    if not Config.TELEGRAM_BOT_TOKEN:
        return jsonify(success=False, message="TELEGRAM_BOT_TOKEN manquant"), 400
    if not Config.PUBLIC_BACKEND_URL:
        return jsonify(success=False, message="PUBLIC_BACKEND_URL manquant"), 400
    if not Config.TELEGRAM_WEBHOOK_SECRET:
        return jsonify(success=False, message="TELEGRAM_WEBHOOK_SECRET manquant"), 400

    webhook_url = Config.PUBLIC_BACKEND_URL.rstrip("/") + "/api/telegram/webhook"

    result = _telegram_call(
        "setWebhook",
        {
            "url": webhook_url,
            "secret_token": Config.TELEGRAM_WEBHOOK_SECRET,
            "allowed_updates": ["message"],
            "drop_pending_updates": False,
        },
    )

    return jsonify(
        success=True,
        message="Webhook Telegram configuré",
        webhook_url=webhook_url,
        telegram=result,
    ), 200
