#!/usr/bin/python3
"""start app"""

from flask import Flask
app = Flask(__name__)

from models import staorage
from api.v1.views import app_views

app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_down(e):
    """Close the current session"""
    storage.close()

if __name__ == "__main__":
    app.run( 
            host=app.config.get('HBNB_API_HOST', '0.0.0.0'),
            port=int(app.config.get('HBNB_API_PORT', '5000')),
            threaded=True
            )
