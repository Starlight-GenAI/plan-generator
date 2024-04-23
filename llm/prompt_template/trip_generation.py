from langchain.prompts import PromptTemplate
from llm.output_parser.json_parser import trip_generation_parser,  trip_generation_parser_v2

prompt = PromptTemplate(
    template="From video subtitle {content}\n Generate travel trip\n{format_instructions}",
    input_variables=["context"],
    partial_variables={"format_instructions": trip_generation_parser.get_format_instructions()},
)

prompt_v2 = PromptTemplate(
    template="From video subtitle {content}\n Generate travel trip\n{format_instructions}",
    input_variables=["context"],
    partial_variables={"format_instructions": trip_generation_parser_v2.get_format_instructions()},
)

def prompt_with_video(subtitle):
    return f"""please consider this video subtitle {subtitle} with the mp4 video""" + """
Generate travel trip with location name and activities associate with the video and subtitle. 
And location name must not be country or province.
The result should have json structure like
[
    {
            "Day": 1,
            "location_with_activity": [
                {
                    "location_name": "name of location in specific name not just country name or province name",
                    "location_detail": "a brief about the location"
                    "activity": "detail interesting activity associate with location"
                },
                {
                    "location_name": "name of location in specific name not just country name or province name",
                    "location_detail": "a brief about the location"
                    "activity": "detail about interesting activity associate with location."
                }
            ]
    },
       {
            "Day": 2,
            "location_with_activity": [
                {
                    "location_name": "name of location in specific name not just country name or province name",
                    "location_detail": "a brief about the location"
                    "activity": "interesting activity associate with location"
                },
                {
                    "location_name": "name of location in specific name not just country name or province name",
                    "location_detail": "a brief about the location"
                    "activity": "interesting activity associate with location"
                }
            ]
    },
]
"""

def prompt_with_video_v2(subtitle):
    return f"""please consider this video subtitle {subtitle} with the mp4 video""" + """
And Generate travel trip with location name and activities associate with the video and subtitle. 
please do not compose activity more than one day into Day
And result should have json structure like
[
    {
            "Day": 1,
            "Location_with_activity": [
                {
                    "location_name": "name of location in specific name not just country name or province name",
                    "location_detail": "a brief about the location"
                    "activity": "detail interesting activity associate with location"
                },
                {
                    "location_name": "name of location in specific name not just country name or province name",
                    "location_detail": "a brief about the location"
                    "activity": "detail about interesting activity associate with location."
                }
            ]
    },
       {
            "Day": 2,
            "Location_with_activity": [
                {
                    "location_name": "name of location in specific name not just country name or province name",
                    "location_detail": "a brief about the location"
                    "activity": "interesting activity associate with location"
                },
                {
                    "location_name": "name of location in specific name not just country name or province name",
                    "location_detail": "a brief about the location"
                    "activity": "interesting activity associate with location"
                }
            ]
    },
]
"""