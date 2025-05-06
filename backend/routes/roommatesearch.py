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
# Get roommate search by ID
# -----------------------------
@roommatesearch_bp.route('/roommatesearch/<int:search_id>', methods=['GET'])
def get_roommate_search(search_id):
    with Session(engine) as session:
        search = session.get(Roommatesearch, search_id)
        if search:
            return jsonify({
                "SearchID": search.SearchID,
                "StudentID": search.StudentID,
                "Preferences": search.Preferences
            })
        return jsonify({"error": "Roommate search not found"}), 404

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

# -----------------------------
# Update a roommate search
# -----------------------------
@roommatesearch_bp.route('/roommatesearch/<int:search_id>', methods=['PUT'])
def update_roommate_search(search_id):
    data = request.get_json()
    with Session(engine) as session:
        search = session.get(Roommatesearch, search_id)
        if search:
            search.StudentID = data.get('StudentID', search.StudentID)
            search.Preferences = data.get('Preferences', search.Preferences)
            session.commit()
            return jsonify({"message": "Roommate search updated"})
        return jsonify({"error": "Roommate search not found"}), 404

# -----------------------------
# Delete a roommate search
# -----------------------------
@roommatesearch_bp.route('/roommatesearch/<int:search_id>', methods=['DELETE'])
def delete_roommate_search(search_id):
    with Session(engine) as session:
        search = session.get(Roommatesearch, search_id)
        if search:
            session.delete(search)
            session.commit()
            return jsonify({"message": "Roommate search deleted"})
        return jsonify({"error": "Roommate search not found"}), 404
