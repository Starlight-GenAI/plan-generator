from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    """
    Provide a very short summary, at least three sentences but not more than 6 sentences, for the following article:
    {content}
    """
)