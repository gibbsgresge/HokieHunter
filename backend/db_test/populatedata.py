from sqlalchemy.orm import Session
import sys
import os
import datetime

# 1) Ensure we can import db.py and models.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 2) Import engine and models
from db import engine
from models import (
    Base,
    Users, Students, Landlords, Admin,
    Property, List, Favorite, Review, Commute, Message,
    Movingservices, Safetyfeatures, Amenities, Leasetransfer,
    Roommatesearch
)

# 3) Create tables
Base.metadata.create_all(engine)

with Session(engine) as session:
    # 4) Clear existing data (order matters due to foreign keys)
    session.query(Amenities).delete()
    session.query(Commute).delete()
    session.query(Leasetransfer).delete()
    session.query(Favorite).delete()
    session.query(Review).delete()
    session.query(Message).delete()
    session.query(Movingservices).delete()
    session.query(Safetyfeatures).delete()
    session.query(Roommatesearch).delete()
    session.query(List).delete()
    session.query(Property).delete()
    session.query(Students).delete()
    session.query(Landlords).delete()
    session.query(Admin).delete()
    session.query(Users).delete()
    session.commit()

    # 5) Create users
    student = Students(
        Email='student@example.com',
        Role='student',
        Username='studuser',
        PasswordHash='hash123',
        Major='Engineering',
        GraduationYear=2026
    )
    landlord = Landlords(
        Email='landlord@example.com',
        Role='landlord',
        Username='landy',
        PasswordHash='hash456'
    )
    admin = Admin(
        Email='admin@example.com',
        Role='admin',
        Username='adminy',
        PasswordHash='hash789',
        Permissions='ALL'
    )
    session.add_all([student, landlord, admin])
    session.flush()

    # 6) Properties
    prop = Property(
        LandlordID=landlord.LandlordID,
        Name='Sunset Villas',
        Location='Downtown',
        Price='1200',
        RoomType='1BR'
    )
    session.add(prop)
    session.flush()

    # 7) List
    listing = List(
        PropertyID=prop.PropertyID,
        AvailableFrom=datetime.date.today(),
        Status='available'
    )
    session.add(listing)
    session.flush()

    # 8) Commute
    session.add(Commute(
        PropertyID=prop.PropertyID,
        Time=10,
        Distance=2.5,
        ServiceID=None
    ))

    # 9) Message
    session.add(Message(
        SenderID=student.UserID,
        Content="Is this property pet-friendly?",
        Timestamp=datetime.datetime.now()
    ))

    # 10) Moving Service
    session.add(Movingservices(
        PropertyID=prop.PropertyID,
        CompanyName='MoveXpress',
        ContactInfo='123-456-7890'
    ))

    # 11) Safety Feature
    session.add(Safetyfeatures(
        PropertyID=prop.PropertyID,
        FeatureDescription='Fire Extinguisher'
    ))

    # 12) Amenities
    session.add(Amenities(
        PropertyID=prop.PropertyID,
        Type='WiFi'
    ))

    # 13) Favorite
    session.add(Favorite(
        StudentID=student.StudentID,
        PropertyID=prop.PropertyID,
        DateSaved=datetime.date.today(),
        Comments='Seems quiet and close to campus'
    ))

    # 14) Lease Transfer
    session.add(Leasetransfer(
        StudentID=student.StudentID,
        PropertyID=prop.PropertyID,
        LeaseEndDate='2026-06-30',
        TransferStatus='open'
    ))

    # 15) Review
    session.add(Review(
        StudentID=student.StudentID,
        PropertyID=prop.PropertyID,
        Rating=5,
        Comments='Loved the natural lighting and modern kitchen'
    ))

    # 16) Roommate Search
    session.add(Roommatesearch(
        StudentID=student.StudentID,
        Preferences='No smoking, early riser'
    ))

    session.commit()

print("✅ Sample data inserted into all tables.")
