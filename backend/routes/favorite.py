from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Favorite, Property, Users, Students
from sqlalchemy.orm import aliased
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
