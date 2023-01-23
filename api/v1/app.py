#!/usr/bin/python3

"""Endpoint (route) will be to return the status of Api"""
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import *
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """closes the current sqlalchemy session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    Create a handler for 404 errors that returns a
    JSON-formatted 404 status code response
    """
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or '5000'
    app.run(host=host, port=port, threaded=True)
