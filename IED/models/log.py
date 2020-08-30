from IED.models.base import Base

from IED.extensions import db


class Log(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(50))
    url = db.Column(db.String(255))