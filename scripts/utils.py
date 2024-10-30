import requests
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import Field, BaseModel
from dotenv import load_dotenv
import os
import re

load_dotenv()

class SearchOptim(BaseModel):
    """Structure of the output for browser search optimization"""
    brief_des: str = Field(description="Brief description of how the search was optimized")
    keywords: list = Field(description="List of keywords")
    description = "Schema to represent the output of a Browser Search Optimization agent"
   

openai_api_key = os.getenv("openai_api_key")
rapid_api_key = os.getenv("rapid_api_key")
base_llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini")
base_prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      """You are a skilled Browser Search Optimization experts that is required to turn the user description of a product into several keywords optimized for web search. You should produce your output in this way:
      - Brief description of how you optimized the search
      - Keywords list for searching
      Be concise and always relay on what the user asks. Never add any extra content or extra search."""),
    ("human", "{message}"),
  ]
)
chat_chain = base_prompt | base_llm.with_structured_output(SearchOptim)



def handle_user_request(user_req: str) -> list:
    res = chat_chain.invoke({"message": user_req})
    return res.keywords

def web_search(user_req: str, limit: int):
    keywords = handle_user_request(user_req)
    query = " ".join(keywords)
    url = "https://real-time-product-search.p.rapidapi.com/search-v2"

    querystring = {"q": query,"country":"us","language":"en","page":"1","limit":limit,"sort_by":"BEST_MATCH","product_condition":"ANY"}

    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "real-time-product-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    resdict = response.json()
    data = resdict["data"]["products"]
    # product_title, product_description, product_photos[0], product_page_url 
    products_list = [[d["product_title"], d["product_description"], d["product_photos"][0], d["product_page_url"]] for d in data]
    proudcts_strings = [f"### [{product[0]}]({product[3]})\n\n![Product image]({product[2]})\n\n#### Description\n{product[1]}\n\n-------------------------------------\n\n" for product in products_list]
    for res in proudcts_strings:
        yield res

def run_inference():
    pass

