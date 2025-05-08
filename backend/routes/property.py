from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from db import engine  
from models import Property, Landlords, Users
property_bp = Blueprint('property_bp', __name__)


from sqlalchemy.orm import aliased
from models import Property, Landlords, Users

@property_bp.route('/property', methods=['GET'])
def get_properties():
    with Session(engine) as session:
        UserAlias = aliased(Users)  

        results = (
            session.query(Property, UserAlias.Email, UserAlias.Username)
            .join(Landlords, Property.LandlordID == Landlords.LandlordID)
            .join(UserAlias, Landlords.LandlordID == UserAlias.UserID)
            .all()
        )

        return jsonify([
            {
                "PropertyID": prop.PropertyID,
                "Name": prop.Name,
                "Location": prop.Location,
                "Price": prop.Price,
                "RoomType": prop.RoomType,
                "LandlordEmail": email,
                "LandlordUsername": username
            }
            for prop, email, username in results
        ])



@property_bp.route('/property/<int:property_id>', methods=['GET'])
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


@property_bp.route('/property', methods=['POST'])
def create_property():
    data = request.get_json()
    required_fields = ['Name', 'Location', 'Price', 'RoomType', 'LandlordID']

    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    with Session(engine) as session:
        new_prop = Property(
            Name=data['Name'],
            Location=data['Location'],
            Price=data['Price'],
            RoomType=data['RoomType'],
            LandlordID=data['LandlordID']
        )
        session.add(new_prop)
        session.commit()
        return jsonify({
            "message": "Property created",
            "PropertyID": new_prop.PropertyID
        }), 201



@property_bp.route('/property/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    data = request.get_json()
    with Session(engine) as session:
        prop = session.query(Property).get(property_id)
        if not prop:
            return jsonify({"error": "Property not found"}), 404

        prop.Name = data.get('Name', prop.Name)
        prop.Location = data.get('Location', prop.Location)
        prop.Price = data.get('Price', prop.Price)
        prop.RoomType = data.get('RoomType', prop.RoomType)

        session.commit()
        return jsonify({"message": "Property updated"})



@property_bp.route('/property/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    with Session(engine) as session:
        prop = session.get(Property, property_id)
        if prop:
            session.delete(prop)
            session.commit()
            return jsonify({"message": "Property deleted"})
        return jsonify({"error": "Property not found"}), 404
