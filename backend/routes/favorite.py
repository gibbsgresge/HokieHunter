from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Favorite
from db import engine
import datetime

favorite_bp = Blueprint('favorite_bp', __name__)

# -----------------------------
# Get all favorites
# -----------------------------
@favorite_bp.route('/favorites', methods=['GET'])
def get_favorites():
    with Session(engine) as session:
        favorites = session.query(Favorite).all()
        return jsonify([
            {
                "FavoriteID": f.FavoriteID,
                "StudentID": f.StudentID,
                "PropertyID": f.PropertyID,
                "DateSaved": f.DateSaved.isoformat() if f.DateSaved else None,
                "Comments": f.Comments
            }
            for f in favorites
        ])

# -----------------------------
# Create a new favorite
# -----------------------------
@favorite_bp.route('/favorites', methods=['POST'])
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
