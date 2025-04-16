from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Movingservices
from db import engine

movingservices_bp = Blueprint('movingservices_bp', __name__)

# -----------------------------
# Get all moving services
# -----------------------------
@movingservices_bp.route('/movingservices', methods=['GET'])
def get_moving_services():
    with Session(engine) as session:
        services = session.query(Movingservices).all()
        return jsonify([
            {
                "ServiceID": s.ServiceID,
                "PropertyID": s.PropertyID,
                "CompanyName": s.CompanyName,
                "ContactInfo": s.ContactInfo
            }
            for s in services
        ])

# -----------------------------
# Create a new moving service
# -----------------------------
@movingservices_bp.route('/movingservices', methods=['POST'])
def create_moving_service():
    data = request.get_json()
    with Session(engine) as session:
        new_service = Movingservices(
            PropertyID=data.get('PropertyID'),
            CompanyName=data.get('CompanyName'),
            ContactInfo=data.get('ContactInfo')
        )
        session.add(new_service)
        session.commit()
        return jsonify({"message": "Moving service added", "ServiceID": new_service.ServiceID}), 201
