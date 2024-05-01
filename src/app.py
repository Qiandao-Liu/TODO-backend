from db import db, User, Recipe
from flask import Flask, json

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(body, code=200):
    return json.dumps(body), code

def failure_response(message, code=404):
    return json.dumps({'error': message}), code


@app.route("/")
def hello():
    return success_response("Hello World!")

@app.route("/users/")
def get_users():
    """
    Endpoint for getting all users
    """

    return success_response({"users": [u.serialize() for u in User.query.all()]})

@app.route("/users/<int:user_id>/")
def get_specific_user(user_id):
    """
    Endpoint for getting a specific user
    """

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("User not found")

    return success_response(user.serialize())

@app.route("/users/", methods=["POST"])
def create_user():
    pass

@app.route("/users/<int:user_id>/bookmark/", methods=["POST"])
def bookmark_recipe(user_id):
    pass

@app.route("/users/<int:user_id>/bookmark/", methods=["DELETE"])
def remove_bookmark(user_id):
    pass

@app.route("/recipes/")
def get_recipes():
    """
    Endpoint for getting all recipes
    """

    return success_response({"recipes": [r.serialize() for r in Recipe.query.all()]})

@app.route("/recipes/<int:recipe_id>/")
def get_specific_recipe(recipe_id):
    """
    Endpoint for getting a specific recipe
    """

    recipe = User.query.filter_by(id=recipe_id).first()

    if recipe is None:
        return failure_response("Recipe not found")

    return success_response(recipe.serialize())

@app.route("/recipes/", methods=["POST"])
def create_recipe():
    pass

@app.route("/recipes/<int:recipe_id>/", methods=["POST"])
def update_recipe(recipe_id):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
