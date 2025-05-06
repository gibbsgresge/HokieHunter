from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Commute
from db import engine  # Use db.py, not app.py

commute_bp = Blueprint('commute_bp', __name__)

# -----------------------------
# Get all commute entries
# -----------------------------
@commute_bp.route('/commute', methods=['GET'])
def get_commutes():
    with Session(engine) as session:
        commutes = session.query(Commute).all()
        return jsonify([
            {
                "CommuteID": c.CommuteID,
                "PropertyID": c.PropertyID,
                "Time": c.Time,
                "Distance": c.Distance,
                "ServiceID": c.ServiceID
            }
            for c in commutes
        ])

# -----------------------------
# Get commute by ID
# -----------------------------
@commute_bp.route('/commute/<int:commute_id>', methods=['GET'])
def get_commute(commute_id):
    with Session(engine) as session:
        commute = session.get(Commute, commute_id)
        if commute:
            return jsonify({
                "CommuteID": commute.CommuteID,
                "PropertyID": commute.PropertyID,
                "Time": commute.Time,
                "Distance": commute.Distance,
                "ServiceID": commute.ServiceID
            })
        return jsonify({"error": "Commute not found"}), 404

# -----------------------------
# Create a new commute entry
# -----------------------------
@commute_bp.route('/commute', methods=['POST'])
def create_commute():
    data = request.get_json()
    with Session(engine) as session:
        new_commute = Commute(
            PropertyID=data.get('PropertyID'),
            Time=data.get('Time'),
            Distance=data.get('Distance'),
            ServiceID=data.get('ServiceID')
        )
        session.add(new_commute)
        session.commit()
        return jsonify({"message": "Commute added", "CommuteID": new_commute.CommuteID}), 201

# -----------------------------
# Update an existing commute entry
# -----------------------------
@commute_bp.route('/commute/<int:commute_id>', methods=['PUT'])
def update_commute(commute_id):
    data = request.get_json()
    with Session(engine) as session:
        commute = session.get(Commute, commute_id)
        if commute:
            commute.PropertyID = data.get('PropertyID', commute.PropertyID)
            commute.Time = data.get('Time', commute.Time)
            commute.Distance = data.get('Distance', commute.Distance)
            commute.ServiceID = data.get('ServiceID', commute.ServiceID)
            session.commit()
            return jsonify({"message": "Commute updated"})
        return jsonify({"error": "Commute not found"}), 404

# -----------------------------
# Delete a commute entry
# -----------------------------
@commute_bp.route('/commute/<int:commute_id>', methods=['DELETE'])
def delete_commute(commute_id):
    with Session(engine) as session:
        commute = session.get(Commute, commute_id)
        if commute:
            session.delete(commute)
            session.commit()
            return jsonify({"message": "Commute deleted"})
        return jsonify({"error": "Commute not found"}), 404
