import logging
from adapter.cloud_storage import download_and_convert
from llm.run import predict, predict_with_video, convert_json
from llm.prompt_template.is_travel_video import prompt as is_travel_prompt
from llm.output_parser.enum_parser import parser as is_travel_parser
from llm.output_parser.enum_parser import location_output_parser
from llm.prompt_template.list_location import prompt as list_location_prompt
from llm.prompt_template.list_location import prompt_with_video
from llm.prompt_template.location_category import prompt as location_category_prompt
from llm.output_parser.json_parser import list_location_parser
from llm.prompt_template.content_summary import prompt as summary_prompt
from langchain_core.output_parsers import StrOutputParser
from model.video_summary import VideoSummaryContent
from adapter.firestore import insert_video_summary
from adapter.place_api import get_place_location,get_place_info
from config.config import config
from vertexai.generative_models import Part
from llm.prompt_template.map_json import json_list_location_convertor_prompt
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from utils.utils import calculate_interquartile_range, is_outlier
YES="yes"
NO="no"

def summarize_video(id, user_id, object_name):
    search = GoogleSearchAPIWrapper()
    search_tool = Tool(
    name="google_search",
    description="Search Google and return the all results.",
    func=search.run,
    )

    try:
        can_generate_trip = False
        can_summarize_video = False
        data = download_and_convert(object_name=f'{object_name}.json')
        logging.info("considering video type ... ")
        is_travel_video = predict(context={"content": data['subtitle']}, prompt=is_travel_prompt, parser=is_travel_parser)
        logging.info(f'video type {is_travel_video.value}')
        if is_travel_video.value == NO:
            return can_summarize_video, can_generate_trip
        else:
            can_summarize_video = True
            can_generate_trip = True
        logging.info("listing locations ... ")
        locations = predict(context={"content": data['subtitle']}, prompt=list_location_prompt,parser=list_location_parser)   
        logging.info("listing locations done ")
        location_with_summary = []
        for i in locations["locations"]:
            summary = predict(context={"content": search_tool.run(i['location_name'])}, prompt=summary_prompt,parser=StrOutputParser())
            place_location = get_place_location(i['location_name'])
            if place_location['place_id'] == "":
                continue
            category = predict(context={"content": summary}, prompt=location_category_prompt, parser=location_output_parser)
            location_with_summary.append(VideoSummaryContent(
                category=category.value,
                location_name=i['location_name'], 
                start_time=i['start_time'],
                end_time=i['end_time'],
                summary=summary,
                place_id=place_location['place_id'],
                lat=place_location['lat'],
                lng=place_location['lng'],
                ).to_dict())
        logging.info("preparing to store data video summary into firestore ....")
        insert_video_summary(data=location_with_summary, queue_id=id, can_generate_trip=can_generate_trip, user_id=user_id)
        return can_summarize_video, can_generate_trip
    except Exception as e:
        raise e

def summarize_video_v2(id, user_id, object_name, is_use_subtitle):
    search = GoogleSearchAPIWrapper()
    search_tool = Tool(
    name="google_search",
    description="Search Google and return the all results.",
    func=search.run,
    )
    try:
        can_generate_trip = True
        can_summarize_video = False
        json_file_name = f'{object_name}.json'
        video_uri =  f'gs://{config.cloud_storage.bucket_name}/{object_name}.mp4'
        logging.info("downloading subtitle ....")
        subtitle = download_and_convert(object_name=json_file_name)
        is_travel_video = predict(context={"content": subtitle['subtitle']}, prompt=is_travel_prompt, parser=is_travel_parser)
        logging.info(f'video type {is_travel_video.value}')
        if is_travel_video.value == NO:
            return can_summarize_video, can_generate_trip
        else:
            can_summarize_video = True
        if is_use_subtitle:
            logging.info("listing locations ... ")
            locations = predict(context={"content": subtitle['subtitle']}, prompt=list_location_prompt,parser=list_location_parser)   
            logging.info("listing locations done ")
        else:
            video = Part.from_uri(
            mime_type="video/mp4",
            uri=video_uri)
            logging.info("preparing video prompt ....")
            text = prompt_with_video(subtitle['subtitle'])
            logging.info("listing locations ... ")
            completion = predict_with_video(video=video, text=text)
            locations = convert_json(context={"content": completion}, prompt=json_list_location_convertor_prompt, parser=list_location_parser)
            logging.info("listing locations done ")
        location_with_summary = []
        lats = []
        lngs = []
        for i in locations["locations"]:
            try:
                content =  search_tool.run(i['location_name'])
                summary = predict(context={"content":content}, prompt=summary_prompt,parser=StrOutputParser())
            except Exception as e:
                logging.error(f'calling search api got error {e}')
                continue
            place_location = get_place_location(i['location_name'])
            if place_location['place_id'] == "":
                continue
            try:
                category_enum = predict(context={"content": summary}, prompt=location_category_prompt, parser=location_output_parser)
                category  = category_enum.value
            except:
                category = "etc"
            place_info = get_place_info(place_id=place_location['place_id'])
            location_with_summary.append(VideoSummaryContent(
                location_name=i['location_name'], 
                category=category,
                start_time=i['start_time'],
                end_time=i['end_time'],
                photos=place_info['photos'],
                summary=summary,
                place_id=place_location['place_id'],
                lat=place_location['lat'],
                lng=place_location['lng'],
                ).to_dict())
            lats.append(place_location['lat'])
            lngs.append(place_location['lng'])
        logging.info("preparing to store data video summary into firestore ....")
        # remove irrelavant location
        relavant_locations = []
        q1_lat,q3_lat,IQR_lat = calculate_interquartile_range(lats)
        q1_lng, q3_lng, IQR_lng = calculate_interquartile_range(lngs)
        for location in location_with_summary:
            if (not is_outlier(location['lat'], q1_lat,q3_lat,IQR_lat)) or (not is_outlier(location['lng'], q1_lng,q3_lng,IQR_lng)):
                relavant_locations.append(location)
        insert_video_summary(data=location_with_summary, queue_id=id, can_generate_trip=can_generate_trip, user_id=user_id)
        return can_summarize_video, can_generate_trip
    except Exception as e:
        raise e
        
    