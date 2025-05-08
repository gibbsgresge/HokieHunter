from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Users, Students, Landlords, Admin
from db import engine 
from .students import create_student 
from .admin import create_admin
from .landlords import create_landlord

user_bp = Blueprint('user_bp', __name__)

# -----------------------------
# Get all users
# -----------------------------
@user_bp.route('/users', methods=['GET'])
def get_users():
    with Session(engine) as session:
        users = session.query(Users).all()
        return jsonify([
            {
                "UserID": u.UserID,
                "Username": u.Username,  # ← now included
                "Email": u.Email,
                "Role": u.Role
            }
            for u in users
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

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    role = data.get('Role')

    if role == 'student':
        return create_student()
    elif role == 'landlord':
        return create_landlord()
    elif role == 'admin':
        return create_admin()
    else:
        return jsonify({'error': 'Invalid role'}), 400


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def change_user_role(user_id):
    data = request.get_json()
    new_role = data.get('Role')
    new_email = data.get('Email')
    extra_fields = data.get('Extra', {})  # optional: {'Major': ..., 'Permissions': ...}

    with Session(engine) as session:
        user = session.get(Users, user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        current_role = user.Role

        # If role changed, preserve username/password and recreate with new subclass
        if new_role != current_role:
            original_username = user.Username
            original_password_hash = user.PasswordHash

            session.delete(user)
            session.flush()  # preserve user_id

            if new_role == 'student':
                new_user = Students(
                    StudentID=user_id,
                    Email=new_email,
                    Role='student',
                    Username=original_username,
                    PasswordHash=original_password_hash,
                    Major=extra_fields.get('Major'),
                    GraduationYear=extra_fields.get('GraduationYear')
                )
            elif new_role == 'landlord':
                new_user = Landlords(
                    LandlordID=user_id,
                    Email=new_email,
                    Role='landlord',
                    Username=original_username,
                    PasswordHash=original_password_hash
                )
            elif new_role == 'admin':
                new_user = Admin(
                    AdminID=user_id,
                    Email=new_email,
                    Role='admin',
                    Username=original_username,
                    PasswordHash=original_password_hash,
                    Permissions=extra_fields.get('Permissions')
                )
            else:
                return jsonify({"error": "Invalid role"}), 400

            session.add(new_user)

        else:
            # If role is unchanged, allow email updates only
            if new_email and user.Email != new_email:
                user.Email = new_email

        session.commit()
        return jsonify({"message": "User role updated successfully"}), 200



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
