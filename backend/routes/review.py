from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Review
from db import engine

review_bp = Blueprint('review_bp', __name__)

# -----------------------------
# Get all reviews
# -----------------------------
@review_bp.route('/review', methods=['GET'])
def get_reviews():
    with Session(engine) as session:
        reviews = session.query(Review).all()
        return jsonify([
            {
                "ReviewID": r.ReviewID,
                "StudentID": r.StudentID,
                "PropertyID": r.PropertyID,
                "Rating": r.Rating,
                "Comments": r.Comments
            }
            for r in reviews
        ])

# -----------------------------
# Create a new review
# -----------------------------
@review_bp.route('/review', methods=['POST'])
def create_review():
    data = request.get_json()
    with Session(engine) as session:
        new_review = Review(
            StudentID=data.get('StudentID'),
            PropertyID=data.get('PropertyID'),
            Rating=data.get('Rating'),
            Comments=data.get('Comments')
        )
        session.add(new_review)
        session.commit()
        return jsonify({"message": "Review submitted", "ReviewID": new_review.ReviewID}), 201
