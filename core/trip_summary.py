import logging
from llm.run import predict,predict_with_video,convert_json
from adapter.firestore import insert_trip_summary
from langchain_core.output_parsers import StrOutputParser
from llm.prompt_template.content_summary import prompt as summary_prompt
from model.trip_summary import TripSummaryContent, LocationWithSummary,RecommendedRestaurant
from adapter.cloud_storage import download_and_convert
from llm.prompt_template.trip_generation import prompt as trip_generate_prompt
from llm.prompt_template.trip_generation import prompt_with_video
from llm.output_parser.json_parser import trip_generation_parser, trip_generation_parser_v2
from config.config import config
from vertexai.generative_models import Part
from adapter.place_api import get_place_location, get_nearby_restaurant, get_place_info,get_nearby_hotel
from llm.prompt_template.map_json import json_trip_summary_converter_prompt
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from utils.utils import calculate_interquartile_range, is_outlier

YES="yes"
NO="no"
LOCATION="location"
DINING="dining"
HOTEL="hotel"
NO_GOOD_RESULT = "No good Google Search Result was found"

def summarize_trip(id, user_id, object_name):
    search = GoogleSearchAPIWrapper()
    search_tool = Tool(
    name="google_search",
    description="Search Google and return the all results.",
    func=search.run,
    )

    try:
        logging.info("starting summarize trip ... ")
        logging.info("downloading data ... ")
        data =  download_and_convert(object_name=f'{object_name}.json')
        logging.info("generating trip ... ")
        completion = predict(context={"content": data['subtitle']}, prompt=trip_generate_prompt,parser=trip_generation_parser)
        logging.info("generating trip done ")
        trips = []
        for i in completion['trips']:
            location_with_summary = []
            for loc in i['location_with_activity']:
                summary = predict(context={"content": search_tool.run(loc['location_name'])}, prompt=summary_prompt,parser=StrOutputParser())
                place_location = get_place_location(loc['location_name'])
                location_with_summary.append(LocationWithSummary(location_name=loc['location_name'], summary=summary, place_id=place_location['place_id'], lat=place_location['lat'], lng=place_location['lng']).to_dict())
            trips.append(TripSummaryContent(day=f"Day {i['day']}", location_with_summary=location_with_summary).to_dict())
        logging.info("preparing to store trip into firestore ....")
        insert_trip_summary(data=trips, queue_id=id, user_id=user_id)
    except Exception as e:
        raise e

