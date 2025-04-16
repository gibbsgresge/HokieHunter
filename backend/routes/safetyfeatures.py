from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Safetyfeatures
from db import engine

safetyfeatures_bp = Blueprint('safetyfeatures_bp', __name__)

# -----------------------------
# Get all safety features
# -----------------------------
@safetyfeatures_bp.route('/safetyfeatures', methods=['GET'])
def get_safety_features():
    with Session(engine) as session:
        features = session.query(Safetyfeatures).all()
        return jsonify([
            {
                "FeatureID": f.FeatureID,
                "PropertyID": f.PropertyID,
                "FeatureDescription": f.FeatureDescription
            }
            for f in features
        ])

# -----------------------------
# Create a new safety feature
# -----------------------------
@safetyfeatures_bp.route('/safetyfeatures', methods=['POST'])
def create_safety_feature():
    data = request.get_json()
    with Session(engine) as session:
        new_feature = Safetyfeatures(
            PropertyID=data.get('PropertyID'),
            FeatureDescription=data.get('FeatureDescription')
        )
        session.add(new_feature)
        session.commit()
        return jsonify({"message": "Safety feature added", "FeatureID": new_feature.FeatureID}), 201
