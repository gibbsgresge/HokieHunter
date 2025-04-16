from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models import Message
from db import engine
import datetime

message_bp = Blueprint('message_bp', __name__)

# -----------------------------
# Get all messages
# -----------------------------
@message_bp.route('/message', methods=['GET'])
def get_messages():
    with Session(engine) as session:
        messages = session.query(Message).all()
        return jsonify([
            {
                "MessageID": m.MessageID,
                "SenderID": m.SenderID,
                "Content": m.Content,
                "Timestamp": m.Timestamp.isoformat() if m.Timestamp else None
            }
            for m in messages
        ])

# -----------------------------
# Create a new message
# -----------------------------
@message_bp.route('/message', methods=['POST'])
def create_message():
    data = request.get_json()
    with Session(engine) as session:
        new_message = Message(
            SenderID=data.get('SenderID'),
            Content=data.get('Content'),
            Timestamp=datetime.datetime.utcnow()
        )
        session.add(new_message)
        session.commit()
        return jsonify({"message": "Message sent", "MessageID": new_message.MessageID}), 201
