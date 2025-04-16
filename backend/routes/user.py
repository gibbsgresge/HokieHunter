from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Users
from db import engine  # or however you expose the engine

user_bp = Blueprint('user_bp', __name__)

# -----------------------------
# Get all users
# -----------------------------
@user_bp.route('/users', methods=['GET'])
def get_users():
    with Session(engine) as session:
        users = session.query(Users).all()
        return jsonify([
            {"UserID": u.UserID, "Email": u.Email, "Role": u.Role} for u in users
        ])

# -----------------------------
# Get single user
# -----------------------------
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    with Session(engine) as session:
        user = session.get(Users, user_id)
        if user:
            return jsonify({"UserID": user.UserID, "Email": user.Email, "Role": user.Role})
        return jsonify({"error": "User not found"}), 404

# -----------------------------
# Create a new user
# -----------------------------
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    with Session(engine) as session:
        new_user = Users(Email=data['Email'], Role=data['Role'])
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User created", "UserID": new_user.UserID}), 201

# -----------------------------
# Update user
# -----------------------------
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    with Session(engine) as session:
        user = session.get(Users, user_id)
        if user:
            user.Email = data.get('Email', user.Email)
            user.Role = data.get('Role', user.Role)
            session.commit()
            return jsonify({"message": "User updated"})
        return jsonify({"error": "User not found"}), 404

# -----------------------------
# Delete user
# -----------------------------
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with Session(engine) as session:
        user = session.get(Users, user_id)
        if user:
            session.delete(user)
            session.commit()
            return jsonify({"message": "User deleted"})
        return jsonify({"error": "User not found"}), 404
