from flask import Flask
from flask_cors import CORS
from routes import register_routes
from db import engine  # <- you now import engine from db.py (no circular import)
from models import Base

app = Flask(__name__)
CORS(app)

# Register all routes from /routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
