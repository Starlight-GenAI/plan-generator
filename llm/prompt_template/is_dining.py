from langchain_core.prompts import PromptTemplate
from llm.output_parser.enum_parser import parser

prompt = PromptTemplate.from_template(
    template = """
    Answer only yes or no
    Please consider content: {content} 
    if content associate with restaurant, dining or food please answer yes. if not, answer no
    {format_instructions}""",
    input_variable=["context"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
    )