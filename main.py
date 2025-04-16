from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"  # Replace with your MongoDB URI
mongo = PyMongo(app)

# Define the collection name
COLLECTION_NAME = "users"

@app.route("/")
def index():
    """
    Displays a list of users from the database.

    Returns:
        str: Rendered HTML template (index.html).
    """
    # Access the collection
    users = mongo.db[COLLECTION_NAME].find()
    return render_template("index.html", users=users)


@app.route("/add", methods=["POST"])
def add_user():
    """
    Adds a new user to the database.

    Returns:
        str: Redirects to the index page.
    """
    name = request.form.get("name")
    email = request.form.get("email")
    # Input validation: Check if name and email are provided
    if not name or not email:
        return "Name and email are required." #  Basic error handling

    # Insert the user data into the collection
    mongo.db[COLLECTION_NAME].insert_one({"name": name, "email": email})
    return redirect(url_for("index"))


@app.route("/edit/<user_id>")
def edit_user(user_id):
    """
    Displays the edit user form.

    Args:
        user_id (str): The ID of the user to edit.

    Returns:
        str: Rendered HTML template (edit.html).
    """
    # Fetch the user from the database by its ID
    user = mongo.db[COLLECTION_NAME].find_one({"_id": mongo.ObjectId(user_id)})
    if not user:
        return "User not found" # error handling
    return render_template("edit.html", user=user)


@app.route("/update/<user_id>", methods=["POST"])
def update_user(user_id):
    """
    Updates an existing user in the database.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        str: Redirects to the index page.
    """
    name = request.form.get("name")
    email = request.form.get("email")
     # Input validation: Check if name and email are provided
    if not name or not email:
        return "Name and email are required." #  Basic error handling

    # Update the user data in the collection
    mongo.db[COLLECTION_NAME].update_one(
        {"_id": mongo.ObjectId(user_id)},
        {"$set": {"name": name, "email": email}},
    )
    return redirect(url_for("index"))



@app.route("/delete/<user_id>")
def delete_user(user_id):
    """
    Deletes a user from the database.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        str: Redirects to the index page.
    """
    # Delete the user from the collection
    mongo.db[COLLECTION_NAME].delete_one({"_id": mongo.ObjectId(user_id)})
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
