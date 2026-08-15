"""Create the single Manga Gallery administrator from environment variables."""
import os
from werkzeug.security import generate_password_hash
from main import app
from database import db
from models.user import User
from models.role import Role

with app.app_context():
    role = Role.query.filter_by(name="admin").first()
    if not role:
        role = Role(name="admin", description="Administrateur unique de Manga Gallery", permissions={"manage_mangas": True, "manage_users": True, "manage_settings": True, "manage_roles": True, "manage_reports": True, "manage_notifications": True}, is_system=True, is_active=True)
        db.session.add(role); db.session.flush()
    else:
        role.permissions = {"manage_mangas": True, "manage_users": True, "manage_settings": True, "manage_roles": True, "manage_reports": True, "manage_notifications": True}
        role.is_system = True; role.is_active = True
    username = os.getenv("ADMIN_USERNAME", "Exauce")
    email = os.getenv("ADMIN_EMAIL", "")
    password = os.getenv("ADMIN_PASSWORD", "")
    telegram_id = os.getenv("ADMIN_TELEGRAM_ID", "")
    if not password:
        raise SystemExit("ADMIN_PASSWORD est obligatoire")
    try: telegram_id = int(telegram_id) if telegram_id else None
    except ValueError: raise SystemExit("ADMIN_TELEGRAM_ID doit être numérique")
    user = User.query.filter((User.username == username) | ((User.email == email) & (User.email.isnot(None)))).first()
    if not user:
        user = User(username=username, email=email or None, telegram_id=telegram_id)
        db.session.add(user)
    user.first_name = user.first_name or username
    user.password_hash = generate_password_hash(password)
    user.role = "admin"; user.role_id = role.id; user.status = "active"; user.is_verified = True
    # Enforce the one-admin rule at bootstrap time.
    for other in User.query.filter(User.id != user.id, User.role == "admin").all():
        other.role = "user"; other.role_id = None
    db.session.commit()
    print(f"ADMIN READY: id={user.id}, username={user.username}")
