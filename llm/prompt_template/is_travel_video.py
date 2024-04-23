from langchain_core.prompts import PromptTemplate
from llm.output_parser.enum_parser import parser

prompt = PromptTemplate.from_template(
    template = """
    Answer only yes or no
    From this {content} if associate with travel asnwer yes. 
    If not return no\n {format_instructions}""",
    input_variable=["context"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
    )