from werkzeug.security import generate_password_hash, check_password_hash
from ..app import db
from sqlalchemy.orm import validates
import re

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username cannot be empty')
        if len(username) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if not re.match('^[A-Za-z0-9_-]*$', username):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return username

    def set_password(self, password):
        if not password:
            raise ValueError('Password cannot be empty')
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 