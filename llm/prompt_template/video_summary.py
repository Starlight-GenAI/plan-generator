from langchain_core.prompts import PromptTemplate


def prompt_with_video(content):
    return  f"""
    From this video subtitle {content} and the mp4 video """ + """ Provide a summary, at least 80 words and no more than 100 words"""

prompt = PromptTemplate(
    template="""From video subtitle {content} 
    Provide a summary, at least 80 words and no more than 100 words""",
    input_variables=["context"],
)