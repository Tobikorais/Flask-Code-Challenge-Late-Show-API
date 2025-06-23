from ..app import db
from sqlalchemy.orm import validates

class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    occupation = db.Column(db.String(120), nullable=False)

    @validates('name', 'occupation')
    def validate_fields(self, key, value):
        if not value or not value.strip():
            raise ValueError(f'{key} cannot be empty')
        if len(value) > 120:
            raise ValueError(f'{key} must be less than 120 characters')
        return value.strip() 