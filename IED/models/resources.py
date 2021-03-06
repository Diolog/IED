from IED.extensions import db
from IED.models.base import Base
from IED.utils.PKGenrate import generate_resource_key


class ResourceClass(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    level = db.Column(db.Integer)
    parentId = db.Column(db.Integer)


class Resource(Base):
    id = db.Column(db.String(25), primary_key=True, default=generate_resource_key)
    name = db.Column(db.String(255))
    real_url = db.Column(db.String(255), nullable=False)
    resource_url = db.Column(db.String(255), nullable=False)
    class_id = db.Column(db.Integer, nullable=False)
    file_md5 = db.Column(db.String(35), nullable=False, unique=True)
    description = db.Column(db.String(255), default='')
    size = db.Column(db.Float, nullable=False)