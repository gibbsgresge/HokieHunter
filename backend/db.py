# db.py
from sqlalchemy import create_engine
from models import Base

DATABASE_URI = 'mysql+pymysql://root:Root123!@localhost:3306/workbenchdb'
engine = create_engine(DATABASE_URI, echo = False)
Base.metadata.bind = engine
