from typing import Optional
from pydantic import BaseModel, Extra
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    
    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        return check_password_hash(self.password, secret)
    
    @classmethod
    def init(cls):
        if User.query.filter_by(username="admin").first() is None:
            user = User(username='admin')
            user.set_password('admin')
            db.session.add(user)
            db.session.commit()


class UserSchema(BaseModel, extra=Extra.forbid):
    id: Optional[int]
    username: str
    password: str
    
class UserChangePasswordSchema(BaseModel, extra=Extra.forbid):
    password: str
    new_password: str
