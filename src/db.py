from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

saved_recipes_table = db.Table("bookmarks_users", db.Model.metadata,
                               db.Column("recipe_id", db.Integer, db.ForeignKey("recipe.id")),
                               db.Column("user_id", db.Integer, db.ForeignKey("user.id")))


# your classes here
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    published_recipes = db.relationship("Recipe", cascade="delete")
    bookmarked_recipes = db.relationship("Recipe", secondary=saved_recipes_table, back_populates='bookmarkers')

    def __init__(self, username):
        self.username = username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "published_recipes": [r.simple_serialize() for r in self.published_recipes],
            "bookmarked_recipes": [b.simple_serialize() for b in self.bookmarked_recipes]
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    # image is a url/file address to access the image, wherever we decide to store it
    image = db.Column(db.String)
    description = db.Column(db.String)
    # Can't make it a list unless we make it another table relationship (meaning that users have less flexibility)
    ingredients = db.Column(db.String, nullable=False)
    directions = db.Column(db.String, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bookmarkers = db.relationship("User", secondary=saved_recipes_table, back_populates='bookmarked_recipes')

    def __init__(self, title, ingredients, directions, owner, image=None, description=None):
        self.title = title
        self.ingredients = ingredients
        self.directions = directions
        self.owner = owner
        self.image = image
        self.description = description

    def serialize(self):
        dic =  {
            "id": self.id,
            "title": self.title,
            "ingredients": self.ingredients,
            "directions": self.directions,
            "owner": self.owner.simple_serialize(),
        }
        if self.description is not None:
            dic["description"] = self.description
        if self.image is not None:
            dic["image"] = self.image
        return dic

    def simple_serialize(self):
        return {
            "id": self.id,
            "title": self.title
        }