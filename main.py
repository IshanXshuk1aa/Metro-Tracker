from fastapi import FastAPI , Depends , WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import local_session
from .schemas import LineSchema , StationSchema
from . import models
import json ,asyncio
from .redis_client import redis_client
app = FastAPI()
def get_db():
    db: Session = local_session()
    try:
        yield db
    finally:
        db.close()
        

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/lines' , response_model=list[LineSchema])
def get_lines(db : Session = Depends(get_db)):
    lines = db.query(models.Line).all()
    return lines
@app.get('/lines/{line_id}/stations' , response_model=list[StationSchema])
def get_stations(line_id : int ,db : Session = Depends(get_db)):
    stations = db.query(models.Station).filter(models.Station.line_id == line_id).order_by(models.Station.order_index).all()
    return stations

@app.websocket('/ws/positions')
async def positions(websocket: WebSocket):
    await websocket.accept()
    db = local_session()
    while True:
        trips =  db.query(models.Trip).filter_by(status="active").all()
        positions_data = {}
        for trip in trips:
            key = f"trip:{trip.id}:position"  
            value = redis_client.get(key) 
           
            if value is not None:
                position = json.loads(value)
                position["line_id"] = trip.line_id
                positions_data[trip.id] = position 
        await websocket.send_json(positions_data)
        await asyncio.sleep(10)
