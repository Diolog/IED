from datetime import datetime

from IED.extensions import db


class Base(db.Model):
    __abstract__ = True
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_delete = db.Column(db.Integer, default=1) # 1 正常， 0 已删除
