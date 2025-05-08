import mysql.connector
import random
from datetime import datetime, timedelta

def random_date(start_days_ago=100):
    return datetime.now() - timedelta(days=random.randint(0, start_days_ago))

def populate_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Root123!',
        database='testHokieHunter'
    )
    cursor = conn.cursor()

    # USERS
    users = [
        ('alice', 'alice@example.com', 'hash1', 'student'),
        ('bob', 'bob@example.com', 'hash2', 'landlord'),
        ('carol', 'carol@example.com', 'hash3', 'admin'),
        ('dave', 'dave@example.com', 'hash4', 'student'),
        ('eve', 'eve@example.com', 'hash5', 'landlord')
    ]
    cursor.executemany("INSERT INTO users (Username, Email, PasswordHash, Role) VALUES (%s, %s, %s, %s)", users)

    # STUDENTS
    cursor.executemany("INSERT INTO students (StudentID, Major, GraduationYear) VALUES (%s, %s, %s)", [
        (1, 'Computer Science', 2025),
        (4, 'Business', 2026)
    ])

    # LANDLORDS
    cursor.executemany("INSERT INTO landlords (LandlordID) VALUES (%s)", [
        (2,),
        (5,)
    ])

    # ADMINS
    cursor.execute("INSERT INTO admin (AdminID, Permissions) VALUES (%s, %s)", (3, 'ALL'))

    # PROPERTIES
    cursor.executemany("INSERT INTO property (Name, Location, Price, RoomType, LandlordID) VALUES (%s, %s, %s, %s, %s)", [
        ('Oakridge Apartments', '123 Main St', '$1000', 'Studio', 2),
        ('Maple Hall', '456 College Ave', '$1200', '1BR', 5)
    ])

    # AMENITIES
    cursor.executemany("INSERT INTO amenities (PropertyID, Type) VALUES (%s, %s)", [
        (1, 'Wi-Fi'),
        (1, 'Gym'),
        (2, 'Laundry')
    ])

    # COMMUTE
    cursor.executemany("INSERT INTO commute (PropertyID, Time, Distance, ServiceID) VALUES (%s, %s, %s, %s)", [
        (1, 15, 2.5, 1),
        (2, 10, 1.0, 2)
    ])

    # MOVING SERVICES
    cursor.executemany("INSERT INTO movingservices (PropertyID, CompanyName, ContactInfo) VALUES (%s, %s, %s)", [
        (1, 'MovePro', '555-1111'),
        (2, 'QuickMove', '555-2222')
    ])

    # LISTINGS
    cursor.executemany("INSERT INTO list (PropertyID, AvailableFrom, Status) VALUES (%s, %s, %s)", [
        (1, random_date().date(), 'Available'),
        (2, random_date().date(), 'Unavailable')
    ])

    # FAVORITES
    cursor.executemany("INSERT INTO favorite (StudentID, PropertyID, DateSaved, Comments) VALUES (%s, %s, %s, %s)", [
        (1, 1, random_date().date(), 'Love it!'),
        (4, 2, random_date().date(), 'Too far')
    ])

    # LEASE TRANSFERS
    cursor.executemany("INSERT INTO leasetransfer (StudentID, PropertyID, LeaseEndDate, TransferStatus) VALUES (%s, %s, %s, %s)", [
        (1, 1, '2025-05-30', 'Pending'),
        (4, 2, '2026-01-15', 'Complete')
    ])

    # REVIEWS
    cursor.executemany("INSERT INTO review (StudentID, PropertyID, Rating, Comments) VALUES (%s, %s, %s, %s)", [
        (1, 1, 5, 'Great place!'),
        (4, 2, 3, 'Okay spot.')
    ])

    # ROOMMATE SEARCH
    cursor.executemany("INSERT INTO roommatesearch (StudentID, Preferences) VALUES (%s, %s)", [
        (1, 'Quiet, no pets'),
        (4, 'Night owl, gamer')
    ])

    # SAFETY FEATURES
    cursor.executemany("INSERT INTO safetyfeatures (PropertyID, FeatureDescription) VALUES (%s, %s)", [
        (1, 'Gated entry'),
        (2, 'Security cameras')
    ])

    # MESSAGES
    cursor.executemany("INSERT INTO message (SenderID, Content, Timestamp) VALUES (%s, %s, %s)", [
        (1, 'Hey, interested in the listing?', datetime.now()),
        (2, 'Sure, let’s talk!', datetime.now())
    ])

    conn.commit()
    cursor.close()
    conn.close()
    print("Database populated successfully.")

if __name__ == "__main__":
    populate_db()
