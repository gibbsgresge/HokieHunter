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
# Get message by ID
# -----------------------------
@message_bp.route('/message/<int:message_id>', methods=['GET'])
def get_message(message_id):
    with Session(engine) as session:
        message = session.get(Message, message_id)
        if message:
            return jsonify({
                "MessageID": message.MessageID,
                "SenderID": message.SenderID,
                "Content": message.Content,
                "Timestamp": message.Timestamp.isoformat() if message.Timestamp else None
            })
        return jsonify({"error": "Message not found"}), 404

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

# -----------------------------
# Update a message
# -----------------------------
@message_bp.route('/message/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    data = request.get_json()
    with Session(engine) as session:
        message = session.get(Message, message_id)
        if message:
            message.SenderID = data.get('SenderID', message.SenderID)
            message.Content = data.get('Content', message.Content)
            session.commit()
            return jsonify({"message": "Message updated"})
        return jsonify({"error": "Message not found"}), 404

# -----------------------------
# Delete a message
# -----------------------------
@message_bp.route('/message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    with Session(engine) as session:
        message = session.get(Message, message_id)
        if message:
            session.delete(message)
            session.commit()
            return jsonify({"message": "Message deleted"})
        return jsonify({"error": "Message not found"}), 404
