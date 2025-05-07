from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Review, Property
from db import engine
from sqlalchemy.orm import joinedload
review_bp = Blueprint('review_bp', __name__)

# -----------------------------
# Get all reviews
# -----------------------------
@review_bp.route('/review', methods=['GET'])
def get_reviews():
    with Session(engine) as session:
        reviews = (
            session.query(
                Review.ReviewID,
                Review.Rating,
                Review.Comments,
                Property.Name.label("PropertyName")
            )
            .join(Property, Review.PropertyID == Property.PropertyID)
            .all()
        )

        return jsonify([
            {
                "ReviewID": r.ReviewID,
                "Rating": r.Rating,
                "Comments": r.Comments,
                "PropertyName": r.PropertyName
            }
            for r in reviews
        ])
# -----------------------------
# Get review by ID
# -----------------------------
@review_bp.route('/review/<int:review_id>', methods=['GET'])
def get_review(review_id):
    with Session(engine) as session:
        review = session.get(Review, review_id)
        if review:
            return jsonify({
                "ReviewID": review.ReviewID,
                "StudentID": review.StudentID,
                "PropertyID": review.PropertyID,
                "Rating": review.Rating,
                "Comments": review.Comments
            })
        return jsonify({"error": "Review not found"}), 404

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

# -----------------------------
# Update a review
# -----------------------------
@review_bp.route('/review/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    with Session(engine) as session:
        review = session.get(Review, review_id)
        if review:
            review.StudentID = data.get('StudentID', review.StudentID)
            review.PropertyID = data.get('PropertyID', review.PropertyID)
            review.Rating = data.get('Rating', review.Rating)
            review.Comments = data.get('Comments', review.Comments)
            session.commit()
            return jsonify({"message": "Review updated"})
        return jsonify({"error": "Review not found"}), 404

# -----------------------------
# Delete a review
# -----------------------------
@review_bp.route('/review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    with Session(engine) as session:
        review = session.get(Review, review_id)
        if review:
            session.delete(review)
            session.commit()
            return jsonify({"message": "Review deleted"})
        return jsonify({"error": "Review not found"}), 404
