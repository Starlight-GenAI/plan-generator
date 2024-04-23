import os
import vertexai
from config.config import config
from vertexai.generative_models import GenerativeModel
from langchain_google_vertexai import VertexAI
import vertexai.preview.generative_models as generative_models
from adapter.auth import credentials, project_id

os.environ["GOOGLE_CSE_ID"] = config.google.google_cse_id
os.environ["GOOGLE_API_KEY"] = config.google.google_api_key

vertexai.init(project=config.vertex_ai.project_id, credentials=credentials)
model = VertexAI(project=project_id,model_name=config.vertex_ai.model,credentials=credentials)
json_converter_model = VertexAI(model=config.vertex_ai.json_convertor_model, convert_system_message_to_human=True, temperature=0)
video_model = GenerativeModel(config.vertex_ai.video_model)
generation_config = {
    "max_output_tokens": int(config.vertex_ai.max_output_tokens),
    "temperature": float(config.vertex_ai.temperature),
    "top_p": float(config.vertex_ai.top_p),
}
safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}
