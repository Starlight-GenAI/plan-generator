import json
from google.auth import jwt
import google.auth
from config.config import config

service_account_info = json.load(open(config.server.credential_path))
credentials, project_id = google.auth.load_credentials_from_file(config.server.credential_path)

def init_credential(audience):
    return jwt.Credentials.from_service_account_info(
    service_account_info, audience=audience)
