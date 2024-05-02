from db import db, User, Recipe
from flask import Flask, request
import json

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
    """
    Endpoint for creating a user
    """
    
    body = json.loads(request.data)
    if body.get('username') is None:
        return failure_response("Bad Request - Username is required", 400)
    new_user = User(
        username=body.get('username')
    )
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user
    """

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return failure_response("User not found")

    db.session.delete(user)
    db.session.commit()

    return success_response(user.serialize())

@app.route("/users/<int:user_id>/bookmark/<int:recipe_id>/", methods=["POST"])
def bookmark_recipe(user_id, recipe_id):
    """
    Endpoint for bookmarking a recipe
    """
    
    user = User.query.filter_by(id=user_id).first()
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if user is None:
        return failure_response("User not Found", 404)
    elif recipe is None:
        return failure_response("Recipe Not Found", 404)
    user.bookmarked_recipes.append(recipe)
    recipe.bookmarkers.append(user)
    db.session.commit()
    return success_response(user.serialize())

@app.route("/users/<int:user_id>/bookmark/<int:recipe_id>/", methods=["DELETE"])
def remove_bookmark(user_id, recipe_id):
    """
    Endpoint for unbookmarking a recipe
    """
    
    user = User.query.filter_by(id=user_id).first()
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if user is None:
        return failure_response("User not Found", 404)
    elif recipe is None:
        return failure_response("Recipe not Found", 404)
    elif recipe not in user.bookmarked_recipes:
        return failure_response("Bookmark not Found", 404)
    user.bookmarked_recipes.remove(recipe)
    db.session.commit()
    return success_response(user.serialize())


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
    recipe = Recipe.query.filter_by(id=recipe_id).first()

    if recipe is None:
        return failure_response("Recipe not found")

    return success_response(recipe.serialize())


@app.route("/users/<int:user_id>/recipes/", methods=["POST"])
def create_recipe(user_id):
    """
    Endpoint for creating a recipe
    """
    
    body = json.loads(request.data)
    if (body.get("title") is None or body.get("ingredients") is None or body.get("directions") is None
            or body.get("difficulty") is None or (isinstance(body.get("difficulty"), int) and (body.get("difficulty") > 3 or body.get("difficulty") < 0))):
        return failure_response("Bad Request - Title, Ingredients, Directions, and Difficulty are required", 400)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not Found", 404)
    new_recipe = Recipe(
        title=body.get("title"),
        ingredients=body.get("ingredients"),
        directions=body.get("directions"),
        publisher_id=user_id,
        image=body.get("image"),
        description=body.get("description"),
        difficulty=body.get("difficulty")
    )
    for k in body.keys():
        if not hasattr(new_recipe, k):
            return failure_response("Bad Request - Recipe has no property " + k, 400)
    db.session.add(new_recipe)
    db.session.commit()
    return success_response(new_recipe.serialize(), 201)


@app.route("/recipes/<int:recipe_id>/", methods=["POST"])
def update_recipe(recipe_id):
    """
    Endpoint for modifying a recipe
    """
    
    body = json.loads(request.data)
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if all(value is None for value in body.values()):
        return failure_response("Bad Request - Body should not be empty", 400)
    for k in body.keys():
        if not hasattr(recipe, k):
            return failure_response("Bad Request - Recipe has no property " + k, 400)
    for k in body.keys():
        v = body.get(k)
        if v is None:
            continue
        setattr(recipe, k, v)
    db.session.commit()
    return success_response(recipe.serialize())

@app.route("/recipes/<int:recipe_id>/", methods=["DELETE"])
def delete_recipe(recipe_id):
    """
    Endpoint for deleting a recipe
    """

    recipe = Recipe.query.filter_by(id=recipe_id).first()

    if recipe is None:
        return failure_response("Recipe not found")

    db.session.delete(recipe)
    db.session.commit()

    return success_response(recipe.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
