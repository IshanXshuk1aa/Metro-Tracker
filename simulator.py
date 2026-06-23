import time
import json
from .database import local_session
from .redis_client import redis_client
from . import models
db = local_session()
stations = db.query(models.Station).order_by(models.Station.order_index).all()
lines = db.query(models.Line).all()
trips = db.query(models.Trip).filter_by(status="active").all()
interchanges = db.query(models.Interchange).all()

stations_by_line = {}

for station in stations:
    if station.line_id not in stations_by_line:
        stations_by_line[station.line_id] = []
    stations_by_line[station.line_id].append(station)
    
def get_position(trip):
    key = f"trip:{trip.id}:position"
    value = redis_client.get(key)
    if value is not None:
        return json.loads(value)
    else:
        return {"index": 0, "direction": trip.direction}
def set_position(trip, index, direction, just_switched=False):
    key = f"trip:{trip.id}:position"
    value = {"index": index, "direction": direction, "just_switched": just_switched}
    value_as_string = json.dumps(value)
    redis_client.set(key, value_as_string)

# trip = trips[0]
# set_position(trip, 1 , "up")
# result = get_position(trip)
# print(result)
def get_next_position(index , direction , last_index):
    if(index==0):
        direction = "up"
        index+=1
    elif (index == last_index):
        direction = "down"
        index-=1
    elif(direction == "up"):
        index+=1
    elif(direction == "down"):
        index-=1
    return {"index" : index , "direction" : direction}

def interchange(station_id):
    for change in interchanges:
        if change.station_a_id == station_id:
            return next(s for s in stations if s.id == change.station_b_id)
        if change.station_b_id == station_id:
            return next(s for s in stations if s.id == change.station_a_id)
    return None    


while True:
    for eachtrips in trips:
        current = get_position(eachtrips)
        line_station = stations_by_line[eachtrips.line_id]
        last_index = len(line_station) - 1
        current_station = line_station[current["index"]]

        # if not current.get("just_switched", False):
        #     connected = interchange(current_station.id)
        #     if connected is not None:
        #         new_line_stations = stations_by_line[connected.line_id]
        #         new_index = next(i for i, s in enumerate(new_line_stations) if s.id == connected.id)
        #         eachtrips.line_id = connected.line_id
        #         db.commit()
        #         set_position(eachtrips, new_index, "up", just_switched=True)
        #         print(f"Trip {eachtrips.id} SWITCHED to line {connected.line_id} at index {new_index}")
        #         continue

        nextt = get_next_position(current["index"], current["direction"], last_index)
        still_switched = current.get("just_switched", False) and nextt["index"] != 0 and nextt["index"] != last_index
        set_position(eachtrips, nextt["index"], nextt["direction"], just_switched=still_switched)
        print(f"Trip {eachtrips.id} | index {nextt['index']} | direction {nextt['direction']} | last_index {last_index}")

    time.sleep(10)

#--------------------------------------------------------#
