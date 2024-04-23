from typing import List



class PhotoDetail:
    def __init__(self, reference: str, max_width: int, max_height: int):
        self.reference = reference
        self.max_width = max_width
        self.max_height = max_height
    
    def to_dict(self):
        return {"reference": self.reference, "max_width": self.max_width, "max_height": self.max_height}

class RecommendedRestaurant:
    def __init__(self, name: str, summary: str, place_id: str, lat: float, lng: float, rating: float, photos: PhotoDetail):
        self.name = name
        self.summary = summary
        self.place_id = place_id
        self.rating = rating
        self.lat = lat
        self.lng = lng
        self.photos = photos
    
    def to_dict(self):
        return {"name": self.name,"summary": self.summary,"rating": self.rating ,"place_id": self.place_id, "lat":self.lat, "lng": self.lng, "photos": self.photos}
class LocationWithSummary:
    def __init__(self, location_name: str, summary: str, place_id: str, lat: float, lng: float, photos: List[PhotoDetail],category: str, rating: float, has_recommended_restaurant: bool=False,recommended_restaurant:RecommendedRestaurant=None):
        self.location_name = location_name
        self.summary = summary
        self.place_id = place_id
        self.lat = lat
        self.lng = lng
        self.category = category
        self.rating = rating
        self.photos = photos
        self.has_recommended_restaurant = has_recommended_restaurant
        self.recommended_restaurant = recommended_restaurant
    
    def to_dict(self):
        return {"location_name": self.location_name, 
                "summary": self.summary, 
                "place_id": self.place_id, 
                "lat": self.lat, 
                "lng": self.lng, 
                "photos": self.photos,
                "category": self.category, 
                "rating": self.rating,
                "has_recommended_restaurant": self.has_recommended_restaurant,
                "recommended_restaurant": self.recommended_restaurant
                }


class TripSummaryContent:
    def __init__(self, day: str, location_with_summary: List[LocationWithSummary]):
        self.day = day
        self.location_with_summary = location_with_summary
        
    
    def to_dict(self):
        return  {"day": self.day, "location_with_summary": self.location_with_summary}