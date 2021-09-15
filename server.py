from datetime import datetime
from flask import Flask, request, jsonify
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)

# db config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# config sqlite3 to enforce foreign key contrains
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close

db = SQLAlchemy(app)
now = datetime.now()

# models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("Blogpost")

class Blogpost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)

# routes
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"})

@app.route("/user/descending_id", methods=["GET"])
def get_all_users_desc():
    pass

@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_asc():
    pass

@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    pass

@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    pass

@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    pass

@app.route("/user/<user_id>", methods=["GET"])
def get_all_blog_post(user_id):
    pass

@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    pass

if __name__ == "__main__":
    app.run(debug=True)