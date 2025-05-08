from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Admin
from db import engine  

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admin', methods=['GET'])
def get_admins():
    with Session(engine) as session:
        admins = session.query(Admin).all()
        return jsonify([
            {
                "AdminID": a.AdminID,
                "Email": a.Email,
                "Role": a.Role,
                "Permissions": a.Permissions
            }
            for a in admins
        ])


@admin_bp.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    with Session(engine) as session:
        admin = session.get(Admin, admin_id)
        if admin:
            return jsonify({
                "AdminID": admin.AdminID,
                "Email": admin.Email,
                "Role": admin.Role,
                "Permissions": admin.Permissions
            })
        return jsonify({"error": "Admin not found"}), 404


@admin_bp.route('/admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    with Session(engine) as session:
        new_admin = Admin(
            Email=data['Email'],
            Role='admin',  # set role explicitly
            Permissions=data.get('Permissions')
        )
        session.add(new_admin)
        session.commit()
        return jsonify({"message": "Admin created", "AdminID": new_admin.AdminID}), 201


@admin_bp.route('/admin/<int:admin_id>', methods=['PUT'])
def update_admin(admin_id):
    data = request.get_json()
    with Session(engine) as session:
        admin = session.get(Admin, admin_id)
        if admin:
            admin.Email = data.get('Email', admin.Email)
            admin.Permissions = data.get('Permissions', admin.Permissions)
            session.commit()
            return jsonify({"message": "Admin updated"})
        return jsonify({"error": "Admin not found"}), 404


@admin_bp.route('/admin/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    with Session(engine) as session:
        admin = session.get(Admin, admin_id)
        if admin:
            session.delete(admin)
            session.commit()
            return jsonify({"message": "Admin deleted"})
        return jsonify({"error": "Admin not found"}), 404
