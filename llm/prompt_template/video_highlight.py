from langchain_core.prompts import PromptTemplate
from llm.output_parser.json_parser import highlight_parser


def prompt_with_video(content):
    return  f"""
    From this video subtitle {content} and the mp4 video """ + """please find highlight associate with the video and subtitle. And result should have json structure like
[
    {
        "highlight_name": "name of highlight",
        "highlight_detail": "detail of highlight"
    }
]
    """

prompt = PromptTemplate(
    template="""From video subtitle {content}
    find highlight or interesting topic associate with subtitle
    {format_instructions}""",
    input_variables=["context"],
    partial_variables={"format_instructions": highlight_parser.get_format_instructions()},
)