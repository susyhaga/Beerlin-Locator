from datetime import datetime
from beerlin import db, login_manager
from flask_login import UserMixin
from sqlalchemy import func, ForeignKeyConstraint, text
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement
import json



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# test_table = db.Table('test_table', db.Model.metadata,
#     db.Column('left_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('right_id', db.Integer, db.ForeignKey('post.id'))
# )


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #posts = db.relationship('Post', foreign_keys='[post.id]',backref='author', lazy=True)

    def __repr__(self):
        return f"{self.id}"

    def user_list():

        sql = text('select id, username from users order by id asc')
        result = db.engine.execute(sql)
        return_Id = []
        return_username = []
        for r in result:
            #print(r[0]) # Access by positional index
            return_Id.append(str(r[0]))
            #print(r['ranking']) # Access by column name as a string
            return_username.append(str(r[1]))
        
        return_final = list(zip(return_Id,return_username))

        #return r_dict
        return return_final

class SpatialConstants:
    # SRID stands for Spatial Reference ID, some explanation of why we need one here: 
    # https://www.gaia-gis.it/gaia-sins/spatialite-cookbook/html/srid.html
    SRID = 4326

class Local(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    location = db.Column(Geometry("POINT", srid=SpatialConstants.SRID, dimension=2, management=True)) 
    name = db.Column(db.String(20), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)


    def get_location_latitude(self):
        point = to_shape(self.location)
        return point.y

    def get_location_longitude(self):
        point = to_shape(self.location)
        return point.x  


    def __repr__(self):
        return f"['{self.name}', {self.latitude}, {self.longitude}]"


    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'location': {
                'lng': self.get_location_longitude(),
                'lat': self.get_location_latitude()
            },
        }  

    def toRankDict(self):
        return self.id


    @staticmethod
    def get_stores_within_radius(lat, lng, radius):
        """Return all stores within a given radius (in meters)"""
        return Local.query.filter(
            func.PtDistWithin(
                Local.location, 
                func.MakePoint(lng, lat, SpatialConstants.SRID), 
                radius)
            ).limit(10).all() #TODO: do I need to limit?

    @staticmethod
    def point_representation(latitude, longitude):
        point = 'POINT(%s %s)' % (longitude, latitude)
        wkb_element = WKTElement(point, srid=SpatialConstants.SRID)
        return wkb_element

    def store_list():

        sql = text('select id, name from store order by id asc')
        result = db.engine.execute(sql)
        return_storeId = []
        return_storeName = []
        for r in result:
            #print(r[0]) # Access by positional index
            return_storeId.append(str(r[0]))
            #print(r['ranking']) # Access by column name as a string
            return_storeName.append(str(r[1]))
        
        return_final = list(zip(return_storeId,return_storeName))

        #return r_dict
        return return_final


class Ranking(db.Model):
    __tablename__ = 'ranking'

    id = db.Column(db.Integer, primary_key=True)
    beercode = db.Column(db.Integer, nullable=False)
    beerbrand = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    ranking = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    def __repr__(self):
        return f"['{self.store_id}', '{self.place}', '{self.beerbrand}', {self.ranking}]"

    @staticmethod
    def values_ranking(result_raking):
        result_final = []
        result_final.append(Ranking.query.filter(Ranking.store_id == result_raking).limit(10).all())

        return result_final

    def toDictfromRank(self):
        return {
            'store_id': self.store_id,
            'place': self.place,
            'beerbrand': self.beerbrand,
            'ranking': self.ranking,
        }  
    
    def beer_rank(store):
        store_id = store
        sql = text('select beerbrand, round(avg(ranking),2) ranking from ranking where store_id = :value group by beerbrand order by ranking desc')
        result = db.engine.execute(sql, value = store_id)
        return_beerbrand = []
        return_ranking = []
        for r in result:
            #print(r[0]) # Access by positional index
            return_beerbrand.append(str(r[0]))
            #print(r['ranking']) # Access by column name as a string
            return_ranking.append(float(r['ranking']))
            r_dict = dict(r.items()) 

            print(r_dict)
        #return r_dict
        return return_beerbrand,return_ranking

    def beer_list():

        sql = text('select distinct beercode, beerbrand from ranking order by beercode asc')
        result = db.engine.execute(sql)
        return_beerId = []
        return_beerName = []
        for r in result:
            #print(r[0]) # Access by positional index
            return_beerId.append(str(r[0]))
            #print(r['ranking']) # Access by column name as a string
            return_beerName.append(str(r[1]))
        
        return_final = list(zip(return_beerId,return_beerName))

        #return r_dict
        return return_final
