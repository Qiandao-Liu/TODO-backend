# API (WIP)

**Users**

Get all users 
- GET /users/

Get user by id
- GET /users/<int:user_id>/

Create user
- POST /users/

Add bookmark
- POST /users/<int:user_id>/bookmark/

Remove bookmark
- DELETE /users/<int:user_id>/bookmark/


**Recipes**
Get all recipes
- GET /recipes/

Get recipe by id
- GET /recipes/<int:recipe_id>/

Create recipe
- POST /recipes/

Update recipe
- POST /recipes/<int:recipe_id>/

