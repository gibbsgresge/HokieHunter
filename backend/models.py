from typing import Optional
from sqlalchemy import (
    Date, DateTime, Enum, Float, ForeignKey, ForeignKeyConstraint,
    Index, Integer, String, Text
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass

# ----------------------------------------------------------------------
# 1) USERS PARENT TABLE (Joined Inheritance)
# ----------------------------------------------------------------------
class Users(Base):
    __tablename__ = 'users'
    

    UserID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Email: Mapped[str] = mapped_column(String(100), nullable=False)
    Role: Mapped[str] = mapped_column(Enum('student', 'landlord', 'admin'), nullable=False)
    Username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    PasswordHash: Mapped[str] = mapped_column(Text, nullable=False)


    __mapper_args__ = {
        'polymorphic_on': Role,
        'polymorphic_identity': 'user'
    }

# ----------------------------------------------------------------------
# 2) CHILD CLASSES
#    "ondelete='CASCADE'" can be used if you want removing a Users row
#    to automatically remove the child row. This is optional in joined
#    inheritance, but shown for completeness.
# ----------------------------------------------------------------------

class Admin(Users):
    __tablename__ = 'admin'
    __table_args__ = (
        ForeignKeyConstraint(
            ['AdminID'], 
            ['users.UserID'],
            ondelete='CASCADE',  # If removing the parent user => remove Admin row
            name='admin_ibfk_1'
        ),
    )
    AdminID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Permissions: Mapped[Optional[str]] = mapped_column(Text)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

class Landlords(Users):
    __tablename__ = 'landlords'
    __table_args__ = (
        ForeignKeyConstraint(
            ['LandlordID'],
            ['users.UserID'],
            ondelete='CASCADE',
            name='landlords_ibfk_1'
        ),
    )
    LandlordID: Mapped[int] = mapped_column(Integer, primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'landlord'
    }


class Students(Users):
    __tablename__ = 'students'
    __table_args__ = (
        ForeignKeyConstraint(
            ['StudentID'],
            ['users.UserID'],
            ondelete='CASCADE',  # If removing user => remove Student row
            name='students_ibfk_1'
        ),
    )
    StudentID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Major: Mapped[Optional[str]] = mapped_column(String(100))
    GraduationYear: Mapped[Optional[int]] = mapped_column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

# ----------------------------------------------------------------------
# 3) PROPERTY TABLE
# ----------------------------------------------------------------------
class Property(Base):
    __tablename__ = 'property'
    PropertyID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LandlordID: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('landlords.LandlordID', ondelete='CASCADE'),
        nullable=False
    )
    Name: Mapped[Optional[str]] = mapped_column(String(100))
    Location: Mapped[Optional[str]] = mapped_column(String(255))
    Price: Mapped[Optional[str]] = mapped_column(String(50))
    RoomType: Mapped[Optional[str]] = mapped_column(String(50))




# ----------------------------------------------------------------------
# 4) TABLES REFERENCING STUDENTS OR PROPERTY, ETC.
#    We'll add "ondelete='CASCADE'" so that removing the parent row
#    automatically removes dependent rows.
# ----------------------------------------------------------------------

class Commute(Base):
    __tablename__ = 'commute'
    __table_args__ = (
        ForeignKeyConstraint(
            ['PropertyID'], 
            ['property.PropertyID'],
            ondelete='CASCADE',
            name='commute_ibfk_1'
        ),
        Index('PropertyID', 'PropertyID')
    )
    CommuteID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    Time: Mapped[Optional[int]] = mapped_column(Integer)
    Distance: Mapped[Optional[float]] = mapped_column(Float)
    ServiceID: Mapped[Optional[int]] = mapped_column(Integer)

class List(Base):
    __tablename__ = 'list'
    __table_args__ = (
        ForeignKeyConstraint(
            ['PropertyID'], 
            ['property.PropertyID'],
            ondelete='CASCADE',
            name='list_ibfk_1'
        ),
        Index('PropertyID', 'PropertyID')
    )
    ListID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    AvailableFrom: Mapped[Optional[datetime.date]] = mapped_column(Date)
    Status: Mapped[Optional[str]] = mapped_column(String(50))

class Message(Base):
    __tablename__ = 'message'
    __table_args__ = (
        ForeignKeyConstraint(
            ['SenderID'], 
            ['users.UserID'],
            ondelete='CASCADE', 
            name='message_ibfk_1'
        ),
        Index('SenderID', 'SenderID')
    )
    MessageID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SenderID: Mapped[Optional[int]] = mapped_column(Integer)
    Content: Mapped[Optional[str]] = mapped_column(Text)
    Timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

