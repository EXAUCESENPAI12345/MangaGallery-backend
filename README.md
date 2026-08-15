# Manga Gallery Backend

Flask + PostgreSQL + SQLAlchemy + JWT API.

## Local

1. Create a PostgreSQL database.
2. Copy `.env.example` to `.env` and fill the values.
3. Install dependencies: `pip install -r requirements.txt`.
4. Set `AUTO_CREATE_TABLES=true` only for first-time initialization, or run `flask --app main init-db`.
5. Start: `python main.py`.

## Production

Use `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 main:app`.

Required environment variables: `SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`.
Telegram credentials must remain environment variables and must never be committed.

## Single administrator

The application reserves the `admin` role for the owner account. Set `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` and optionally `ADMIN_TELEGRAM_ID`, then run:

`python scripts/bootstrap_admin.py`

The bootstrap script demotes any other account carrying the `admin` role, leaving one administrator.

## Health

`GET /health` checks the Flask process and PostgreSQL connection.


## Telegram Bot

The backend exposes a Telegram webhook at:

`POST /api/telegram/webhook`

Set these environment variables in production:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_BOT_USERNAME`
- `TELEGRAM_MINI_APP_URL` (must be HTTPS)
- `PUBLIC_BACKEND_URL` (the public Render URL)
- `TELEGRAM_WEBHOOK_SECRET`

After deployment, configure the webhook with:

`python scripts/set_telegram_webhook.py`

The `/start` command automatically creates or updates the Telegram user and sends an **Ouvrir Manga Gallery** Mini App button. `/help` sends the bot help message.

Never commit a real Telegram bot token.
