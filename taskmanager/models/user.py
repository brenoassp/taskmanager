from db import db


class UserModel(db.Model):
    """User model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    tasks = db.relationship("TaskModel", back_populates="user", lazy="dynamic")

    def save_to_db(self):
        """Save the model to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete the model from the database."""
        db.session.delete(self)
        db.session.commit()
