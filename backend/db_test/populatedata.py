from sqlalchemy.orm import Session
import sys
import os
import datetime

# 1) Ensure we can import db.py and models.py from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 2) Import the engine from db.py and models from models.py
from db import engine
from models import (
    Base,
    # Parent + children
    Users, Students, Landlords, Admin,
    # Other tables
    Property, List, Favorite, Review, Commute, Message,
    Movingservices, Safetyfeatures, Amenities, Leasetransfer,
    Roommatesearch
)

# 3) Create/upgrade tables
Base.metadata.create_all(engine)

with Session(engine) as session:
    # ----------------------------------------------------------------------
    # 4) Clean out existing data to avoid duplicates
    #    We'll do it in dependency order to avoid foreign key constraint errors
    # ----------------------------------------------------------------------
    
    # Child tables that reference students or property
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

    # Since Students, Landlords, Admin all derive from Users, remove them first
    session.query(Students).delete()
    session.query(Landlords).delete()
    session.query(Admin).delete()

    # Lastly, clear the parent table
    session.query(Users).delete()
    session.commit()

    # ----------------------------------------------------------------------
    # 5) Insert sample data
    # ----------------------------------------------------------------------

    # --- A) CREATE USERS / CHILD TABLE ROWS ---
    # Student user
    student_user = Students(
        Email='alice_student@example.com',
        Role='student',  # matches 'polymorphic_identity' in Students
        Major='Computer Science',
        GraduationYear=2026
    )
    session.add(student_user)

    # Landlord user
    landlord_user = Landlords(
        Email='bob_landlord@example.com',
        Role='landlord'
    )
    session.add(landlord_user)

    # Admin user
    admin_user = Admin(
        Email='charlie_admin@example.com',
        Role='admin', 
        Permissions='FULL_ACCESS'
    )
    session.add(admin_user)

    # --- B) PROPERTIES ---
    property1 = Property(
        Name='Hokie Heights',
        Location='Blacksburg',
        Price='1000',
        RoomType='Studio'
    )
    session.add(property1)

    # Let’s also create a second property
    property2 = Property(
        Name='The Village',
        Location='Uptown',
        Price='1500',
        RoomType='2BR'
    )
    session.add(property2)

    # commit so property1.PropertyID and property2.PropertyID are generated
    session.commit()

    # --- C) LIST (LISTINGS) ---
    listing1 = List(
        PropertyID=property1.PropertyID,
        AvailableFrom=datetime.date.today(),
        Status='available'
    )
    session.add(listing1)

    listing2 = List(
        PropertyID=property2.PropertyID,
        AvailableFrom=datetime.date(2025, 5, 1),
        Status='pending'
    )
    session.add(listing2)

    # --- D) REVIEWS ---
    review1 = Review(
        StudentID=student_user.StudentID,
        PropertyID=property1.PropertyID,
        Rating=5,
        Comments='Great location and price!'
    )
    session.add(review1)

    review2 = Review(
        StudentID=student_user.StudentID,
        PropertyID=property2.PropertyID,
        Rating=4,
        Comments='Nice place but a bit pricey'
    )
    session.add(review2)

    # --- E) FAVORITE ---
    favorite1 = Favorite(
        StudentID=student_user.StudentID,
        PropertyID=property1.PropertyID,
        DateSaved=datetime.date.today(),
        Comments='I really like this place'
    )
    session.add(favorite1)

    # --- F) LEASETRANSFER ---
    lease1 = Leasetransfer(
        StudentID=student_user.StudentID,
        PropertyID=property1.PropertyID,
        LeaseEndDate=datetime.date(2026, 5, 31),
        TransferStatus='open'
    )
    session.add(lease1)

    # --- G) COMMUTE ---
    commute1 = Commute(
        PropertyID=property1.PropertyID,
        Time=15,
        Distance=3.2,
        ServiceID=None
    )
    session.add(commute1)

    # Also a commute for property2
    commute2 = Commute(
        PropertyID=property2.PropertyID,
        Time=25,
        Distance=6.7
    )
    session.add(commute2)

    # --- H) MESSAGE ---
    # Let’s say the student sends a message
    message1 = Message(
        SenderID=student_user.UserID,  # not StudentID but UserID 
        Content='Is this still available?',
        Timestamp=datetime.datetime.now()
    )
    session.add(message1)

    # --- I) MOVINGSERVICES ---
    moving1 = Movingservices(
        PropertyID=property1.PropertyID,
        CompanyName='Movers Inc',
        ContactInfo='555-1234'
    )
    session.add(moving1)

    # --- J) SAFETYFEATURES ---
    safety1 = Safetyfeatures(
        PropertyID=property1.PropertyID,
        FeatureDescription='Smoke Alarms'
    )
    session.add(safety1)

    # --- K) AMENITIES ---
    # We reference the listing, not the property directly
    amenity1 = Amenities(
        ListID=listing1.ListID,
        Type='Pool'
    )
    session.add(amenity1)

    # Another amenity for listing2
    amenity2 = Amenities(
        ListID=listing2.ListID,
        Type='Gym'
    )
    session.add(amenity2)

    # --- L) ROOMMATESEARCH ---
    roommate1 = Roommatesearch(
        StudentID=student_user.StudentID,
        Preferences='Non-smoker, quiet'
    )
    session.add(roommate1)

    # Final commit for all
    session.commit()

print("✅ Database seeded successfully with sample data for all tables!")
