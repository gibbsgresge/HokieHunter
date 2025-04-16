from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Amenities
from db import engine

amenities_bp = Blueprint('amenities_bp', __name__)

# -----------------------------
# Get all amenities
# -----------------------------
@amenities_bp.route('/amenities', methods=['GET'])
def get_amenities():
    with Session(engine) as session:
        amenities = session.query(Amenities).all()
        return jsonify([
            {
                "AmenityID": a.AmenityID,
                "ListID": a.ListID,
                "Type": a.Type
            }
            for a in amenities
        ])

# -----------------------------
# Create a new amenity
# -----------------------------
@amenities_bp.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    with Session(engine) as session:
        new_amenity = Amenities(
            ListID=data.get('ListID'),
            Type=data.get('Type')
        )
        session.add(new_amenity)
        session.commit()
        return jsonify({"message": "Amenity added", "AmenityID": new_amenity.AmenityID}), 201
