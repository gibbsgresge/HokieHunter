# save this as populate_data.py or similar
from sqlalchemy.orm import Session
from faker import Faker
import datetime
import random
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import engine
from models import (
    Base, Users, Students, Landlords, Admin,
    Property, List, Favorite, Review, Commute, Message,
    Movingservices, Safetyfeatures, Amenities, Leasetransfer,
    Roommatesearch
)

fake = Faker()
Base.metadata.create_all(engine)

with Session(engine) as session:
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

    students, landlords, admins = [], [], []

    for _ in range(20):
        students.append(Students(
            Email=fake.email(),
            Role='student',
            Username=fake.user_name(),
            PasswordHash=fake.sha256(),
            Major=fake.job(),
            GraduationYear=random.randint(2025, 2030)
        ))

        landlords.append(Landlords(
            Email=fake.email(),
            Role='landlord',
            Username=fake.user_name(),
            PasswordHash=fake.sha256()
        ))

        admins.append(Admin(
            Email=fake.email(),
            Role='admin',
            Username=fake.user_name(),
            PasswordHash=fake.sha256(),
            Permissions='ALL'
        ))

    session.add_all(students + landlords + admins)
    session.flush()

    properties = []
    for i in range(20):
        landlord = random.choice(landlords)
        prop = Property(
            LandlordID=landlord.LandlordID,
            Name=fake.company(),
            Location=fake.address(),
            Price=str(random.randint(800, 2000)),
            RoomType=random.choice(['Studio', '1BR', '2BR', 'Shared'])
        )
        properties.append(prop)
    session.add_all(properties)
    session.flush()

    lists, commutes, messages, movings, safety, amenities = [], [], [], [], [], []
    favorites, leases, reviews, roommate_searches = [], [], [], []

    for prop in properties:
        lists.append(List(
            PropertyID=prop.PropertyID,
            AvailableFrom=fake.date_this_year(),
            Status=random.choice(['available', 'occupied'])
        ))

        commutes.append(Commute(
            PropertyID=prop.PropertyID,
            Time=random.randint(5, 30),
            Distance=round(random.uniform(1.0, 10.0), 2),
            ServiceID=random.randint(1, 100)
        ))

        movings.append(Movingservices(
            PropertyID=prop.PropertyID,
            CompanyName=fake.company(),
            ContactInfo=fake.phone_number()
        ))

        safety.append(Safetyfeatures(
            PropertyID=prop.PropertyID,
            FeatureDescription=random.choice(['CCTV', 'Fire Extinguisher', 'Emergency Exit', 'Smoke Detector'])
        ))

        amenities.append(Amenities(
            PropertyID=prop.PropertyID,
            Type=random.choice(['WiFi', 'Pool', 'Gym', 'Laundry'])
        ))

    for student in students:
        messages.append(Message(
            SenderID=student.UserID,
            Content=fake.sentence(),
            Timestamp=datetime.datetime.now()
        ))

        roommate_searches.append(Roommatesearch(
            StudentID=student.StudentID,
            Preferences=fake.text(max_nb_chars=100)
        ))

        for _ in range(1):  # 1 of each per student
            p = random.choice(properties)
            favorites.append(Favorite(
                StudentID=student.StudentID,
                PropertyID=p.PropertyID,
                DateSaved=fake.date_this_year(),
                Comments=fake.text(max_nb_chars=100)
            ))

            leases.append(Leasetransfer(
                StudentID=student.StudentID,
                PropertyID=p.PropertyID,
                LeaseEndDate=fake.date_between(start_date='+1y', end_date='+2y').isoformat(),
                TransferStatus=random.choice(['open', 'pending', 'closed'])
            ))

            reviews.append(Review(
                StudentID=student.StudentID,
                PropertyID=p.PropertyID,
                Rating=random.randint(1, 5),
                Comments=fake.text(max_nb_chars=150)
            ))

    session.add_all(lists + commutes + messages + movings + safety + amenities +
                    favorites + leases + reviews + roommate_searches)
    session.commit()
    print("✅ 20 entries per table inserted.")
