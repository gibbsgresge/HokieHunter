from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Commute, Property
from db import engine  # Use db.py, not app.py

commute_bp = Blueprint('commute_bp', __name__)


@commute_bp.route('/commute', methods=['GET'])
def get_commutes():
    with Session(engine) as session:
        commutes = (
            session.query(
                Commute.CommuteID,
                Commute.Time,
                Commute.Distance,
                Commute.ServiceID,
                Property.Name.label("PropertyName")
            )
            .join(Property, Commute.PropertyID == Property.PropertyID)
            .all()
        )

        return jsonify([
            {
                "CommuteID": c.CommuteID,
                "Time": c.Time,
                "Distance": c.Distance,
                "ServiceID": c.ServiceID,
                "PropertyName": c.PropertyName
            }
            for c in commutes
        ])


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


@commute_bp.route('/commute/<int:commute_id>', methods=['DELETE'])
def delete_commute(commute_id):
    with Session(engine) as session:
        commute = session.get(Commute, commute_id)
        if commute:
            session.delete(commute)
            session.commit()
            return jsonify({"message": "Commute deleted"})
        return jsonify({"error": "Commute not found"}), 404
