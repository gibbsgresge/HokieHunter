from sqlalchemy.orm import Session
import sys
import os
import datetime

# 1) Ensure we can import db.py and models.py from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 2) Import the engine and models
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
    # 4) Clean existing data (in dependency order)
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

    # 5) Create sample users
    student_user = Students(
        Email='alice_student@example.com',
        Role='student',
        Username='alice123',
        PasswordHash='hashed_password_1',
        Major='Computer Science',
        GraduationYear=2026
    )

    landlord_user = Landlords(
        Email='bob_landlord@example.com',
        Role='landlord',
        Username='bob_landlord',
        PasswordHash='hashed_password_2'
    )

    admin_user = Admin(
        Email='charlie_admin@example.com',
        Role='admin',
        Username='charlie_admin',
        PasswordHash='hashed_password_3',
        Permissions='FULL_ACCESS'
    )

    session.add_all([student_user, landlord_user, admin_user])
    session.flush()  # Assign IDs

    # 6) Properties owned by landlord
    property1 = Property(
        LandlordID=landlord_user.LandlordID,
        Name='Hokie Heights',
        Location='Blacksburg',
        Price='1000',
        RoomType='Studio'
    )
    property2 = Property(
        LandlordID=landlord_user.LandlordID,
        Name='The Village',
        Location='Uptown',
        Price='1500',
        RoomType='2BR'
    )
    session.add_all([property1, property2])
    session.flush()

    # 7) Listings
    listing1 = List(
        PropertyID=property1.PropertyID,
        AvailableFrom=datetime.date.today(),
        Status='available'
    )
    listing2 = List(
        PropertyID=property2.PropertyID,
        AvailableFrom=datetime.date(2025, 5, 1),
        Status='pending'
    )
    session.add_all([listing1, listing2])
    session.flush()

    # 8) Reviews
    session.add_all([
        Review(StudentID=student_user.StudentID, PropertyID=property1.PropertyID, Rating=5, Comments='Great location and price!'),
        Review(StudentID=student_user.StudentID, PropertyID=property2.PropertyID, Rating=4, Comments='Nice place but a bit pricey')
    ])

    # 9) Favorite
    session.add(Favorite(
        StudentID=student_user.StudentID,
        PropertyID=property1.PropertyID,
        DateSaved=datetime.date.today(),
        Comments='I really like this place'
    ))

    # 10) Lease Transfer
    session.add(Leasetransfer(
        StudentID=student_user.StudentID,
        PropertyID=property1.PropertyID,
        LeaseEndDate=datetime.date(2026, 5, 31),
        TransferStatus='open'
    ))

    # 11) Commute
    session.add_all([
        Commute(PropertyID=property1.PropertyID, Time=15, Distance=3.2),
        Commute(PropertyID=property2.PropertyID, Time=25, Distance=6.7)
    ])

    # 12) Message
    session.add(Message(
        SenderID=student_user.UserID,
        Content='Is this still available?',
        Timestamp=datetime.datetime.now()
    ))

    # 13) Moving Services
    session.add(Movingservices(
        PropertyID=property1.PropertyID,
        CompanyName='Movers Inc',
        ContactInfo='555-1234'
    ))

    # 14) Safety Features
    session.add(Safetyfeatures(
        PropertyID=property1.PropertyID,
        FeatureDescription='Smoke Alarms'
    ))

    # 15) Amenities
    session.add_all([
        Amenities(ListID=listing1.ListID, Type='Pool'),
        Amenities(ListID=listing2.ListID, Type='Gym')
    ])

    # 16) Roommate Search
    session.add(Roommatesearch(
        StudentID=student_user.StudentID,
        Preferences='Non-smoker, quiet'
    ))

    # Final commit
    session.commit()

print("✅ Database seeded successfully with sample data for all tables!")
