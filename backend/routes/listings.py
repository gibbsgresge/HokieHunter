from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import List
from db import engine
import datetime

list_bp = Blueprint('list_bp', __name__)

# -----------------------------
# Get all listings
# -----------------------------
@list_bp.route('/list', methods=['GET'])
def get_listings():
    with Session(engine) as session:
        listings = session.query(List).all()
        return jsonify([
            {
                "ListID": l.ListID,
                "PropertyID": l.PropertyID,
                "AvailableFrom": l.AvailableFrom.isoformat() if l.AvailableFrom else None,
                "Status": l.Status
            }
            for l in listings
        ])

# -----------------------------
# Create a new listing
# -----------------------------
@list_bp.route('/listings', methods=['POST'])
def create_listing():
    data = request.get_json()
    with Session(engine) as session:
        new_listing = List(
            PropertyID=data.get('PropertyID'),
            AvailableFrom=datetime.date.fromisoformat(data['AvailableFrom']) if data.get('AvailableFrom') else None,
            Status=data.get('Status')
        )
        session.add(new_listing)
        session.commit()
        return jsonify({"message": "Listing created", "ListID": new_listing.ListID}), 201
