from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Landlords, Property, Movingservices, Safetyfeatures, Commute, Amenities
from db import engine  # Make sure engine is accessible here

landlords_bp = Blueprint('landlords_bp', __name__)
def is_property_owned_by_landlord(session, property_id, landlord_id):
    return session.query(Property).filter_by(PropertyID=property_id, LandlordID=landlord_id).first() is not None
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
    



# -------------------------------
# SAFETY FEATURES CRUD
# -------------------------------

@landlords_bp.route('/landlord/<int:landlord_id>/safetyfeatures', methods=['GET'])
def get_safetyfeatures_by_landlord(landlord_id):
    with Session(engine) as session:
        features = (
            session.query(Safetyfeatures)
            .join(Property, Safetyfeatures.PropertyID == Property.PropertyID)
            .filter(Property.LandlordID == landlord_id)
            .all()
        )
        return jsonify([
            {
                "FeatureID": f.FeatureID,
                "PropertyID": f.PropertyID,
                "FeatureDescription": f.FeatureDescription
            } for f in features
        ])

@landlords_bp.route('/landlord/<int:landlord_id>/safetyfeatures', methods=['POST'])
def create_safetyfeature_by_landlord(landlord_id):
    data = request.get_json()
    with Session(engine) as session:
        if not is_property_owned_by_landlord(session, data.get('PropertyID'), landlord_id):
            return jsonify({"error": "Invalid property"}), 403

        new_feature = Safetyfeatures(
            PropertyID=data.get('PropertyID'),
            FeatureDescription=data.get('FeatureDescription')
        )
        session.add(new_feature)
        session.commit()
        return jsonify({"message": "Safety feature created", "FeatureID": new_feature.FeatureID}), 201

@landlords_bp.route('/landlord/<int:landlord_id>/safetyfeatures/<int:feature_id>', methods=['PUT'])
def update_safetyfeature_by_landlord(landlord_id, feature_id):
    data = request.get_json()
    with Session(engine) as session:
        feature = session.get(Safetyfeatures, feature_id)
        if not feature:
            return jsonify({"error": "Safety feature not found"}), 404
        if not is_property_owned_by_landlord(session, feature.PropertyID, landlord_id):
            return jsonify({"error": "Not authorized"}), 403

        feature.FeatureDescription = data.get('FeatureDescription', feature.FeatureDescription)
        session.commit()
        return jsonify({"message": "Safety feature updated"})

@landlords_bp.route('/landlord/<int:landlord_id>/safetyfeatures/<int:feature_id>', methods=['DELETE'])
def delete_safetyfeature_by_landlord(landlord_id, feature_id):
    with Session(engine) as session:
        feature = session.get(Safetyfeatures, feature_id)
        if not feature or not is_property_owned_by_landlord(session, feature.PropertyID, landlord_id):
            return jsonify({"error": "Not authorized or not found"}), 404
        session.delete(feature)
        session.commit()
        return jsonify({"message": "Safety feature deleted"})

# -------------------------------
# MOVING SERVICES CRUD
# -------------------------------

@landlords_bp.route('/landlord/<int:landlord_id>/movingservices', methods=['GET'])
def get_movingservices_by_landlord(landlord_id):
    with Session(engine) as session:
        services = (
            session.query(Movingservices)
            .join(Property, Movingservices.PropertyID == Property.PropertyID)
            .filter(Property.LandlordID == landlord_id)
            .all()
        )
        return jsonify([
            {
                "ServiceID": s.ServiceID,
                "PropertyID": s.PropertyID,
                "CompanyName": s.CompanyName,
                "ContactInfo": s.ContactInfo
            } for s in services
        ])

@landlords_bp.route('/landlord/<int:landlord_id>/movingservices', methods=['POST'])
def create_movingservice_by_landlord(landlord_id):
    data = request.get_json()
    with Session(engine) as session:
        if not is_property_owned_by_landlord(session, data.get('PropertyID'), landlord_id):
            return jsonify({"error": "Invalid property"}), 403

        new_service = Movingservices(
            PropertyID=data.get('PropertyID'),
            CompanyName=data.get('CompanyName'),
            ContactInfo=data.get('ContactInfo')
        )
        session.add(new_service)
        session.commit()
        return jsonify({"message": "Moving service created", "ServiceID": new_service.ServiceID}), 201

@landlords_bp.route('/landlord/<int:landlord_id>/movingservices/<int:service_id>', methods=['PUT'])
def update_movingservice_by_landlord(landlord_id, service_id):
    data = request.get_json()
    with Session(engine) as session:
        service = session.get(Movingservices, service_id)
        if not service or not is_property_owned_by_landlord(session, service.PropertyID, landlord_id):
            return jsonify({"error": "Not authorized or not found"}), 404

        service.CompanyName = data.get('CompanyName', service.CompanyName)
        service.ContactInfo = data.get('ContactInfo', service.ContactInfo)
        session.commit()
        return jsonify({"message": "Moving service updated"})

