from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from database import db

class AuthService:
    def get_by_telegram_id(self, telegram_id): return User.query.filter_by(telegram_id=telegram_id).first()
    def get_by_username(self, username): return User.query.filter_by(username=username).first()
    def telegram_exists(self, telegram_id): return self.get_by_telegram_id(telegram_id) is not None
    def username_exists(self, username): return self.get_by_username(username) is not None
    def validate_username(self, username):
        username=str(username or '').strip()
        return 3 <= len(username) <= 100
    def validate_password(self, password): return bool(password) and len(str(password)) >= 8
    def create_account(self, telegram_id, username, password, first_name=None, last_name=None, photo_url=None, email=None):
        if telegram_id is not None and self.telegram_exists(telegram_id): return None
        if username and self.username_exists(username): return None
        if not self.validate_username(username) or not self.validate_password(password): return None
        user=User(telegram_id=telegram_id,username=username.strip(),first_name=first_name,last_name=last_name,photo_url=photo_url,email=email,password_hash=generate_password_hash(password),role='user',status='active',is_verified=True)
        db.session.add(user);db.session.commit();return user
    def authenticate(self, username, password):
        user=self.get_by_username(username)
        if not user or user.status!='active' or not user.password_hash or not check_password_hash(user.password_hash,password): return None
        user.last_login=datetime.utcnow();db.session.commit();return user
    def update_profile_photo(self,user,photo_url): user.photo_url=photo_url;db.session.commit();return user
    def update_username(self,user,username):
        if not self.validate_username(username) or (self.username_exists(username) and user.username!=username): return None
        user.username=username.strip();user.updated_at=datetime.utcnow();db.session.commit();return user
    def save(self): db.session.commit()
