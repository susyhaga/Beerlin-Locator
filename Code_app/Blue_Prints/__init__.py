from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy import event
from sqlalchemy.sql import select, func
from flask_mail import Mail



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['GOOGLE_MAPS_API_KEY'] = 'AIzaSyBMd_Sabn9rfbMx7e9157nDFToMcTQAwvo' 


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

from beerlin.users.routes import users
from beerlin.maps.routes import maps
from beerlin.main.routes import main
app.register_blueprint(users)
app.register_blueprint(maps)
app.register_blueprint(main)





@event.listens_for(db.engine, "connect")    
def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')

engine = create_engine('sqlite:///gis.db', echo=True)
listen(engine, 'connect', load_spatialite)






