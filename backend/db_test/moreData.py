from sqlalchemy import create_engine, text
from datetime import date
import random

# ✅ Replace with your MySQL credentials
DB_URI = "mysql+pymysql://root:Root123!@localhost:3306/workbenchdb"

engine = create_engine(DB_URI)

def get_next_id(conn, table, id_col):
    """Return the next available ID for a table."""
    result = conn.execute(text(f"SELECT MAX({id_col}) FROM {table}"))
    max_id = result.scalar()
    return (max_id or 0) + 1

with engine.begin() as conn:
    print("Connected to DB. Inserting sample data...\n")

    # === USERS ===
    roles = ['student'] * 10 + ['landlord'] * 5 + ['admin'] * 5
    user_start_id = get_next_id(conn, "users", "UserID")
    user_sql = "INSERT INTO users (UserID, Email, Role) VALUES (:id, :email, :role)"

    student_users = []
    landlord_users = []
    admin_users = []

    for i, role in enumerate(roles):
        user_id = user_start_id + i
        conn.execute(text(user_sql), {
            'id': user_id,
            'email': f'user{user_id}@example.com',
            'role': role
        })
        if role == "student":
            student_users.append(user_id)
        elif role == "landlord":
            landlord_users.append(user_id)
        elif role == "admin":
            admin_users.append(user_id)

    # === STUDENTS ===
    student_start_id = get_next_id(conn, "students", "StudentID")
    student_sql = "INSERT INTO students (StudentID, Major, GraduationYear) VALUES (:id, :major, :year)"
    majors = ['CS', 'Biology', 'Economics', 'Math', 'History']

    for i, uid in enumerate(student_users[:5]):
        conn.execute(text(student_sql), {
            'id': uid,
            'major': majors[i % len(majors)],
            'year': random.choice([2024, 2025, 2026])
        })

    # === LANDLORDS ===
    landlord_sql = "INSERT INTO landlords (LandlordID) VALUES (:id)"
    for uid in landlord_users[:5]:
        conn.execute(text(landlord_sql), {'id': uid})

    # === ADMIN ===
    admin_sql = "INSERT INTO admin (AdminID, Permissions) VALUES (:id, :perm)"
    for uid in admin_users[:3]:
        conn.execute(text(admin_sql), {'id': uid, 'perm': 'all'})

    # === PROPERTIES ===
    prop_start_id = get_next_id(conn, "property", "PropertyID")
    prop_sql = """
    INSERT INTO property (PropertyID, Name, Location, Price, RoomType)
    VALUES (:id, :name, :location, :price, :room)
    """
    for i in range(20):
        pid = prop_start_id + i
        conn.execute(text(prop_sql), {
            'id': pid,
            'name': f'Hokie House {pid}',
            'location': f'{100 + pid} Main St',
            'price': str(1000 + i * 25),
            'room': random.choice(['1B1B', '2B2B', '3B2B'])
        })

    # === REVIEWS ===
    review_start_id = get_next_id(conn, "review", "ReviewID")
    review_sql = """
    INSERT INTO review (ReviewID, StudentID, PropertyID, Rating, Comments)
    VALUES (:id, :student_id, :property_id, :rating, :comments)
    """
    for i in range(5):
        conn.execute(text(review_sql), {
            'id': review_start_id + i,
            'student_id': student_users[i],
            'property_id': prop_start_id + i,
            'rating': random.randint(3, 5),
            'comments': f'Review for property {prop_start_id + i}'
        })

    # === FAVORITES ===
    fav_start_id = get_next_id(conn, "favorite", "FavoriteID")
    fav_sql = """
    INSERT INTO favorite (FavoriteID, StudentID, PropertyID, DateSaved, Comments)
    VALUES (:id, :student_id, :property_id, :date_saved, :comments)
    """
    for i in range(5):
        conn.execute(text(fav_sql), {
            'id': fav_start_id + i,
            'student_id': student_users[i],
            'property_id': prop_start_id + i,
            'date_saved': date.today().isoformat(),
            'comments': f'Favorite property {prop_start_id + i}'
        })

    # === LEASE TRANSFERS ===
    lease_start_id = get_next_id(conn, "leasetransfer", "TransferID")
    lease_sql = """
    INSERT INTO leasetransfer (TransferID, StudentID, PropertyID, LeaseEndDate, TransferStatus)
    VALUES (:id, :student_id, :property_id, :lease_end, :status)
    """
    for i in range(5):
        conn.execute(text(lease_sql), {
            'id': lease_start_id + i,
            'student_id': student_users[i],
            'property_id': prop_start_id + i,
            'lease_end': date(2025, 5, 31).isoformat(),
            'status': random.choice(['Open', 'Pending'])
        })

    print("✅ Sample data inserted safely without duplicate IDs.")
