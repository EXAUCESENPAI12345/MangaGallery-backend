"""
Manga Gallery - Telegram Bot service.

Uses the Telegram Bot HTTP API directly so the backend does not need
python-telegram-bot and remains compatible with Gunicorn/Render.
"""

import json
import secrets
from urllib import request, error

from flask import current_app

from config import Config
from database import db
from models.user import User


def _telegram_call(method, payload):
    token = Config.TELEGRAM_BOT_TOKEN
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")

    url = f"https://api.telegram.org/bot{token}/{method}"
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (error.URLError, TimeoutError) as exc:
        current_app.logger.exception("Telegram API request failed")
        raise RuntimeError("Telegram API unavailable") from exc

    if not data.get("ok"):
        raise RuntimeError(data.get("description", "Telegram API error"))
    return data.get("result")


def _bot_username():
    return Config.TELEGRAM_BOT_USERNAME.strip().lstrip("@")


def ensure_telegram_user(telegram_user):
    telegram_id = telegram_user.get("id")
    if not telegram_id:
        raise ValueError("Telegram user id is required")

    user = User.query.filter_by(telegram_id=int(telegram_id)).first()
    created = False

    username = telegram_user.get("username")
    first_name = telegram_user.get("first_name")
    last_name = telegram_user.get("last_name")

    if not user:
        base_username = username or f"tg_{telegram_id}"
        candidate = base_username[:100]
        if User.query.filter_by(username=candidate).first():
            candidate = f"tg_{telegram_id}"[:100]

        user = User(
            telegram_id=int(telegram_id),
            username=candidate,
            first_name=first_name,
            last_name=last_name,
            photo_url=None,
            role="user",
            role_id=None,
            status="active",
            is_verified=True,
        )
        db.session.add(user)
        db.session.commit()
        created = True
    else:
        changed = False
        if username and user.username != username:
            # Username is not unique in the current schema, so update safely.
            user.username = username[:100]
            changed = True
        if user.first_name != first_name:
            user.first_name = first_name
            changed = True
        if user.last_name != last_name:
            user.last_name = last_name
            changed = True
        if changed:
            db.session.commit()

    return user, created


def build_start_message(user, created=False):
    name = user.first_name or user.username or "ami"
    if created:
        intro = f"Bienvenue {name} sur Manga Gallery !"
        body = (
            "Ton compte Manga Gallery vient d'être créé automatiquement "
            "à partir de ton compte Telegram."
        )
    else:
        intro = f"Bon retour {name} !"
        body = "Ton compte Manga Gallery est prêt."

    return (
        f"<b>{intro}</b>\n\n"
        f"{body}\n\n"
        "Ouvre la Mini App pour découvrir tes mangas et chapitres."
    )


def send_start(user, created=False):
    text = build_start_message(user, created=created)
    reply_markup = None

    if Config.TELEGRAM_MINI_APP_URL:
        reply_markup = {
            "inline_keyboard": [[
                {
                    "text": "Ouvrir Manga Gallery",
                    "web_app": {"url": Config.TELEGRAM_MINI_APP_URL},
                }
            ]]
        }

    payload = {
        "chat_id": user.telegram_id,
        "text": text,
        "parse_mode": "HTML",
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    return _telegram_call("sendMessage", payload)


def send_help(telegram_id):
    return _telegram_call(
        "sendMessage",
        {
            "chat_id": telegram_id,
            "text": (
                "<b>Manga Gallery — Aide</b>\n\n"
                "/start — ouvrir Manga Gallery et créer ton compte si nécessaire\n"
                "/help — afficher cette aide\n\n"
                "Tu peux ensuite utiliser la Mini App pour consulter les mangas "
                "et les chapitres."
            ),
            "parse_mode": "HTML",
        },
    )


def handle_update(update):
    if not isinstance(update, dict):
        return

    message = update.get("message") or {}
    telegram_user = message.get("from") or {}
    text = (message.get("text") or "").strip()

    if not telegram_user.get("id"):
        return

    user, created = ensure_telegram_user(telegram_user)

    if text.startswith("/start"):
        send_start(user, created=created)
    elif text.startswith("/help"):
        send_help(user.telegram_id)


def generate_webhook_secret():
    return secrets.token_urlsafe(32)[:64]
