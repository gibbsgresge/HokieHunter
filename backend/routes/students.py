from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Students, Leasetransfer, Review, Favorite, Roommatesearch, Property
from db import engine
import datetime

students_bp = Blueprint('students_bp', __name__)

# -----------------------------
# Students CRUD
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
            } for s in students
        ])

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

@students_bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    with Session(engine) as session:
        new_student = Students(
            Email=data['Email'],
            Role='student',
            Major=data.get('Major'),
            GraduationYear=data.get('GraduationYear')
        )
        session.add(new_student)
        session.commit()
        return jsonify({"message": "Student created", "StudentID": new_student.StudentID}), 201

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

@students_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    with Session(engine) as session:
        student = session.get(Students, student_id)
        if student:
            session.delete(student)
            session.commit()
            return jsonify({"message": "Student deleted"})
        return jsonify({"error": "Student not found"}), 404

# -----------------------------
# Lease Transfers
# -----------------------------
@students_bp.route('/student/<int:student_id>/lease_transfers', methods=['GET'])
def get_lease_transfers(student_id):
    with Session(engine) as session:
        results = (
            session.query(Leasetransfer, Property)
            .join(Property, Leasetransfer.PropertyID == Property.PropertyID)
            .filter(Leasetransfer.StudentID == student_id)
            .all()
        )
        return jsonify([
            {
                "TransferID": lease.TransferID,
                "LeaseEndDate": lease.LeaseEndDate,
                "TransferStatus": lease.TransferStatus,
                "PropertyName": prop.Name
            } for lease, prop in results
        ])

@students_bp.route('/lease_transfers', methods=['POST'])
def create_lease_transfer():
    data = request.get_json()
    with Session(engine) as session:
        new_lease = Leasetransfer(
            StudentID=data['StudentID'],
            PropertyID=data['PropertyID'],
            LeaseEndDate=data['LeaseEndDate'],
            TransferStatus=data['TransferStatus']
        )
        session.add(new_lease)
        session.commit()
        return jsonify({'message': 'Lease transfer added'}), 201

@students_bp.route('/lease_transfers/<int:transfer_id>', methods=['PUT'])
def update_lease_transfer(transfer_id):
    data = request.get_json()
    with Session(engine) as session:
        lease = session.get(Leasetransfer, transfer_id)
        if lease:
            lease.LeaseEndDate = data.get('LeaseEndDate', lease.LeaseEndDate)
            lease.TransferStatus = data.get('TransferStatus', lease.TransferStatus)
            session.commit()
            return jsonify({'message': 'Lease transfer updated'})
        return jsonify({'error': 'Lease transfer not found'}), 404

@students_bp.route('/lease_transfers/<int:transfer_id>', methods=['DELETE'])
def delete_lease_transfer(transfer_id):
    with Session(engine) as session:
        lease = session.get(Leasetransfer, transfer_id)
        if lease:
            session.delete(lease)
            session.commit()
            return jsonify({'message': 'Lease transfer deleted'})
        return jsonify({'error': 'Lease transfer not found'}), 404

# -----------------------------
# Reviews
# -----------------------------
@students_bp.route('/student/<int:student_id>/reviews', methods=['GET'])
def get_reviews(student_id):
    with Session(engine) as session:
        results = (
            session.query(Review, Property)
            .join(Property, Review.PropertyID == Property.PropertyID)
            .filter(Review.StudentID == student_id)
            .all()
        )
        return jsonify([
            {
                "ReviewID": r.ReviewID,
                "Rating": r.Rating,
                "Comments": r.Comments,
                "PropertyName": p.Name
            } for r, p in results
        ])

@students_bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    with Session(engine) as session:
        new_review = Review(
            StudentID=data['StudentID'],
            PropertyID=data['PropertyID'],
            Rating=data['Rating'],
            Comments=data['Comments']
        )
        session.add(new_review)
        session.commit()
        return jsonify({'message': 'Review added'}), 201

