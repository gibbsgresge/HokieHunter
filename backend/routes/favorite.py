from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session, aliased
from models import Favorite, Property, Users, Students
from db import engine
import datetime

favorite_bp = Blueprint('favorite_bp', __name__)

# -----------------------------
# Get all favorites
# -----------------------------
@favorite_bp.route('/favorite', methods=['GET'])
def get_favorites():
    with Session(engine) as session:
        StudentUser = aliased(Users)

        favorites = (
            session.query(
                Favorite.FavoriteID,
                Favorite.Comments,
                Favorite.DateSaved,
                Property.Name.label("PropertyName"),
                StudentUser.Username.label("StudentUsername"),
                StudentUser.Email.label("StudentEmail")
            )
            .join(Property, Favorite.PropertyID == Property.PropertyID)
            .join(Students, Favorite.StudentID == Students.StudentID)
            .join(StudentUser, Students.StudentID == StudentUser.UserID)
            .all()
        )

        return jsonify([
            {
                "FavoriteID": fav.FavoriteID,
                "PropertyName": fav.PropertyName,
                "StudentUsername": fav.StudentUsername,
                "StudentEmail": fav.StudentEmail,
                "DateSaved": fav.DateSaved.isoformat() if fav.DateSaved else None,
                "Comments": fav.Comments
            }
            for fav in favorites
        ])

# -----------------------------
# Get favorite by ID
# -----------------------------
@favorite_bp.route('/favorite/<int:favorite_id>', methods=['GET'])
def get_favorite(favorite_id):
    with Session(engine) as session:
        favorite = session.get(Favorite, favorite_id)
        if favorite:
            return jsonify({
                "FavoriteID": favorite.FavoriteID,
                "StudentID": favorite.StudentID,
                "PropertyID": favorite.PropertyID,
                "DateSaved": favorite.DateSaved.isoformat() if favorite.DateSaved else None,
                "Comments": favorite.Comments
            })
        return jsonify({"error": "Favorite not found"}), 404

# -----------------------------
# Create a new favorite
# -----------------------------
@favorite_bp.route('/favorite', methods=['POST'])
def create_favorite():
    data = request.get_json()
    with Session(engine) as session:
        new_favorite = Favorite(
            StudentID=data.get('StudentID'),
            PropertyID=data.get('PropertyID'),
            DateSaved=datetime.date.fromisoformat(data['DateSaved']) if data.get('DateSaved') else None,
            Comments=data.get('Comments')
        )
        session.add(new_favorite)
        session.commit()
        return jsonify({"message": "Favorite added", "FavoriteID": new_favorite.FavoriteID}), 201

# -----------------------------
# Update a favorite
# -----------------------------
@favorite_bp.route('/favorite/<int:favorite_id>', methods=['PUT'])
def update_favorite(favorite_id):
    data = request.get_json()
    with Session(engine) as session:
        favorite = session.get(Favorite, favorite_id)
        if favorite:
            favorite.StudentID = data.get('StudentID', favorite.StudentID)
            favorite.PropertyID = data.get('PropertyID', favorite.PropertyID)
            if 'DateSaved' in data:
                favorite.DateSaved = datetime.date.fromisoformat(data['DateSaved']) if data['DateSaved'] else None
            favorite.Comments = data.get('Comments', favorite.Comments)
            session.commit()
            return jsonify({"message": "Favorite updated"})
        return jsonify({"error": "Favorite not found"}), 404

# -----------------------------
# Delete a favorite
# -----------------------------
@favorite_bp.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    with Session(engine) as session:
        favorite = session.get(Favorite, favorite_id)
        if favorite:
            session.delete(favorite)
            session.commit()
            return jsonify({"message": "Favorite deleted"})
        return jsonify({"error": "Favorite not found"}), 404
