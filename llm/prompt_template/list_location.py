from langchain.prompts import PromptTemplate
from llm.output_parser.json_parser import list_location_parser

prompt = PromptTemplate(
    template="From video subtitle {content}\n List all unique locations with start time and end time.\n{format_instructions}",
    input_variables=["context"],
    partial_variables={"format_instructions": list_location_parser.get_format_instructions()},
)

def prompt_with_video(content):
    return f"""From this video subtitle {content} and the mp4 video """ + """
    Please list all location ,which is not country or province, with start time and end time. Location name should not be country or province moreover location name must be unique.
    The result should have json structure like
    {
        "locations": [
            {
                "location_name": "name of location. And location's name must not be country or province"
                "start_time: "the time that the location was mentioned",
                "end_time": "the time that the location was last mentioned"
            },
            {
                "location_name": "name of location. And location's name must not be country or province"
                "start_time: "the time that the location was mentioned",
                "end_time": "the time that the location was last mentioned"
            }
        ]
    }

"""
    