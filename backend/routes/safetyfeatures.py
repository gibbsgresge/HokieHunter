from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Safetyfeatures, Property
from db import engine

safetyfeatures_bp = Blueprint('safetyfeatures_bp', __name__)

# -----------------------------
# Get all safety features
# -----------------------------
@safetyfeatures_bp.route('/safetyfeatures', methods=['GET'])
def get_safety_features():
    with Session(engine) as session:
        results = (
            session.query(
                Safetyfeatures.FeatureID,
                Safetyfeatures.FeatureDescription,
                Property.Name.label("PropertyName")
            )
            .join(Property, Safetyfeatures.PropertyID == Property.PropertyID)
            .all()
        )

        return jsonify([
            {
                "FeatureID": f.FeatureID,
                "FeatureDescription": f.FeatureDescription,
                "PropertyName": f.PropertyName
            }
            for f in results
        ])

# -----------------------------
# Get safety feature by ID
# -----------------------------
@safetyfeatures_bp.route('/safetyfeatures/<int:feature_id>', methods=['GET'])
def get_safety_feature(feature_id):
    with Session(engine) as session:
        feature = session.get(Safetyfeatures, feature_id)
        if feature:
            return jsonify({
                "FeatureID": feature.FeatureID,
                "PropertyID": feature.PropertyID,
                "FeatureDescription": feature.FeatureDescription
            })
        return jsonify({"error": "Safety feature not found"}), 404


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


@safetyfeatures_bp.route('/safetyfeatures/<int:feature_id>', methods=['PUT'])
def update_safety_feature(feature_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    with Session(engine) as session:
        feature = session.get(Safetyfeatures, feature_id)
        if not feature:
            return jsonify({"error": "Safety feature not found"}), 404

        # Optional updates with fallback to current values
        if 'PropertyID' in data:
            feature.PropertyID = data['PropertyID']
        if 'FeatureDescription' in data:
            feature.FeatureDescription = data['FeatureDescription']

        session.commit()
        return jsonify({
            "message": "Safety feature updated",
            "FeatureID": feature.FeatureID,
            "PropertyID": feature.PropertyID,
            "FeatureDescription": feature.FeatureDescription
        })


@safetyfeatures_bp.route('/safetyfeatures/<int:feature_id>', methods=['DELETE'])
def delete_safety_feature(feature_id):
    with Session(engine) as session:
        feature = session.get(Safetyfeatures, feature_id)
        if feature:
            session.delete(feature)
            session.commit()
            return jsonify({"message": "Safety feature deleted"})
        return jsonify({"error": "Safety feature not found"}), 404
