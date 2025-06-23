from ..app import db
from sqlalchemy.orm import validates
from datetime import date

class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan', lazy=True)

    @validates('date')
    def validate_date(self, key, value):
        if isinstance(value, str):
            try:
                year, month, day = map(int, value.split('-'))
                value = date(year, month, day)
            except (ValueError, TypeError):
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        if value < date(2000, 1, 1):
            raise ValueError('Date cannot be before year 2000')
        return value

    @validates('number')
    def validate_number(self, key, value):
        try:
            episode_number = int(value)
            if episode_number < 1:
                raise ValueError('Episode number must be positive')
            return episode_number
        except (ValueError, TypeError):
            raise ValueError('Episode number must be a valid integer') 