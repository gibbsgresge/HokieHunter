from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session, aliased
from models import Leasetransfer, Property, Students, Users
from db import engine
import datetime

leasetransfer_bp = Blueprint('leasetransfer_bp', __name__)


@leasetransfer_bp.route('/leasetransfer', methods=['GET'])
def get_lease_transfers():
    with Session(engine) as session:
        StudentUser = aliased(Users)

        transfers = (
            session.query(
                Leasetransfer.TransferID,
                Leasetransfer.LeaseEndDate,
                Leasetransfer.TransferStatus,
                Property.Name.label("PropertyName"),
                StudentUser.Username.label("StudentUsername"),
                StudentUser.Email.label("StudentEmail")
            )
            .join(Property, Leasetransfer.PropertyID == Property.PropertyID)
            .join(Students, Leasetransfer.StudentID == Students.StudentID)
            .join(StudentUser, Students.StudentID == StudentUser.UserID)
            .all()
        )

        return jsonify([
            {
                "TransferID": t.TransferID,
                "PropertyName": t.PropertyName,
                "StudentUsername": t.StudentUsername,
                "StudentEmail": t.StudentEmail,
                "LeaseEndDate": t.LeaseEndDate,
                "TransferStatus": t.TransferStatus
            }
            for t in transfers
        ])


@leasetransfer_bp.route('/leasetransfer/<int:transfer_id>', methods=['GET'])
def get_lease_transfer(transfer_id):
    with Session(engine) as session:
        transfer = session.get(Leasetransfer, transfer_id)
        if transfer:
            return jsonify({
                "TransferID": transfer.TransferID,
                "StudentID": transfer.StudentID,
                "PropertyID": transfer.PropertyID,
                "LeaseEndDate": transfer.LeaseEndDate.isoformat() if transfer.LeaseEndDate else None,
                "TransferStatus": transfer.TransferStatus
            })
        return jsonify({"error": "Lease transfer not found"}), 404


@leasetransfer_bp.route('/leasetransfer', methods=['POST'])
def create_leasetransfer():
    data = request.get_json()
    with Session(engine) as session:
        new_transfer = Leasetransfer(
            StudentID=data.get('StudentID'),
            PropertyID=data.get('PropertyID'),
            LeaseEndDate=datetime.date.fromisoformat(data['LeaseEndDate']) if data.get('LeaseEndDate') else None,
            TransferStatus=data.get('TransferStatus')
        )
        session.add(new_transfer)
        session.commit()
        return jsonify({"message": "Lease transfer created", "TransferID": new_transfer.TransferID}), 201


@leasetransfer_bp.route('/leasetransfer/<int:transfer_id>', methods=['PUT'])
def update_leasetransfer(transfer_id):
    data = request.get_json()
    with Session(engine) as session:
        transfer = session.get(Leasetransfer, transfer_id)
        if transfer:
            transfer.StudentID = data.get('StudentID', transfer.StudentID)
            transfer.PropertyID = data.get('PropertyID', transfer.PropertyID)
            if 'LeaseEndDate' in data:
                transfer.LeaseEndDate = datetime.date.fromisoformat(data['LeaseEndDate']) if data['LeaseEndDate'] else None
            transfer.TransferStatus = data.get('TransferStatus', transfer.TransferStatus)
            session.commit()
            return jsonify({"message": "Lease transfer updated"})
        return jsonify({"error": "Lease transfer not found"}), 404


@leasetransfer_bp.route('/leasetransfer/<int:transfer_id>', methods=['DELETE'])
def delete_leasetransfer(transfer_id):
    with Session(engine) as session:
        transfer = session.get(Leasetransfer, transfer_id)
        if transfer:
            session.delete(transfer)
            session.commit()
            return jsonify({"message": "Lease transfer deleted"})
        return jsonify({"error": "Lease transfer not found"}), 404
