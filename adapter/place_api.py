import googlemaps
from config.config import config
from model.trip_summary import PhotoDetail

gmaps = googlemaps.Client(key=config.google_map.key)

def get_place_location(place_name):
    try:
        place_complete = gmaps.places_autocomplete(input_text=place_name)
        if len(place_complete) == 0:
            return {"place_id": "", "lat": 0 ,"lng":0}
        geo = gmaps.geocode(place_id=place_complete[0]['place_id'])
        lat_long = geo[0]['geometry']['location']
        return {"place_id": place_complete[0]['place_id'], "lat":lat_long['lat'] ,"lng":lat_long['lng']}
    except:
        return {"place_id": "", "lat": 0 ,"lng":0}

def get_nearby_restaurant(place_name, used_restaurant):
    try:
        place_complete = gmaps.places_autocomplete(input_text=place_name)
        restaurants = []
        if len(place_complete) == 0:
            return {"name": "" ,"place_id": "", "lat": 0 ,"lng":0, "rating": 0}
        geo = gmaps.geocode(place_id=place_complete[0]['place_id'])
        lat_long = geo[0]['geometry']['location'].values()
        location = ",".join([str(i) for i in lat_long])
        restaurant_nearby = gmaps.places_nearby(location=location, radius = 2000, open_now =False , type = 'restaurant')
        for restaurant in restaurant_nearby['results']:
            if 'rating' not in restaurant or restaurant['name'] == "" or restaurant['name'] in used_restaurant:
                continue
            else:
                rating = restaurant['rating']
            restaurants.append({'name': restaurant['name'], 'rating': rating, 'place_id': restaurant['place_id'], 'lat': restaurant['geometry']['location']['lat'], 'lng':restaurant['geometry']['location']['lng'] })
    
        if len(restaurants) == 0:
            return {'name': "", 'rating': 0, 'place_id': "", 'lat': 0, 'lng':0 }
            
        restaurants.sort(key=lambda x: -x['rating'])
        return restaurants[0]
    except:
        return {"name": "" ,"place_id": "", "lat": 0 ,"lng":0, "rating": 0}

def get_place_info(place_id):
    try:
        place = gmaps.place(place_id=place_id,fields=["type", "rating", "photo"])
        if 'rating' in  place['result']:
            rating = place['result']['rating']
        else:
            rating = 0
        types = place['result']['types']
        is_restaurant = True if "food" in types or "restaurant" in types else False
        photos = []
    
        if 'photos' in place['result']:
            for photo in place['result']["photos"]:
                photos.append(PhotoDetail(reference=photo["photo_reference"], max_width=photo["width"], max_height=photo["height"]).to_dict())
        
        return  {"is_restaurant": is_restaurant, 'rating': rating, 'photos': photos }
    except:
        {"is_restaurant": False, 'rating': 0, 'photos': [] }