from db import db


class TaskModel(db.Model):
    """Task model."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    done = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel", back_populates="tasks")

    def __init__(self, name, user_id, done=False):
        self.name = name
        self.done = done
        self.user_id = user_id
        self.created_at = db.func.now()
        self.updated_at = db.func.now()

    def save_to_db(self):
        """Save the model to the database."""
        self.updated_at = db.func.now()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete the model from the database."""
        db.session.delete(self)
        db.session.commit()