class Movingservices(Base):
    __tablename__ = 'movingservices'
    __table_args__ = (
        ForeignKeyConstraint(
            ['PropertyID'],
            ['property.PropertyID'],
            ondelete='CASCADE',
            name='movingservices_ibfk_1'
        ),
        Index('PropertyID', 'PropertyID')
    )
    ServiceID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    CompanyName: Mapped[Optional[str]] = mapped_column(String(100))
    ContactInfo: Mapped[Optional[str]] = mapped_column(String(100))

class Safetyfeatures(Base):
    __tablename__ = 'safetyfeatures'
    __table_args__ = (
        ForeignKeyConstraint(
            ['PropertyID'],
            ['property.PropertyID'],
            ondelete='CASCADE',
            name='safetyfeatures_ibfk_1'
        ),
        Index('PropertyID', 'PropertyID')
    )
    FeatureID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    FeatureDescription: Mapped[Optional[str]] = mapped_column(Text)

class Amenities(Base):
    __tablename__ = 'amenities'
    __table_args__ = (
        ForeignKeyConstraint(
            ['PropertyID'],
            ['property.PropertyID'],
            ondelete='CASCADE',
            name='amenities_ibfk_1'
        ),
        Index('PropertyID', 'PropertyID')
    )
    AmenityID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PropertyID: Mapped[int] = mapped_column(Integer, nullable=False)
    Type: Mapped[Optional[str]] = mapped_column(String(100))


class Favorite(Base):
    __tablename__ = 'favorite'
    __table_args__ = (
        ForeignKeyConstraint(
            ['PropertyID'],
            ['property.PropertyID'],
            ondelete='CASCADE',
            name='favorite_ibfk_2'
        ),
        ForeignKeyConstraint(
            ['StudentID'],
            ['students.StudentID'],
            ondelete='CASCADE',
            name='favorite_ibfk_1'
        ),
        Index('PropertyID', 'PropertyID'),
        Index('StudentID', 'StudentID')
    )
    FavoriteID: Mapped[int] = mapped_column(Integer, primary_key=True)
    StudentID: Mapped[Optional[int]] = mapped_column(Integer)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    DateSaved: Mapped[Optional[datetime.date]] = mapped_column(Date)
    Comments: Mapped[Optional[str]] = mapped_column(Text)

class Leasetransfer(Base):
    __tablename__ = 'leasetransfer'
    __table_args__ = (
        ForeignKeyConstraint(
            ['PropertyID'],
            ['property.PropertyID'],
            ondelete='CASCADE',
            name='leasetransfer_ibfk_2'
        ),
        ForeignKeyConstraint(
            ['StudentID'],
            ['students.StudentID'],
            ondelete='CASCADE',
            name='leasetransfer_ibfk_1'
        ),
        Index('PropertyID', 'PropertyID'),
        Index('StudentID', 'StudentID')
    )
    TransferID: Mapped[int] = mapped_column(Integer, primary_key=True)
    StudentID: Mapped[Optional[int]] = mapped_column(Integer)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    LeaseEndDate: Mapped[Optional[str]] = mapped_column(String(40))
    TransferStatus: Mapped[Optional[str]] = mapped_column(String(50))

class Review(Base):
    __tablename__ = 'review'
    __table_args__ = (
        ForeignKeyConstraint(
            ['PropertyID'],
            ['property.PropertyID'],
            ondelete='CASCADE',
            name='review_ibfk_2'
        ),
        ForeignKeyConstraint(
            ['StudentID'],
            ['students.StudentID'],
            ondelete='CASCADE',
            name='review_ibfk_1'
        ),
        Index('PropertyID', 'PropertyID'),
        Index('StudentID', 'StudentID')
    )
    ReviewID: Mapped[int] = mapped_column(Integer, primary_key=True)
    StudentID: Mapped[Optional[int]] = mapped_column(Integer)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    Rating: Mapped[Optional[int]] = mapped_column(Integer)
    Comments: Mapped[Optional[str]] = mapped_column(Text)

class Roommatesearch(Base):
    __tablename__ = 'roommatesearch'
    __table_args__ = (
        ForeignKeyConstraint(
            ['StudentID'],
            ['students.StudentID'],
            ondelete='CASCADE',
            name='roommatesearch_ibfk_1'
        ),
        Index('StudentID', 'StudentID')
    )
    SearchID: Mapped[int] = mapped_column(Integer, primary_key=True)
    StudentID: Mapped[Optional[int]] = mapped_column(Integer)
    Preferences: Mapped[Optional[str]] = mapped_column(Text)
