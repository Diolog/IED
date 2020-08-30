from werkzeug.security import generate_password_hash, check_password_hash

from IED.extensions import db
from IED.models.base import Base
from IED.utils.PKGenrate import generate_user_key


class User(Base):
    id = db.Column(db.String(25), primary_key=True, default=generate_user_key)
    username = db.Column(db.String(25))
    password_hash =db.Column(db.String(255))
    is_manager = db.Column(db.Integer) # 0 不是管理员 1 是管理员

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)