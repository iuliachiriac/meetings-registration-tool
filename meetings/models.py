from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Meeting(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    acronym = db.Column(db.String(16), nullable=False)
    type_id = db.Column(db.String(32), db.ForeignKey('type.slug'),
                        nullable=False)
    type = db.relationship('MeetingType',
                           backref=db.backref('meetings', lazy='dynamic'))
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    venue_address = db.Column(db.String(128))
    venue_city = db.Column(db.String(32), nullable=False)
    venue_country = db.Column(db.String(32), nullable=False)
    admin_name = db.Column(db.String(32))
    admin_email = db.Column(db.String(32))
    media_admin_name = db.Column(db.String(32))
    media_admin_email = db.Column(db.String(32))
    online_registration = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '{}'.format(self.title)


class MeetingType(db.Model):

    slug = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
