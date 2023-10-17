import flask
from flask import Response, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Session, User, Advertisement
from schema import CreateUser, PatchUser, CreateAdvertisement, PatchAdvertisement

app = flask.Flask("app")
bcrypt = Bcrypt(app)


def hash_password(password: str):
    password = password.encode()
    return bcrypt.generate_password_hash(password).decode()


def check_password(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(password, hashed_password)


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


def validate(model, data):
    try:
        return model.model_validate(data).model_dump(exclude_unset=True)
    except ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response


def get_user(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, "user already exists")
    return user


def add_advertisement(advertisement: Advertisement):
    try:
        request.session.add(advertisement)
        request.session.commit()
    except IntegrityError as err:
        # print(err)
        raise HttpError(409, "user does not exist")
    return advertisement


def get_advertisement(ad_id: int):
    advertisement = request.session.get(Advertisement, ad_id)
    if advertisement is None:
        raise HttpError(404, "advertisement not found")
    # print(advertisement.description)
    return advertisement


class UserView(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, user_id: int):
        user = get_user(user_id)
        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "registration_time": user.registration_time.isoformat(),
            }
        )

    def post(self):
        user_data = validate(CreateUser, request.json)
        user_data["password"] = hash_password(user_data["password"])
        new_user = User(**user_data)
        new_user = add_user(new_user)
        return jsonify({"id": new_user.id})

    def patch(self, user_id: int):
        user_data = validate(PatchUser, request.json)
        if "password" in user_data:
            user_data["password"] = hash_password(user_data["password"])
        user = get_user(user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        user = add_user(user)
        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "registration_time": user.registration_time.isoformat(),
            }
        )

    def delete(self, user_id: int):
        user = get_user(user_id)
        self.session.delete(user)
        self.session.commit()
        return jsonify({"status": "ok"})


class AdView(MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, ad_id: int):
        advertisement = get_advertisement(ad_id)
        return jsonify(
            {
                "id": advertisement.id,
                "heading": advertisement.heading,
                "description": advertisement.description,
                "date_creation": advertisement.date_creation.isoformat(),
            }
        )

    def post(self):
        advertisement_data = validate(CreateAdvertisement, request.json)
        new_advertisement = Advertisement(**advertisement_data)
        add_advertisement(new_advertisement)
        return jsonify({"id": new_advertisement.id})

    def patch(self, ad_id: int):
        advertisement_data = validate(PatchAdvertisement, request.json)
        advertisement = get_advertisement(ad_id)
        for key, value in advertisement_data.items():
            setattr(advertisement, key, value)
        user = add_advertisement(advertisement)
        return jsonify(
            {
                "id": advertisement.id,
                "heading": advertisement.heading,
                "description": advertisement.description,
                "date_creation": advertisement.date_creation.isoformat(),
            }
        )

    def delete(self, ad_id: int):
        advertisement = get_advertisement(ad_id)
        self.session.delete(advertisement)
        self.session.commit()
        return jsonify({"status": "ok"})


user_view = UserView.as_view("user_view")
ad_view = AdView.as_view("ad_view")


app.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/user", view_func=user_view, methods=["POST"])

app.add_url_rule(
    "/advertisement/<int:ad_id>", view_func=ad_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/advertisement", view_func=ad_view, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
