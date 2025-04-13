from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Users,  Property, Review, Favorite, Leasetransfer

app = Flask(__name__)

DATABASE_URI = 'mysql+pymysql://root:Root123!@localhost:3306/workbenchdb'
engine = create_engine(DATABASE_URI)
Base.metadata.bind = engine

# -----------------------------
# Users CRUD
# -----------------------------
@app.route('/users', methods=['GET'])
def get_users():
    with Session(engine) as session:
        users = session.query(Users).all()
        return jsonify([{"UserID": u.UserID, "Email": u.Email, "Role": u.Role} for u in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    with Session(engine) as session:
        user = session.get(Users, user_id)
        if user:
            return jsonify({"UserID": user.UserID, "Email": user.Email, "Role": user.Role})
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    with Session(engine) as session:
        new_user = Users(Email=data['Email'], Role=data['Role'])
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User created", "UserID": new_user.UserID}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    with Session(engine) as session:
        user = session.get(Users, user_id)
        if user:
            user.Email = data.get('Email', user.Email)
            user.Role = data.get('Role', user.Role)
            session.commit()
            return jsonify({"message": "User updated"})
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with Session(engine) as session:
        user = session.get(Users, user_id)
        if user:
            session.delete(user)
            session.commit()
            return jsonify({"message": "User deleted"})
        return jsonify({"error": "User not found"}), 404

# -----------------------------
# Property CRUD
# -----------------------------
@app.route('/properties', methods=['GET'])
def get_properties():
    with Session(engine) as session:
        properties = session.query(Property).all()
        return jsonify([{
            "PropertyID": p.PropertyID,
            "Name": p.Name,
            "Location": p.Location,
            "Price": p.Price,
            "RoomType": p.RoomType
        } for p in properties])

@app.route('/properties/<int:property_id>', methods=['GET'])
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

@app.route('/properties', methods=['POST'])
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

@app.route('/properties/<int:property_id>', methods=['PUT'])
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

@app.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    with Session(engine) as session:
        prop = session.get(Property, property_id)
        if prop:
            session.delete(prop)
            session.commit()
            return jsonify({"message": "Property deleted"})
        return jsonify({"error": "Property not found"}), 404

# -----------------------------
# Review Create
# -----------------------------
@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    with Session(engine) as session:
        new_review = Review(
            StudentID=data['StudentID'],
            PropertyID=data['PropertyID'],
            Rating=data['Rating'],
            Comments=data.get('Comments')
        )
        session.add(new_review)
        session.commit()
        return jsonify({"message": "Review added", "ReviewID": new_review.ReviewID}), 201

# -----------------------------
# Favorite Create
# -----------------------------
@app.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    with Session(engine) as session:
        favorite = Favorite(
            StudentID=data['StudentID'],
            PropertyID=data['PropertyID'],
            DateSaved=data.get('DateSaved'),
            Comments=data.get('Comments')
        )
        session.add(favorite)
        session.commit()
        return jsonify({"message": "Favorite saved", "FavoriteID": favorite.FavoriteID}), 201

# -----------------------------
# Lease Transfer Create
# -----------------------------
@app.route('/leasetransfers', methods=['POST'])
def create_leasetransfer():
    data = request.get_json()
    with Session(engine) as session:
        lease = Leasetransfer(
            StudentID=data['StudentID'],
            PropertyID=data['PropertyID'],
            LeaseEndDate=data.get('LeaseEndDate'),
            TransferStatus=data.get('TransferStatus')
        )
        session.add(lease)
        session.commit()
        return jsonify({"message": "Lease transfer created", "TransferID": lease.TransferID}), 201

if __name__ == '__main__':
    app.run(debug=True)