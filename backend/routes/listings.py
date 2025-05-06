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
# Get listing by ID
# -----------------------------
@list_bp.route('/list/<int:list_id>', methods=['GET'])
def get_listing(list_id):
    with Session(engine) as session:
        listing = session.get(List, list_id)
        if listing:
            return jsonify({
                "ListID": listing.ListID,
                "PropertyID": listing.PropertyID,
                "AvailableFrom": listing.AvailableFrom.isoformat() if listing.AvailableFrom else None,
                "Status": listing.Status
            })
        return jsonify({"error": "Listing not found"}), 404

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

# -----------------------------
# Update an existing listing
# -----------------------------
@list_bp.route('/list/<int:list_id>', methods=['PUT'])
def update_listing(list_id):
    data = request.get_json()
    with Session(engine) as session:
        listing = session.get(List, list_id)
        if listing:
            listing.PropertyID = data.get('PropertyID', listing.PropertyID)
            if 'AvailableFrom' in data:
                listing.AvailableFrom = datetime.date.fromisoformat(data['AvailableFrom']) if data['AvailableFrom'] else None
            listing.Status = data.get('Status', listing.Status)
            session.commit()
            return jsonify({"message": "Listing updated"})
        return jsonify({"error": "Listing not found"}), 404

# -----------------------------
# Delete a listing
# -----------------------------
@list_bp.route('/list/<int:list_id>', methods=['DELETE'])
def delete_listing(list_id):
    with Session(engine) as session:
        listing = session.get(List, list_id)
        if listing:
            session.delete(listing)
            session.commit()
            return jsonify({"message": "Listing deleted"})
        return jsonify({"error": "Listing not found"}), 404
