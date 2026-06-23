#Not vibe-coded comments are for the ease of understanding the code
from .database import local_session 
from . import  models
from .database import Base, engine, local_session


Base.metadata.create_all(engine)
db = local_session()
#------------------Trains----------------------#
Yellow = models.Line(
    name = "Yellow_line",
    color_hex="#ACF00D"
)
Blue = models.Line(
    name = "Blue_line",
    color_hex="#200EE9"
)
Red= models.Line(
    name = "Red_line",
    color_hex="#D81313"
)
db.add_all([Yellow , Blue , Red])
db.commit()
db.refresh(Yellow)
db.refresh(Blue)
db.refresh(Red)
#------------------------Stations----------------------------#

Yellow_station = [
    ("Samaypur Badli", 28.742872, 77.146545),
    ("Vishwavidyalaya", 28.694765, 77.212418),
    ("Kashmere Gate", 28.667879, 77.228012),
    ("Rajiv Chowk", 28.632896, 77.219574),
    ("Dilli Haat - INA", 28.575195, 77.209473),
    ("Huda City Centre", 28.459118, 77.072586)
]

Blue_station= [
    ("Dwarka", 28.614899, 77.022629),
    ("Rajiv Chowk", 28.632896, 77.219574),
    ("Mandi House", 28.625816, 77.234726),
    ("Yamuna Bank", 28.623178, 77.267937),
    ("Noida Electronic City", 28.628685, 77.375229)
]

Red_station= [
    ("Rithala", 28.720821, 77.105042),
    ("Kashmere Gate", 28.667879, 77.228012),
    ("Shastri Park", 28.668451, 77.250404),
    ("Shaheed Sthal", 28.670177, 77.416031)
]
#------------------ADDING STATIONS-------------------------#
def add_stations(line , station_names):

    for index, (name, lat, lon) in enumerate(station_names):

        station = models.Station(
            name=name,
            latitude=lat,
            longitude=lon,
            line_id=line.id,
            order_index=index
            )
        db.add(station) 
   

add_stations(Yellow , Yellow_station)
add_stations(Blue ,Blue_station)
add_stations(Red,Red_station)
db.commit()
#----------------InterChange-------------#
kashmere_yellow = db.query(models.Station).filter_by(name="Kashmere Gate" , line_id = Yellow.id).first()
kashmere_red = db.query(models.Station).filter_by(name="Kashmere Gate" , line_id = Red.id).first()
Rajiv_yellow = db.query(models.Station).filter_by(name="Rajiv Chowk" , line_id = Yellow.id).first()
Rajiv_blue = db.query(models.Station).filter_by(name="Rajiv Chowk" , line_id = Blue.id).first()

interchange1=models.Interchange(
    station_a_id = kashmere_yellow.id,
    station_b_id = kashmere_red.id
)
interchange2=models.Interchange(
    station_a_id = Rajiv_yellow.id,
    station_b_id = Rajiv_blue.id
)
db.add_all([interchange1 , interchange2])
db.commit()
#--------------------------------------------#
Train_no = ["DL-001", "DL-002", "DL-003", "DL-004"]
Trains=[]
for train_no in Train_no:
    train = models.Train(
        train_no = train_no 
    )
    Trains.append(train)
    db.add(train)
db.commit()
for t in Trains:
    db.refresh(t)
#------------------------------#
trip1 = models.Trip(
    train_id = Trains[0].id,
    line_id = Yellow.id,
    direction = "up",
    status = "active"
)
trip2 = models.Trip(
    train_id = Trains[1].id,
    line_id = Blue.id,
    direction = "up",
    status = "active"
)
trip3 = models.Trip(
    train_id = Trains[2].id,
    line_id = Red.id,
    direction = "down",
    status = "active"
)
trip4 = models.Trip(
    train_id = Trains[3].id,
    line_id = Yellow.id,
    direction = "up",
    status = "active"
)
db.add_all([trip1 , trip2 , trip3 , trip4])
db.commit()


