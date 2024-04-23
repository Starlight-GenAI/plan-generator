from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from typing import List, TypedDict

class LocationWihTime(BaseModel):
    locations: List[TypedDict("locations",{"location_name": str, "start_time": float, "end_time": float })] = Field(description="a location name ,which must not name of country or province, with start time and end time which was metioned in video")

class TripGeneration(BaseModel):
    trips: List[TypedDict("Trip", {"day": int, "location_with_activity": List[TypedDict("locations", {"location_name": str, "activity": str})]})] = Field(description="a travel trip which compose of day, and list of location and recommended activity of each place.If some day has not enough information please ignore.")

class VideoHighlight(BaseModel):
    highlight_name: str = Field("highlight_name")
    highlight_detail: str = Field("highlight_detail")
    
class Highlight(BaseModel):
    highlights: List[VideoHighlight]
    
class LocationWithActivity(BaseModel):
    location_name: str = Field("location_name")
    location_detail: str = Field("location_detail")
    activity: str = Field("activity")

class Trip(BaseModel):
    day: int = Field("day")
    location_with_activity: List[LocationWithActivity] = Field("location_with_activity")
    
class TripData(BaseModel):
    trips: List[Trip]

list_location_parser = JsonOutputParser(pydantic_object=LocationWihTime)
trip_generation_parser = JsonOutputParser(pydantic_object=TripGeneration)
highlight_parser = JsonOutputParser(pydantic_object=Highlight)
trip_generation_parser_v2 = JsonOutputParser(pydantic_object=TripData)