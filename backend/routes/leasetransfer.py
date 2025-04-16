from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Leasetransfer
from db import engine
import datetime

leasetransfer_bp = Blueprint('leasetransfer_bp', __name__)

# -----------------------------
# Get all lease transfers
# -----------------------------
@leasetransfer_bp.route('/leasetransfer', methods=['GET'])
def get_leasetransfers():
    with Session(engine) as session:
        transfers = session.query(Leasetransfer).all()
        return jsonify([
            {
                "TransferID": t.TransferID,
                "StudentID": t.StudentID,
                "PropertyID": t.PropertyID,
                "LeaseEndDate": t.LeaseEndDate.isoformat() if t.LeaseEndDate else None,
                "TransferStatus": t.TransferStatus
            }
            for t in transfers
        ])

# -----------------------------
# Create a new lease transfer
# -----------------------------
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
