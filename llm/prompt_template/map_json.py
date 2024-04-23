from langchain.prompts import PromptTemplate
from llm.output_parser.json_parser import highlight_parser, trip_generation_parser_v2, list_location_parser

json_highlight_convertor_prompt = PromptTemplate(
    template="From json data {content}\n please map attribute \n{format_instructions}",
    input_variables=["context"],
    partial_variables={"format_instructions": highlight_parser.get_format_instructions()},
)

json_trip_summary_converter_prompt = PromptTemplate(
    template="From json data {content}\n please map attribute \n{format_instructions}",
    input_variables=["context"],
    partial_variables={"format_instructions": trip_generation_parser_v2.get_format_instructions()},
)

json_list_location_convertor_prompt = PromptTemplate(
    template="From json data {content}\n please map attribute \n{format_instructions}",
    input_variables=["context"],
    partial_variables={"format_instructions": list_location_parser.get_format_instructions()},
)