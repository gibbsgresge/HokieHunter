from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from models import Users, Students, Landlords
from db import engine
from sqlalchemy.orm import with_polymorphic, joinedload

auth_bp = Blueprint('auth', __name__)

# -----------------------------
# STUDENT SIGNUP
# -----------------------------
@auth_bp.route('/signup/student', methods=['POST'])
def signup_student():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    major = data.get('major')
    graduation_year = data.get('graduation_year')

    if not all([username, email, password]):
        return jsonify({'error': 'Missing username, email, or password'}), 400

    password_hash = generate_password_hash(password)

    with Session(engine) as session:
        if session.query(Users).filter_by(Username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        new_student = Students(
            Username=username,
            Email=email,
            Role='student',
            PasswordHash=password_hash,
            Major=major,
            GraduationYear=graduation_year
        )
        session.add(new_student)
        session.commit()

        return jsonify({'message': 'Student account created', 'user_id': new_student.UserID})


# -----------------------------
# LANDLORD SIGNUP
# -----------------------------
@auth_bp.route('/signup/landlord', methods=['POST'])
def signup_landlord():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'Missing username, email, or password'}), 400

    password_hash = generate_password_hash(password)

    with Session(engine) as session:
        if session.query(Users).filter_by(Username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        new_landlord = Landlords(
            Username=username,
            Email=email,
            Role='landlord',
            PasswordHash=password_hash
        )
        session.add(new_landlord)
        session.commit()

        return jsonify({'message': 'Landlord account created', 'user_id': new_landlord.UserID})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'error': 'Username and password required'}), 400

    with Session(engine) as session:
        user = session.query(Users).filter_by(Username=username).first()

        if not user or not check_password_hash(user.PasswordHash, password):
            return jsonify({'error': 'Invalid username or password'}), 401

        return jsonify({
            'message': f'Welcome, {username}!',
            'user_id': user.UserID,
            'role': user.Role
        })


# -----------------------------
# ADMIN SIGNUP
# -----------------------------
@auth_bp.route('/signup/admin', methods=['POST'])
def signup_admin():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'Missing username, email, or password'}), 400

    password_hash = generate_password_hash(password)

    with Session(engine) as session:
        if session.query(Users).filter_by(Username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        new_admin = Users(
            Username=username,
            Email=email,
            Role='admin',
            PasswordHash=password_hash
        )
        session.add(new_admin)
        session.commit()

        return jsonify({'message': 'Admin account created', 'user_id': new_admin.UserID})





@auth_bp.route('/users/<int:user_id>/promote', methods=['PUT'])
def promote_to_admin(user_id):
    with Session(engine) as session:
        user = session.query(Users).filter_by(UserID=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user.Role = 'admin'

        # Explicitly delete subclass without deleting base user
        if user.Role == 'student':
            session.query(Students).filter_by(UserID=user_id).delete()
        elif user.Role == 'landlord':
            session.query(Landlords).filter_by(UserID=user_id).delete()

        session.commit()
        return jsonify({'message': f'User {user.Username} promoted to admin'})

