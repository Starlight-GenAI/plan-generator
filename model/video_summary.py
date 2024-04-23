from model.trip_summary import PhotoDetail
from typing import List

class VideoSummaryContent:
    def __init__(self, location_name: str, category: str, start_time: float, end_time: float, summary: str, place_id: str, lat: float, lng: float, photos: List[PhotoDetail]):
        self.location_name = location_name
        self.category = category
        self.start_time = start_time 
        self.end_time = end_time
        self.summary = summary
        self.place_id = place_id
        self.lat = lat
        self.lng = lng
        self.photos = photos
    
    def to_dict(self):
        return {'location_name': self.location_name, 
                'category':self.category ,
                'start_time': self.start_time, 'end_time': self.end_time, 
                'summary': self.summary, 'place_id': self.place_id,
                'lat': self.lat, 'lng': self.lng,
                'photos': self.photos
                }