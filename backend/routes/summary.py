from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Float
from db import engine
from models import Users, Students, Landlords, Admin, Property, Commute

summary_bp = Blueprint('summary_bp', __name__)

@summary_bp.route('/summary', methods=['GET'])
def get_summary():
    with Session(engine) as session:
        return jsonify({
            "Total Users": session.query(Users).count(),
            "Students": session.query(Students).count(),
            "Landlords": session.query(Landlords).count(),
            "Admins": session.query(Admin).count(),
            "Total Listings": session.query(Property).count(),
            "Avg Listing Price": session.query(func.avg(cast(Property.Price, Float))).scalar(),
            "Avg Commute Time": session.query(func.avg(Commute.Time)).scalar(),
            "Most Common Room Type": session.query(
                Property.RoomType, func.count()
            ).group_by(Property.RoomType).order_by(func.count().desc()).first()[0]
        })

@summary_bp.route('/landlord-stats', methods=['GET'])
def landlord_stats():
    with Session(engine) as session:
        total_properties = session.query(Property).count()
        landlords = session.query(
            Landlords.Username,
            func.avg(cast(Property.Price, Float)).label('avg_price'),
            func.count(Property.PropertyID).label('property_count')
        ).join(Property).group_by(Landlords.LandlordID).all()

        return jsonify([
            {
                "name": name,
                "avg_price": avg_price,
                "percentage_owned": (count / total_properties) * 100
            } for name, avg_price, count in landlords
        ])

@summary_bp.route('/student-stats', methods=['GET'])
def student_stats():
    with Session(engine) as session:
        total = session.query(Students).count()

        by_major = session.query(
            Students.Major,
            func.count().label('count')
        ).group_by(Students.Major).all()

        by_year = session.query(
            Students.GraduationYear,
            func.count().label('count')
        ).group_by(Students.GraduationYear).all()

        return jsonify({
            "by_major": [
                {"major": major, "percent": count / total * 100} for major, count in by_major
            ],
            "by_graduation_year": [
                {"grad_year": year, "percent": count / total * 100} for year, count in by_year
            ]
        })