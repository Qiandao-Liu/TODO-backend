from db import db
from flask import Flask

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/users/")
def get_users():
    pass

@app.route("/users/<int:user_id>/")
def get_specific_user(user_id):
    pass

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
    pass

@app.route("/recipes/<int:recipe_id>/")
def get_specific_recipe(recipe_id):
    pass

@app.route("/recipes/", methods=["POST"])
def create_recipe():
    pass

@app.route("/recipes/<int:recipe_id>/", methods=["POST"])
def update_recipe(recipe_id):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
