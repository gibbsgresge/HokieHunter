from typing import List, Optional
from sqlalchemy import Date, DateTime, Enum, Float, ForeignKeyConstraint, Index, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass

class LeaseTransfer(Base):
    __tablename__ = 'lease_transfer'
    lease_transfer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transfer_details: Mapped[Optional[str]] = mapped_column(Text)
    student_id: Mapped[Optional[int]] = mapped_column(Integer)
    property_id: Mapped[Optional[int]] = mapped_column(Integer)

class Property(Base):
    __tablename__ = 'property'
    PropertyID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Name: Mapped[Optional[str]] = mapped_column(String(100))
    Location: Mapped[Optional[str]] = mapped_column(String(255))
    Price: Mapped[Optional[str]] = mapped_column(String(50))
    RoomType: Mapped[Optional[str]] = mapped_column(String(50))

class RoommateSearch(Base):
    __tablename__ = 'roommate_search'
    roommate_search_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    preferences: Mapped[Optional[str]] = mapped_column(Text)
    student_id: Mapped[Optional[int]] = mapped_column(Integer)

class SafetyFeatures(Base):
    __tablename__ = 'safety_features'
    safety_feature_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feature_name: Mapped[Optional[str]] = mapped_column(String(100))
    property_id: Mapped[Optional[int]] = mapped_column(Integer)

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (Index('Email', 'Email', unique=True),)
    UserID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Email: Mapped[str] = mapped_column(String(100))
    Role: Mapped[str] = mapped_column(Enum('student', 'landlord', 'admin'))

class Admin(Users):
    __tablename__ = 'admin'
    __table_args__ = (
        ForeignKeyConstraint(['AdminID'], ['users.UserID'], name='admin_ibfk_1'),
    )
    AdminID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Permissions: Mapped[Optional[str]] = mapped_column(Text)

class Commute(Base):
    __tablename__ = 'commute'
    __table_args__ = (
        ForeignKeyConstraint(['PropertyID'], ['property.PropertyID'], name='commute_ibfk_1'),
        Index('PropertyID', 'PropertyID')
    )
    CommuteID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    Time: Mapped[Optional[int]] = mapped_column(Integer)
    Distance: Mapped[Optional[float]] = mapped_column(Float)
    ServiceID: Mapped[Optional[int]] = mapped_column(Integer)

class Landlords(Users):
    __tablename__ = 'landlords'
    __table_args__ = (
        ForeignKeyConstraint(['LandlordID'], ['users.UserID'], name='landlords_ibfk_1'),
    )
    LandlordID: Mapped[int] = mapped_column(Integer, primary_key=True)

class List(Base):
    __tablename__ = 'list'
    __table_args__ = (
        ForeignKeyConstraint(['PropertyID'], ['property.PropertyID'], name='list_ibfk_1'),
        Index('PropertyID', 'PropertyID')
    )
    ListID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    AvailableFrom: Mapped[Optional[datetime.date]] = mapped_column(Date)
    Status: Mapped[Optional[str]] = mapped_column(String(50))

class Message(Base):
    __tablename__ = 'message'
    __table_args__ = (
        ForeignKeyConstraint(['SenderID'], ['users.UserID'], name='message_ibfk_1'),
        Index('SenderID', 'SenderID')
    )
    MessageID: Mapped[int] = mapped_column(Integer, primary_key=True)
    SenderID: Mapped[Optional[int]] = mapped_column(Integer)
    Content: Mapped[Optional[str]] = mapped_column(Text)
    Timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

class Movingservices(Base):
    __tablename__ = 'movingservices'
    __table_args__ = (
        ForeignKeyConstraint(['PropertyID'], ['property.PropertyID'], name='movingservices_ibfk_1'),
        Index('PropertyID', 'PropertyID')
    )
    ServiceID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    CompanyName: Mapped[Optional[str]] = mapped_column(String(100))
    ContactInfo: Mapped[Optional[str]] = mapped_column(String(100))

class Safetyfeatures(Base):
    __tablename__ = 'safetyfeatures'
    __table_args__ = (
        ForeignKeyConstraint(['PropertyID'], ['property.PropertyID'], name='safetyfeatures_ibfk_1'),
        Index('PropertyID', 'PropertyID')
    )
    FeatureID: Mapped[int] = mapped_column(Integer, primary_key=True)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    FeatureDescription: Mapped[Optional[str]] = mapped_column(Text)

class Students(Users):
    __tablename__ = 'students'
    __table_args__ = (
        ForeignKeyConstraint(['StudentID'], ['users.UserID'], name='students_ibfk_1'),
    )
    StudentID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Major: Mapped[Optional[str]] = mapped_column(String(100))
    GraduationYear: Mapped[Optional[int]] = mapped_column(Integer)

class Amenities(Base):
    __tablename__ = 'amenities'
    __table_args__ = (
        ForeignKeyConstraint(['ListID'], ['list.ListID'], name='amenities_ibfk_1'),
        Index('ListID', 'ListID')
    )
    AmenityID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ListID: Mapped[Optional[int]] = mapped_column(Integer)
    Type: Mapped[Optional[str]] = mapped_column(String(100))

class Favorite(Base):
    __tablename__ = 'favorite'
    __table_args__ = (
        ForeignKeyConstraint(['PropertyID'], ['property.PropertyID'], name='favorite_ibfk_2'),
        ForeignKeyConstraint(['StudentID'], ['students.StudentID'], name='favorite_ibfk_1'),
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
        ForeignKeyConstraint(['PropertyID'], ['property.PropertyID'], name='leasetransfer_ibfk_2'),
        ForeignKeyConstraint(['StudentID'], ['students.StudentID'], name='leasetransfer_ibfk_1'),
        Index('PropertyID', 'PropertyID'),
        Index('StudentID', 'StudentID')
    )
    TransferID: Mapped[int] = mapped_column(Integer, primary_key=True)
    StudentID: Mapped[Optional[int]] = mapped_column(Integer)
    PropertyID: Mapped[Optional[int]] = mapped_column(Integer)
    LeaseEndDate: Mapped[Optional[datetime.date]] = mapped_column(Date)
    TransferStatus: Mapped[Optional[str]] = mapped_column(String(50))

class Review(Base):
    __tablename__ = 'review'
    __table_args__ = (
        ForeignKeyConstraint(['PropertyID'], ['property.PropertyID'], name='review_ibfk_2'),
        ForeignKeyConstraint(['StudentID'], ['students.StudentID'], name='review_ibfk_1'),
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
        ForeignKeyConstraint(['StudentID'], ['students.StudentID'], name='roommatesearch_ibfk_1'),
        Index('StudentID', 'StudentID')
    )
    SearchID: Mapped[int] = mapped_column(Integer, primary_key=True)
    StudentID: Mapped[Optional[int]] = mapped_column(Integer)
    Preferences: Mapped[Optional[str]] = mapped_column(Text)
