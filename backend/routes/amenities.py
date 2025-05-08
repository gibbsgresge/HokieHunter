from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Amenities, Property
from db import engine

amenities_bp = Blueprint('amenities_bp', __name__)

# -----------------------------
# Get all amenities
# -----------------------------
@amenities_bp.route('/amenities', methods=['GET'])
def get_amenities():
    with Session(engine) as session:
        amenities = (
            session.query(
                Amenities.AmenityID,
                Amenities.PropertyID,
                Amenities.Type,
                Property.Name.label("PropertyName")
            )
            .join(Property, Amenities.PropertyID == Property.PropertyID)
            .all()
        )

        return jsonify([
            {
                "AmenityID": a.AmenityID,
                "PropertyID": a.PropertyID,
                "Type": a.Type,
                "PropertyName": a.PropertyName
            }
            for a in amenities
        ])


# -----------------------------
# Get amenity by ID
# -----------------------------
@amenities_bp.route('/amenities/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    with Session(engine) as session:
        amenity = session.get(Amenities, amenity_id)
        if amenity:
            return jsonify({
                "AmenityID": amenity.AmenityID,
                "PropertyID": amenity.PropertyID,
                "Type": amenity.Type
            })
        return jsonify({"error": "Amenity not found"}), 404

# -----------------------------
# Create a new amenity
# -----------------------------
@amenities_bp.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    with Session(engine) as session:
        new_amenity = Amenities(
            PropertyID=data.get('PropertyID'),
            Type=data.get('Type')
        )
        session.add(new_amenity)
        session.commit()
        return jsonify({"message": "Amenity added", "AmenityID": new_amenity.AmenityID}), 201

# -----------------------------
# Update an existing amenity
# -----------------------------
@amenities_bp.route('/amenities/<int:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.get_json()
    with Session(engine) as session:
        amenity = session.get(Amenities, amenity_id)
        if amenity:
            amenity.PropertyID = data.get('PropertyID', amenity.PropertyID)
            amenity.Type = data.get('Type', amenity.Type)
            session.commit()
            return jsonify({"message": "Amenity updated"})
        return jsonify({"error": "Amenity not found"}), 404

# -----------------------------
# Delete an amenity
# -----------------------------
@amenities_bp.route('/amenities/<int:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    with Session(engine) as session:
        amenity = session.get(Amenities, amenity_id)
        if amenity:
            session.delete(amenity)
            session.commit()
            return jsonify({"message": "Amenity deleted"})
        return jsonify({"error": "Amenity not found"}), 404
