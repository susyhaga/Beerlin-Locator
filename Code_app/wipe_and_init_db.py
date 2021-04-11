import random, string
from beerlin import db, bcrypt
from beerlin.models import User, Local

def load_file_as_list(filename):
    result = []
    with open(filename, "r") as a_file:
        for line in a_file:
            result.append(line.strip())
    return result

db.drop_all()

# This attempts to fix this error:
# AddGeometryColumn() error: unexpected metadata layout
# DiscardGeometryColumn: "no such table: geometry_columns"
db.engine.execute("SELECT InitSpatialMetaData();")

db.create_all()



# Insert my own user as Admin
hashed_password = bcrypt.generate_password_hash('password')
admin = User(username='Susy', email='susy87@gmail.com', password=hashed_password)
db.session.add(admin)
print(f"Added admin user: email=susy87@gmail.com pass=password")


count_users = 0


with open("beerlin/resources/locals_fake2.txt", "r") as a_file:
  for line in a_file:
    id,name,address,latitude,longitude,zipcode,city = line.strip().split(",")


    local = Local(
        id=id, 
        name=name, 
        address=address,
        latitude=latitude,
        longitude=longitude,
        location=Local.point_representation(latitude=latitude, longitude=longitude),
        zipcode=zipcode,
        city=city)


    db.session.add(local)
    count_users += 1

print(f"Added locals: {count_users}")
        
db.session.commit()