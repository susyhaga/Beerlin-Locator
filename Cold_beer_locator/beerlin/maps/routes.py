import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from beerlin import app, db, bcrypt
from beerlin.models import User, Local
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from flask import jsonify

maps = Blueprint('maps', __name__)

@ maps.route("/map")
def map():
    local = Local.query.all()
    print(local)
    return render_template('map.html', title='Map', local=local)


# JSON Api routes
# ----------------
@maps.route("/api/get_stores_in_radius")
def get_stores_in_radius():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('lng'))
    radius = int(request.args.get('radius'))

    # TODO: Validate the input? 

    stores = Local.get_stores_within_radius(lat=latitude, lng=longitude, radius=radius)
   
    result = []
    for s in stores:
        result.append(s.toDict())
        
    return jsonify(result)