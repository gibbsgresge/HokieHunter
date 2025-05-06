from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Landlords, Property
from db import engine  # Make sure engine is accessible here

landlords_bp = Blueprint('landlords_bp', __name__)

# -----------------------------
# Get all landlords
# -----------------------------
@landlords_bp.route('/landlords', methods=['GET'])
def get_landlords():
    with Session(engine) as session:
        landlords = session.query(Landlords).all()
        return jsonify([
            {
                "LandlordID": l.LandlordID,
                "Email": l.Email,
                "Role": l.Role
            }
            for l in landlords
        ])

# -----------------------------
# Get a single landlord
# -----------------------------
@landlords_bp.route('/landlords/<int:landlord_id>', methods=['GET'])
def get_landlord(landlord_id):
    with Session(engine) as session:
        landlord = session.get(Landlords, landlord_id)
        if landlord:
            return jsonify({
                "LandlordID": landlord.LandlordID,
                "Email": landlord.Email,
                "Role": landlord.Role
            })
        return jsonify({"error": "Landlord not found"}), 404

# -----------------------------
# Create a new landlord
# -----------------------------
@landlords_bp.route('/landlords', methods=['POST'])
def create_landlord():
    data = request.get_json()
    with Session(engine) as session:
        new_landlord = Landlords(
            Email=data['Email'],
            Role='landlord'  # explicitly set role
        )
        session.add(new_landlord)
        session.commit()
        return jsonify({"message": "Landlord created", "LandlordID": new_landlord.LandlordID}), 201

# -----------------------------
# Update landlord
# -----------------------------
@landlords_bp.route('/landlords/<int:landlord_id>', methods=['PUT'])
def update_landlord(landlord_id):
    data = request.get_json()
    with Session(engine) as session:
        landlord = session.get(Landlords, landlord_id)
        if landlord:
            landlord.Email = data.get('Email', landlord.Email)
            session.commit()
            return jsonify({"message": "Landlord updated"})
        return jsonify({"error": "Landlord not found"}), 404

# -----------------------------
# Delete landlord
# -----------------------------
@landlords_bp.route('/landlords/<int:landlord_id>', methods=['DELETE'])
def delete_landlord(landlord_id):
    with Session(engine) as session:
        landlord = session.get(Landlords, landlord_id)
        if landlord:
            session.delete(landlord)
            session.commit()
            return jsonify({"message": "Landlord deleted"})
        return jsonify({"error": "Landlord not found"}), 404


#VERY IMPORTANT ROUTE LANDLORD BEING LINKED WITH PROPORTY 
@landlords_bp.route('/landlord/<int:landlord_id>/properties', methods=['GET'])
def get_landlord_properties(landlord_id):
    with Session(engine) as session:
        properties = session.query(Property).filter_by(LandlordID=landlord_id).all()
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