from google.cloud import firestore
from config.config import config
from adapter.auth import credentials, project_id

db = firestore.Client(project=project_id, database=config.firestore.database, credentials=credentials)
db._database = config.firestore.database
video_summary = db.collection(config.firestore.video_summary_collection)
trip_summary = db.collection(config.firestore.trip_summary_collection)
video_highlight = db.collection(config.firestore.video_highlight_collection)

def insert_video_summary(data, queue_id,user_id, can_generate_trip):
    try:
        video_summary.document().set({"content": data, "queue_id": queue_id, "can_generate_trip": can_generate_trip, "user_id": user_id})
    except Exception as e:
        raise e
        

def insert_trip_summary(data, queue_id, user_id ):
    try:
        trip_summary.document().set({"content": data, "queue_id": queue_id, "user_id": user_id})
    except Exception as e:
        raise e

def insert_video_highlight(data, queue_id, user_id):
    try:
        video_highlight.document().set({"content": data, "queue_id": queue_id, "user_id": user_id})
    except Exception as e:
        raise e