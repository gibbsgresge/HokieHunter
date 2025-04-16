from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Students
from db import engine  # or wherever you create the engine

students_bp = Blueprint('students_bp', __name__)

# -----------------------------
# Get all students
# -----------------------------
@students_bp.route('/students', methods=['GET'])
def get_students():
    with Session(engine) as session:
        students = session.query(Students).all()
        return jsonify([
            {
                "StudentID": s.StudentID,
                "Email": s.Email,
                "Role": s.Role,
                "Major": s.Major,
                "GraduationYear": s.GraduationYear
            }
            for s in students
        ])

# -----------------------------
# Get a single student
# -----------------------------
@students_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    with Session(engine) as session:
        student = session.get(Students, student_id)
        if student:
            return jsonify({
                "StudentID": student.StudentID,
                "Email": student.Email,
                "Role": student.Role,
                "Major": student.Major,
                "GraduationYear": student.GraduationYear
            })
        return jsonify({"error": "Student not found"}), 404

# -----------------------------
# Create a new student
# -----------------------------
@students_bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    with Session(engine) as session:
        new_student = Students(
            Email=data['Email'],
            Role='student',  # hardcoded to 'student'
            Major=data.get('Major'),
            GraduationYear=data.get('GraduationYear')
        )
        session.add(new_student)
        session.commit()
        return jsonify({"message": "Student created", "StudentID": new_student.StudentID}), 201

# -----------------------------
# Update student
# -----------------------------
@students_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    with Session(engine) as session:
        student = session.get(Students, student_id)
        if student:
            student.Email = data.get('Email', student.Email)
            student.Major = data.get('Major', student.Major)
            student.GraduationYear = data.get('GraduationYear', student.GraduationYear)
            session.commit()
            return jsonify({"message": "Student updated"})
        return jsonify({"error": "Student not found"}), 404

# -----------------------------
# Delete student
# -----------------------------
@students_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    with Session(engine) as session:
        student = session.get(Students, student_id)
        if student:
            session.delete(student)
            session.commit()
            return jsonify({"message": "Student deleted"})
        return jsonify({"error": "Student not found"}), 404
