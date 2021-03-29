import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from beerlin import app, db, bcrypt
from beerlin.models import User, Local
from flask_login import login_user, current_user, logout_user, login_required



main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home(): 
      return render_template(
        'home.html', 
        map_key=app.config['GOOGLE_MAPS_API_KEY'],
        profiles=[]
    )



