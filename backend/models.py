from database import db
from datetime import datetime


class AuthorizedUser(db.Model):

    __tablename__ = 'authorized_users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    rfid_tag = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )


class SmartBin(db.Model):

    __tablename__ = 'smart_bins'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    location = db.Column(
        db.String(100)
    )

    current_level = db.Column(
        db.Integer
    )

    status = db.Column(
        db.String(50)
    )

    last_collection = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class EventLog(db.Model):

    __tablename__ = 'event_logs'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    bin_id = db.Column(
        db.Integer,
        db.ForeignKey('smart_bins.id')
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('authorized_users.id'),
        nullable=True
    )

    event_type = db.Column(
        db.String(100)
    )

    level = db.Column(
        db.Integer
    )

    message = db.Column(
        db.String(255)
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )