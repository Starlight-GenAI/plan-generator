from config.config import config
import logging
from adapter.cloud_storage import download_and_convert
from llm.run import predict_with_video, predict,convert_json
from llm.prompt_template.video_highlight import prompt, prompt_with_video
from llm.output_parser.json_parser import highlight_parser
from adapter.firestore import insert_video_highlight
from vertexai.generative_models import Part
from llm.prompt_template.map_json import json_highlight_convertor_prompt

def generate_video_highlight(id, user_id,is_use_subtitle,object_name):
    try:
        json_file_name = f'{object_name}.json'
        video_uri = f'gs://{config.cloud_storage.bucket_name}/{object_name}.mp4'
        logging.info("downloading subtitle ....")
        subtitle = download_and_convert(object_name=json_file_name)
        if is_use_subtitle:
            logging.info("predicting highlight ....")
            highlights = predict(context={"content": subtitle['subtitle']}, prompt=prompt, parser=highlight_parser)
        else:
            video = Part.from_uri(
            mime_type="video/mp4",
            uri=video_uri)
            logging.info("preparing video prompt ....")
            text = prompt_with_video(subtitle['subtitle'])
            logging.info("predicting highlight ....")
            completion = predict_with_video(video=video, text=text)
            highlights = convert_json(context={"content": completion}, prompt=json_highlight_convertor_prompt, parser=highlight_parser)
        logging.info("storing highlight into firestore ....")
        insert_video_highlight(data=highlights['highlights'], queue_id=id, user_id=user_id)
    except Exception as e:
        raise e