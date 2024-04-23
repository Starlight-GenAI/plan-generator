from google.cloud import pubsub_v1
import logging
from config.config import config
from typing import Callable
from concurrent import futures
from adapter.auth import init_credential

publisher = pubsub_v1.PublisherClient(credentials=init_credential(config.pubsub.publisher_audience))
topic_path = publisher.topic_path(config.pubsub.project_id, config.pubsub.notification_topic)
publish_futures = []

def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            publish_future.result(timeout=60)
        except futures.TimeoutError:
            logging.error("publish error")
        except Exception as e:
            raise e
    return callback

def publish(data: bytes):
    try:
        publish_future = publisher.publish(topic_path, data)
        publish_future.add_done_callback(get_callback(publish_future, data))
        publish_futures.append(publish_future)
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
        logging.info("successfully publish notification")
    except Exception as e:
        logging.error(f'publish notification error with {e}')
