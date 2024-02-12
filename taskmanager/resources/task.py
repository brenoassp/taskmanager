from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from schemas import ListTasksSchema, TaskSchema, TaskUpdateSchema
from models.task import TaskModel

blp = Blueprint("tasks", __name__)


@blp.route("/tasks/<int:task_id>")
class Task(MethodView):
    """Routes to Read, Update and Delete a task."""

    @jwt_required()
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        """Get a task by id."""
        task = TaskModel.query.get_or_404(task_id)
        request_user_id = get_jwt_identity()
        if task.user_id != request_user_id:
            abort(403, message="You are not allowed to access this task.")
        return task

    @jwt_required()
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200)
    def put(self, task_data, task_id):
        """Update a task by id."""
        task = TaskModel.query.get_or_404(task_id)
        request_user_id = get_jwt_identity()
        if task.user_id != request_user_id:
            abort(403, message="You are not allowed to access this task.")
        task.name = task_data.get("name", task.name)
        task.done = task_data.get("done", task.done)
        task.save_to_db()
        return {
            "id": task.id,
            "name": task.name,
            "done": task.done,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }, 200

    @jwt_required()
    @blp.response(204)
    def delete(self, task_id):
        """Delete a task by id."""
        task = TaskModel.query.get_or_404(task_id)
        request_user_id = get_jwt_identity()
        if task.user_id != request_user_id:
            abort(403, message="You are not allowed to access this task.")
        try:
            task.delete_from_db()
        except Exception:
            abort(500, message="An error occurred deleting the task.")
        return None, 204


@blp.route("/tasks")
class TaskCreation(MethodView):
    """Route to create a task."""

    @jwt_required()
    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        """Create a task."""
        author_id = get_jwt_identity()
        task = TaskModel(
            name=task_data["name"],
            user_id=author_id,
        )
        try:
            task.save_to_db()
        except Exception:
            abort(500, message="An error occurred creating the task.")

        return {
            "id": task.id,
            "name": task.name,
            "done": task.done,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }, 201


@blp.route("/tasks")
class TaskList(MethodView):
    """Route to get all tasks."""

    @jwt_required()
    @blp.response(200, ListTasksSchema)
    def get(self):
        """Get all tasks."""
        author_id = get_jwt_identity()
        tasks = TaskModel.query.filter(TaskModel.user_id == author_id).all()
        return {"data": tasks}