@students_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    with Session(engine) as session:
        review = session.get(Review, review_id)
        if review:
            review.Rating = data.get('Rating', review.Rating)
            review.Comments = data.get('Comments', review.Comments)
            session.commit()
            return jsonify({'message': 'Review updated'})
        return jsonify({'error': 'Review not found'}), 404

@students_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    with Session(engine) as session:
        review = session.get(Review, review_id)
        if review:
            session.delete(review)
            session.commit()
            return jsonify({'message': 'Review deleted'})
        return jsonify({'error': 'Review not found'}), 404

# -----------------------------
# Favorites
# -----------------------------
@students_bp.route('/student/<int:student_id>/favorites', methods=['GET'])
def get_favorites(student_id):
    with Session(engine) as session:
        results = (
            session.query(Favorite, Property)
            .join(Property, Favorite.PropertyID == Property.PropertyID)
            .filter(Favorite.StudentID == student_id)
            .all()
        )
        return jsonify([
            {
                "FavoriteID": f.FavoriteID,
                "Comments": f.Comments,
                "PropertyName": p.Name
            } for f, p in results
        ])

@students_bp.route('/favorites', methods=['POST'])
def create_favorite():
    data = request.get_json()
    with Session(engine) as session:
        new_fav = Favorite(
            StudentID=data['StudentID'],
            PropertyID=data['PropertyID'],
            Comments=data['Comments'],
            DateSaved=datetime.date.today()
        )
        session.add(new_fav)
        session.commit()
        return jsonify({'message': 'Favorite added'}), 201

@students_bp.route('/favorites/<int:favorite_id>', methods=['PUT'])
def update_favorite(favorite_id):
    data = request.get_json()
    with Session(engine) as session:
        favorite = session.get(Favorite, favorite_id)
        if favorite:
            favorite.Comments = data.get('Comments', favorite.Comments)
            session.commit()
            return jsonify({'message': 'Favorite updated'})
        return jsonify({'error': 'Favorite not found'}), 404

@students_bp.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    with Session(engine) as session:
        favorite = session.get(Favorite, favorite_id)
        if favorite:
            session.delete(favorite)
            session.commit()
            return jsonify({'message': 'Favorite deleted'})
        return jsonify({'error': 'Favorite not found'}), 404

# -----------------------------
# Roommate Search
# -----------------------------
@students_bp.route('/student/<int:student_id>/roommate_search', methods=['GET'])
def get_roommate_preferences(student_id):
    with Session(engine) as session:
        results = (
            session.query(Roommatesearch)
            .filter(Roommatesearch.StudentID == student_id)
            .all()
        )
        return jsonify([
            {
                "SearchID": r.SearchID,
                "Preferences": r.Preferences
            } for r in results
        ])

@students_bp.route('/student/<int:student_id>/roommate_search', methods=['POST'])
def create_roommate_preference(student_id):
    data = request.get_json()
    with Session(engine) as session:
        new_pref = Roommatesearch(
            StudentID=student_id,
            Preferences=data['Preferences']
        )
        session.add(new_pref)
        session.commit()
        return jsonify({'message': 'Roommate preference added'}), 201

@students_bp.route('/roommate_search/<int:search_id>', methods=['PUT'])
def update_roommate_preference(search_id):
    data = request.get_json()
    with Session(engine) as session:
        pref = session.get(Roommatesearch, search_id)
        if pref:
            pref.Preferences = data.get('Preferences', pref.Preferences)
            session.commit()
            return jsonify({'message': 'Roommate preference updated'})
        return jsonify({'error': 'Roommate preference not found'}), 404

@students_bp.route('/roommate_search/<int:search_id>', methods=['DELETE'])
def delete_roommate_preference(search_id):
    with Session(engine) as session:
        pref = session.get(Roommatesearch, search_id)
        if pref:
            session.delete(pref)
            session.commit()
            return jsonify({'message': 'Roommate preference deleted'})
        return jsonify({'error': 'Roommate preference not found'}), 404



