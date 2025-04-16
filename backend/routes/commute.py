from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Commute
from db import engine  # Make sure you use db.py, not app.py

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
