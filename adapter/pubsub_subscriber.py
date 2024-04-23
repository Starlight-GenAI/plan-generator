import logging
from google.cloud import pubsub_v1
from config.config import config
from model.generate_plan_event import GeneratePlanEvent
from model.notification_event import NotificationEvent
from core.video_summary import summarize_video_v2
from core.video_highlight import generate_video_highlight
from adapter.auth import init_credential
from core.trip_summary import summarize_trip_v2
from adapter.pubsub_publisher import publish
subscriber = pubsub_v1.SubscriberClient(credentials=init_credential(audience=config.pubsub.subscriber_audience))
subscription_path = subscriber.subscription_path(config.pubsub.project_id, config.pubsub.generate_plan_subscription_id)

FAIL = "failed"
SUCCESS = "success"
IS_NOT_TRAVEL_VIDEO="is_not_travel_video"

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    logging.info("start consuming event")
    try:
        data = GeneratePlanEvent(message.data)
        message.ack()
        logging.info(f"event id {data.id} is processing")
        can_summarize_video, can_generate_trip = summarize_video_v2(id=data.id, object_name=data.object_name, user_id=data.user_id, is_use_subtitle=data.is_use_subtitle)
        if not can_summarize_video:
            logging.info(f"event id {data.id} video does not associate with travel content")
            publish(NotificationEvent(id=data.id, status=IS_NOT_TRAVEL_VIDEO).to_byte())
        else:
            generate_video_highlight(id=data.id, user_id=data.user_id, object_name=data.object_name, is_use_subtitle=data.is_use_subtitle)
            if can_generate_trip:
                summarize_trip_v2(id=data.id,user_id=data.user_id,object_name=data.object_name,is_use_subtitle=data.is_use_subtitle)
            publish(NotificationEvent(id=data.id, status=SUCCESS).to_byte())
            
        logging.info(f"event id {data.id} done")
    except Exception as e:
        logging.error(f'error with {e}')
        publish(NotificationEvent(id=data.id, status=FAIL).to_byte())

def run():
    logging.info("consumer running")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    with subscriber:
        try:
            streaming_pull_future.result()
        except:
            print("pull data failed")