def summarize_trip_v2(id, user_id, object_name, is_use_subtitle):
    search = GoogleSearchAPIWrapper()
    search_tool = Tool(
    name="google_search",
    description="Search Google and return the all results.",
    func=search.run,
    )

    try:
        json_file_name = f'{object_name}.json'
        video_uri = f'gs://{config.cloud_storage.bucket_name}/{object_name}.mp4'
        logging.info("downloading subtitle ....")
        subtitle = download_and_convert(object_name=json_file_name)
        trips = []
        if is_use_subtitle:
            logging.info("generating trip ... ")
            completion = predict(context={"content": subtitle['subtitle']}, prompt=trip_generate_prompt,parser=trip_generation_parser)
            logging.info("generating trip done ")
        else:
            video = Part.from_uri(
                 mime_type="video/mp4",
                  uri=video_uri)
            logging.info("preparing video prompt ....")
            text = prompt_with_video(subtitle=subtitle['subtitle'])
            logging.info("generating trip ....")
            completion = predict_with_video(video=video, text=text)
            completion = convert_json(context={"content": completion}, prompt=json_trip_summary_converter_prompt, parser=trip_generation_parser_v2)
            logging.info("generating trip done")
        current_day = 0
        used_restaurant = []
        used_hotel = []
        for i in completion['trips']:
            location_with_summary = []
            lats = []
            lngs = []
            if len(i['location_with_activity']) == 0:
                continue
            current_day+=1
            num_dining = 0
            for loc in i['location_with_activity']:
                try:
                    content = search_tool.run(loc['location_name'])
                    if content != NO_GOOD_RESULT:
                        summary = predict(context={"content": content}, prompt=summary_prompt,parser=StrOutputParser())
                    else:
                        summary = ""
                except Exception as e:
                    logging.error(f'calling search api got error {e}')
                    continue
                place_location = get_place_location(loc['location_name'])
                if place_location['place_id'] == "":
                    continue
                place_info = get_place_info(place_id=place_location['place_id'])
                lats.append(place_location['lat'])
                lngs.append(place_location['lng'])
                if not place_info['is_restaurant']:
                    location_with_summary.append(LocationWithSummary(location_name=loc['location_name'], summary=summary, place_id=place_location['place_id'], lat=place_location['lat'], lng=place_location['lng'],category=LOCATION, rating=place_info['rating'], photos=place_info['photos']).to_dict())
                else:
                    used_restaurant.append(loc['location_name'])
                    location_with_summary.append(LocationWithSummary(location_name=loc['location_name'], summary=summary, place_id=place_location['place_id'], lat=place_location['lat'], lng=place_location['lng'], category=DINING, rating=place_info['rating'], photos=place_info['photos']).to_dict())
            q1_lat,q3_lat,IQR_lat = calculate_interquartile_range(lats)
            q1_lng, q3_lng, IQR_lng = calculate_interquartile_range(lngs)
            relevant_location = []
            locations = []
            for location in location_with_summary:
                if (not is_outlier(location['lat'], q1_lat,q3_lat,IQR_lat)) or (not is_outlier(location['lng'],q1_lng, q3_lng, IQR_lng)):
                    if location['category'] == DINING:
                        num_dining+=1
                    relevant_location.append(location)
            if len(relevant_location) == 0:
                relevant_location = location_with_summary
                
            if len(relevant_location) < 5:
                if num_dining < 2:
                    for location in relevant_location:
                        if location['category'] == LOCATION:
                            restaurant = get_nearby_restaurant(place_name=location['location_name'], used_restaurant=used_restaurant)
                            if restaurant['name'] == "":
                                locations.append(location)
                                continue
                            restaurant_info = get_place_info(place_id=restaurant['place_id'])
                            restaurant_content = search_tool.run(restaurant['name'])
                            if restaurant_content != NO_GOOD_RESULT: 
                                restaurant_summary = predict(context={"content": restaurant_content}, prompt=summary_prompt,parser=StrOutputParser())
                            else:
                                restaurant_summary = ""
                            recommended_restaurant = RecommendedRestaurant(name=restaurant['name'], summary=restaurant_summary, place_id=restaurant['place_id'], lat=restaurant['lat'], lng=restaurant['lng'], rating=restaurant_info['rating'],photos=restaurant_info['photos']).to_dict()
                            locations.append(LocationWithSummary(location_name=location['location_name'], summary=location['summary'], place_id=location['place_id'], lat=location['lat'], lng=location['lng'], category=LOCATION, rating=location['rating'], photos=location['photos'], has_recommended_restaurant=True,recommended_restaurant=recommended_restaurant).to_dict())
                            used_restaurant.append(restaurant['name'])
                        else:
                            locations.append(location)
                else:
                    locations = relevant_location
            else:
                if num_dining == 0:
                    for location in relevant_location:
                        if location['category'] == LOCATION:
                            restaurant = get_nearby_restaurant(place_name=location['location_name'], used_restaurant=used_restaurant)
                            if restaurant['name'] == "":
                                locations.append(location)
                                continue
                            restaurant_info = get_place_info(place_id=restaurant['place_id'])
                            restaurant_content = search_tool.run(restaurant['name'])
                            if restaurant_content != NO_GOOD_RESULT:
                                restaurant_summary = predict(context={"content": restaurant_content}, prompt=summary_prompt,parser=StrOutputParser())
                            else:
                                restaurant_summary = ""
                            recommended_restaurant = RecommendedRestaurant(name=restaurant['name'], summary=restaurant_summary, place_id=restaurant['place_id'], lat=restaurant['lat'], lng=restaurant['lng'], rating=restaurant_info['rating'],photos=restaurant_info['photos']).to_dict()
                            locations.append(LocationWithSummary(location_name=location['location_name'], summary=location['summary'], place_id=location['place_id'], lat=location['lat'], lng=location['lng'], category=LOCATION, rating=location['rating'], photos=location['photos'], has_recommended_restaurant=True,recommended_restaurant=recommended_restaurant).to_dict())
                            used_restaurant.append(restaurant['name'])
                        else:
                            locations.append(location)
                else:
                    locations = relevant_location
            
            recommended_hotel = get_nearby_hotel(f"{locations[-1]['lat']},{locations[-1]['lng']}", used_hotel)
            if recommended_hotel['name'] != "":
                hotel_info = get_place_info(recommended_hotel['place_id'])
                hotel_content = search_tool.run(recommended_hotel['name'])
                if hotel_content != NO_GOOD_RESULT:
                    hotel_summary=predict(context={"content": hotel_content}, prompt=summary_prompt,parser=StrOutputParser())
                else:
                    hotel_summary = ""
                used_hotel.append(recommended_hotel['name'])
                locations.append(LocationWithSummary(location_name=recommended_hotel['name'], summary=hotel_summary, place_id=recommended_hotel['place_id'], lat=recommended_hotel['lat'], lng=recommended_hotel['lng'], category=HOTEL, rating=recommended_hotel['rating'], photos=hotel_info['photos']).to_dict())
            trips.append(TripSummaryContent(day=f"Day {current_day}", location_with_summary=locations).to_dict())
        logging.info("preparing to store trip into firestore ....")
        insert_trip_summary(data=trips, queue_id=id, user_id=user_id)
            
    except Exception as e:
        raise e
