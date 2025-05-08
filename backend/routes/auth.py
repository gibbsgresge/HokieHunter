from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session, with_polymorphic
from models import Users, Students, Landlords, Admin
from db import engine

auth_bp = Blueprint('auth', __name__)


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

        new_admin = Admin(
            Username=username,
            Email=email,
            Role='admin',
            PasswordHash=password_hash,
            Permissions='all'
        )
        session.add(new_admin)
        session.commit()
        return jsonify({'message': 'Admin account created', 'user_id': new_admin.UserID})



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

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



@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not all([username, old_password, new_password]):
        return jsonify({'error': 'Username, old password, and new password are required'}), 400

    with Session(engine) as session:
        UserWithSubclasses = with_polymorphic(Users, [Admin, Students, Landlords])
        user = session.query(UserWithSubclasses).filter(Users.Username == username).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404
        if not check_password_hash(user.PasswordHash, old_password):
            return jsonify({'error': 'Old password is incorrect'}), 403

        user.PasswordHash = generate_password_hash(new_password)
        session.commit()

        return jsonify({'message': 'Password changed successfully'})




@auth_bp.route('/users/<int:user_id>/promote', methods=['PUT'])
def promote_to_admin(user_id):
    with Session(engine) as session:
        user = session.query(Users).filter_by(UserID=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        current_role = user.Role

        
        if current_role == 'student':
            session.query(Students).filter_by(StudentID=user_id).delete()
        elif current_role == 'landlord':
            session.query(Landlords).filter_by(LandlordID=user_id).delete()

      
        new_admin = Admin(
            AdminID=user_id,
            Username=user.Username,
            Email=user.Email,
            Role='admin',
            PasswordHash=user.PasswordHash,
            Permissions='all'
        )

        session.delete(user)
        session.flush() 
        session.add(new_admin)
        session.commit()

        return jsonify({'message': f'User {new_admin.Username} promoted to admin'})
