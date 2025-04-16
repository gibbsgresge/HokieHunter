from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Roommatesearch
from db import engine

roommatesearch_bp = Blueprint('roommatesearch_bp', __name__)

# -----------------------------
# Get all roommate searches
# -----------------------------
@roommatesearch_bp.route('/roommatesearch', methods=['GET'])
def get_roommate_searches():
    with Session(engine) as session:
        searches = session.query(Roommatesearch).all()
        return jsonify([
            {
                "SearchID": s.SearchID,
                "StudentID": s.StudentID,
                "Preferences": s.Preferences
            }
            for s in searches
        ])

# -----------------------------
# Create a new roommate search
# -----------------------------
@roommatesearch_bp.route('/roommatesearch', methods=['POST'])
def create_roommate_search():
    data = request.get_json()
    with Session(engine) as session:
        new_search = Roommatesearch(
            StudentID=data.get('StudentID'),
            Preferences=data.get('Preferences')
        )
        session.add(new_search)
        session.commit()
        return jsonify({"message": "Roommate search created", "SearchID": new_search.SearchID}), 201
