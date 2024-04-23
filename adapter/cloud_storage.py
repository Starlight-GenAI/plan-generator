import json
import os
from google.cloud import storage
from config.config import  config
from adapter.auth import credentials, project_id


storage_client = storage.Client(project=project_id, credentials=credentials)
bucket = storage_client.bucket(config.cloud_storage.bucket_name)

def download_and_convert(object_name):
    try:
        blob = bucket.blob(object_name)
        blob.download_to_filename(object_name)
        with open(object_name, 'rb') as f:
            data = json.load(f)
        os.remove(object_name)
        return data
    except Exception as e:
        raise e

