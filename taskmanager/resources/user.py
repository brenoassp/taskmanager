from flask_jwt_extended import create_access_token, create_refresh_token
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256

from schemas import UserLoginSchema, UserSchema
from models.user import UserModel

blp = Blueprint("users", __name__)


@blp.route("/users")
class UserRegister(MethodView):
    """User registration."""

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """User registration func."""
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(400, message="A user with that username already exists.")
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(400, message="A user with that email already exists.")
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            email=user_data["email"],
        )

        try:
            user.save_to_db()
        except Exception:
            abort(500, message="An error occurred creating the user.")

        return user_data, 201


@blp.route("/users/<int:user_id>")
class User(MethodView):
    """User."""

    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get a user by id."""
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.response(204)
    def delete(self, user_id):
        """Delete a user by id."""
        user = UserModel.query.get_or_404(user_id)
        try:
            user.delete_from_db()
        except Exception:
            abort(500, message="An error occurred deleting the user.")
        return None, 204


@blp.route("/users/login")
class UserLogin(MethodView):
    """User login."""

    @blp.arguments(UserLoginSchema)
    @blp.response(200, UserLoginSchema)
    def post(self, user_data):
        """User login func."""
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if not user or not pbkdf2_sha256.verify(user_data["password"], user.password):
            abort(401, message="Invalid username or password.")

        access_token = create_access_token(
            identity=user.id, additional_claims={"username": user.username}
        )
        refresh_token = create_refresh_token(identity=user.id)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
