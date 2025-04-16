from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Property
from db import engine  # make sure this points to your SQLAlchemy engine

property_bp = Blueprint('property_bp', __name__)

# -----------------------------
# Get all properties
# -----------------------------
@property_bp.route('/properties', methods=['GET'])
def get_properties():
    with Session(engine) as session:
        properties = session.query(Property).all()
        return jsonify([
            {
                "PropertyID": p.PropertyID,
                "Name": p.Name,
                "Location": p.Location,
                "Price": p.Price,
                "RoomType": p.RoomType
            }
            for p in properties
        ])

# -----------------------------
# Get a single property
# -----------------------------
@property_bp.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    with Session(engine) as session:
        prop = session.get(Property, property_id)
        if prop:
            return jsonify({
                "PropertyID": prop.PropertyID,
                "Name": prop.Name,
                "Location": prop.Location,
                "Price": prop.Price,
                "RoomType": prop.RoomType
            })
        return jsonify({"error": "Property not found"}), 404

# -----------------------------
# Create a new property
# -----------------------------
@property_bp.route('/properties', methods=['POST'])
def create_property():
    data = request.get_json()
    with Session(engine) as session:
        new_prop = Property(
            Name=data['Name'],
            Location=data['Location'],
            Price=data['Price'],
            RoomType=data['RoomType']
        )
        session.add(new_prop)
        session.commit()
        return jsonify({"message": "Property created", "PropertyID": new_prop.PropertyID}), 201

# -----------------------------
# Update property
# -----------------------------
@property_bp.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    data = request.get_json()
    with Session(engine) as session:
        prop = session.get(Property, property_id)
        if prop:
            prop.Name = data.get('Name', prop.Name)
            prop.Location = data.get('Location', prop.Location)
            prop.Price = data.get('Price', prop.Price)
            prop.RoomType = data.get('RoomType', prop.RoomType)
            session.commit()
            return jsonify({"message": "Property updated"})
        return jsonify({"error": "Property not found"}), 404

# -----------------------------
# Delete property
# -----------------------------
@property_bp.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    with Session(engine) as session:
        prop = session.get(Property, property_id)
        if prop:
            session.delete(prop)
            session.commit()
            return jsonify({"message": "Property deleted"})
        return jsonify({"error": "Property not found"}), 404