@landlords_bp.route('/landlord/<int:landlord_id>/movingservices/<int:service_id>', methods=['DELETE'])
def delete_movingservice_by_landlord(landlord_id, service_id):
    with Session(engine) as session:
        service = session.get(Movingservices, service_id)
        if not service or not is_property_owned_by_landlord(session, service.PropertyID, landlord_id):
            return jsonify({"error": "Not authorized or not found"}), 404
        session.delete(service)
        session.commit()
        return jsonify({"message": "Moving service deleted"})

# -------------------------------
# COMMUTE INFO CRUD
# -------------------------------

@landlords_bp.route('/landlord/<int:landlord_id>/commute', methods=['GET'])
def get_commute_by_landlord(landlord_id):
    with Session(engine) as session:
        commutes = (
            session.query(Commute)
            .join(Property, Commute.PropertyID == Property.PropertyID)
            .filter(Property.LandlordID == landlord_id)
            .all()
        )
        return jsonify([
            {
                "CommuteID": c.CommuteID,
                "PropertyID": c.PropertyID,
                "Time": c.Time,
                "Distance": c.Distance
            } for c in commutes
        ])

@landlords_bp.route('/landlord/<int:landlord_id>/commute', methods=['POST'])
def create_commute_by_landlord(landlord_id):
    data = request.get_json()
    with Session(engine) as session:
        if not is_property_owned_by_landlord(session, data.get('PropertyID'), landlord_id):
            return jsonify({"error": "Invalid property"}), 403

        new_commute = Commute(
            PropertyID=data.get('PropertyID'),
            Time=data.get('Time'),
            Distance=data.get('Distance')
        )
        session.add(new_commute)
        session.commit()
        return jsonify({"message": "Commute info created", "CommuteID": new_commute.CommuteID}), 201

@landlords_bp.route('/landlord/<int:landlord_id>/commute/<int:commute_id>', methods=['PUT'])
def update_commute_by_landlord(landlord_id, commute_id):
    data = request.get_json()
    with Session(engine) as session:
        commute = session.get(Commute, commute_id)
        if not commute or not is_property_owned_by_landlord(session, commute.PropertyID, landlord_id):
            return jsonify({"error": "Not authorized or not found"}), 404

        commute.Time = data.get('Time', commute.Time)
        commute.Distance = data.get('Distance', commute.Distance)
        session.commit()
        return jsonify({"message": "Commute updated"})

@landlords_bp.route('/landlord/<int:landlord_id>/commute/<int:commute_id>', methods=['DELETE'])
def delete_commute_by_landlord(landlord_id, commute_id):
    with Session(engine) as session:
        commute = session.get(Commute, commute_id)
        if not commute or not is_property_owned_by_landlord(session, commute.PropertyID, landlord_id):
            return jsonify({"error": "Not authorized or not found"}), 404
        session.delete(commute)
        session.commit()
        return jsonify({"message": "Commute deleted"})

# -------------------------------
# AMENITIES CRUD
# -------------------------------

@landlords_bp.route('/landlord/<int:landlord_id>/amenities', methods=['GET'])
def get_amenities_by_landlord(landlord_id):
    with Session(engine) as session:
        amenities = (
            session.query(Amenities)
            .join(Property, Amenities.PropertyID == Property.PropertyID)
            .filter(Property.LandlordID == landlord_id)
            .all()
        )
        return jsonify([
            {
                "AmenityID": a.AmenityID,
                "PropertyID": a.PropertyID,
                "Type": a.Type
            } for a in amenities
        ])

@landlords_bp.route('/landlord/<int:landlord_id>/amenities', methods=['POST'])
def create_amenity_by_landlord(landlord_id):
    data = request.get_json()
    with Session(engine) as session:
        if not is_property_owned_by_landlord(session, data.get('PropertyID'), landlord_id):
            return jsonify({"error": "Invalid property"}), 403

        new_amenity = Amenities(
            PropertyID=data.get('PropertyID'),
            Type=data.get('Type')
        )
        session.add(new_amenity)
        session.commit()
        return jsonify({"message": "Amenity created", "AmenityID": new_amenity.AmenityID}), 201

@landlords_bp.route('/landlord/<int:landlord_id>/amenities/<int:amenity_id>', methods=['PUT'])
def update_amenity_by_landlord(landlord_id, amenity_id):
    data = request.get_json()
    with Session(engine) as session:
        amenity = session.get(Amenities, amenity_id)
        if not amenity or not is_property_owned_by_landlord(session, amenity.PropertyID, landlord_id):
            return jsonify({"error": "Not authorized or not found"}), 404

        amenity.Type = data.get('Type', amenity.Type)
        session.commit()
        return jsonify({"message": "Amenity updated"})

@landlords_bp.route('/landlord/<int:landlord_id>/amenities/<int:amenity_id>', methods=['DELETE'])
def delete_amenity_by_landlord(landlord_id, amenity_id):
    with Session(engine) as session:
        amenity = session.get(Amenities, amenity_id)
        if not amenity or not is_property_owned_by_landlord(session, amenity.PropertyID, landlord_id):
            return jsonify({"error": "Not authorized or not found"}), 404
        session.delete(amenity)
        session.commit()
        return jsonify({"message": "Amenity deleted"})

