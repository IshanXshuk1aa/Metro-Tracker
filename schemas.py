from pydantic import BaseModel ,ConfigDict 
from typing import Optional
class LineSchema(BaseModel):
    id : int 
    name : str
    color_hex : str
    model_config = ConfigDict(from_attributes=True)
class StationSchema(BaseModel):
    id : int
    name : str
    latitude :Optional[float]=None  
    longitude : Optional[float]=None  
    line_id : int
    order_index : int
    model_config = ConfigDict(from_attributes=True)
