from sqlalchemy.orm import Session
from db import engine
from models import RoommateSearch, SafetyFeatures, MovingServices

# Dummy data for each table
roommate_data = [
    {"StudentID": 1, "PreferredRoomType": "Single", "StudyHabits": "Quiet", "GuestPolicy": "No guests", "Smoking": False},
    {"StudentID": 2, "PreferredRoomType": "Double", "StudyHabits": "Flexible", "GuestPolicy": "Occasional", "Smoking": False},
    {"StudentID": 3, "PreferredRoomType": "Triple", "StudyHabits": "Loud", "GuestPolicy": "Often", "Smoking": True},
]

safety_features_data = [
    {"PropertyID": 1, "FireExtinguisher": True, "SecurityCameras": True, "EmergencyExit": True},
    {"PropertyID": 2, "FireExtinguisher": False, "SecurityCameras": False, "EmergencyExit": True},
    {"PropertyID": 3, "FireExtinguisher": True, "SecurityCameras": True, "EmergencyExit": False},
]

moving_services_data = [
    {"Name": "QuickMove", "Phone": "555-1234", "Website": "https://quickmove.example.com"},
    {"Name": "Uhaul Bros", "Phone": "555-5678", "Website": "https://uhaulbros.example.com"},
    {"Name": "Campus Movers", "Phone": "555-9012", "Website": "https://campusmovers.example.com"},
]

# Insert data using SQLAlchemy session
with Session(engine) as session:
    session.add_all([RoommateSearch(**r) for r in roommate_data])
    session.add_all([SafetyFeatures(**s) for s in safety_features_data])
    session.add_all([MovingServices(**m) for m in moving_services_data])
    session.commit()

print("Dummy data inserted successfully.")
