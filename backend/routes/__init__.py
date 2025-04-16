from .user import user_bp
from .students import students_bp
from .landlords import landlords_bp
from .admin import admin_bp
from .property import property_bp
from .commute import commute_bp
from .message import message_bp
from .listings import list_bp
from .movingservices import movingservices_bp
from .safetyfeatures import safetyfeatures_bp
from .roommatesearch import roommatesearch_bp
from .amenities import amenities_bp
from .favorite import favorite_bp
from .leasetransfer import leasetransfer_bp
from .review import review_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(landlords_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(commute_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(list_bp)
    app.register_blueprint(movingservices_bp)
    app.register_blueprint(safetyfeatures_bp)
    app.register_blueprint(roommatesearch_bp)
    app.register_blueprint(amenities_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(leasetransfer_bp)
    app.register_blueprint(review_bp)
