import requests
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import Field, BaseModel
from qdrant_client import QdrantClient
from .secretsStreamlit import openai_api_key, rapid_api_key, qdrant_api_key, qdrant_url

class SearchOptim(BaseModel):
    """Structure of the output for browser search optimization"""
    brief_des: str = Field(description="Brief description of how the search was optimized")
    keywords: list = Field(description="List of keywords")
    description = "Schema to represent the output of a Browser Search Optimization agent"

class SustainEval(BaseModel):
    """Structure of the output for sustainability evaluation"""
    low_c_mat_grade: int = Field(description="Grade on Low carbon material usage from 1 to 10")
    ren_en_grade: int = Field(description="Grade on renewable energy usage from 1 to 10")
    overall_grade: int = Field(description="Overall sustainability grade from 1 to 10")
    low_c_mat_des: str = Field(description="Explanation for the grade on low carbon material usage")
    ren_en_des: str = Field(description="Explanation for the grade on renewable energy usage")
    overall_des: str = Field(description="Explanation for the grade on overall sustainability")
    description = "Schema to represent the output of a Sustainability Evaluation agent"

class NeuralSearcher:
    def __init__(self, collection_name, client, model):
        self.collection_name = collection_name
        self.model = model
        self.qdrant_client = client
    def search(self, text: str):
        vector = self.model.embed_query(text)
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=None, 
            limit=2,
        )
        payloads = [hit.payload for hit in search_result]
        retrieved_context = f"""This is the top-match retrieved context for the user's prompt:
        '''
        {payloads[0]['text']}
        '''
        And this is the second best match:
        '''
        {payloads[1]['text']}
        '''
        """
        return retrieved_context

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
sustain_prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      """You are an expert in sport fashion sustainability who is asked to give an evaluation of a product and/or its brand. Relaying on this context retrieved from your information database:
      
      {context}

      You should produce your evaluation, and the output must be in this way:
      - A grade on low-carbon material usage (from 1 to 10)
      - A grade on renewable energy usage (from 1 to 10)
      - An overall sustainability grade (from 1 to 10)
      - An explanation for your grade on low-carbon material usage
      - An explanation for your grade on renewable energy usage
      - An explanation for your grade on overall sustainability
      Be concise and always rely on what the user asks. Never add any extra content or extra search."""),
    ("human", "{message}"),
  ]
)
sustain_chain = sustain_prompt | base_llm.with_structured_output(SustainEval)
embedder = OpenAIEmbeddings(model="text-embedding-3-small", api_key=openai_api_key)
qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
searcher = NeuralSearcher("fashiondata", qdrant_client, embedder)

def remove_items(test_list, item): 
    res = [i for i in test_list if i != item] 
    return res 

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
    proudcts_strings = [f"### [{product[0]}]({product[3]})\n\n![Product image]({product[2]})\n\n#### Description\n{product[1]}" for product in products_list]
    return proudcts_strings

def grade_to_markdown_color(grade: int):
    if grade < 3:
        evaluation = "bad"
    elif 3 <= grade < 7:
        evaluation = "medium"
    else:
        evaluation = "good"
    colors = {"bad": "ff0000", "medium": "ffcc00", "good": "33cc33"}
    mdcode = f"![#{colors[evaluation]}](https://placehold.co/15x15/{colors[evaluation]}/{colors[evaluation]}.png)"
    return mdcode



def run_inference(product_strings):
    final_strings = []
    for product_string in product_strings:
        context = searcher.search(product_string)
        res = sustain_chain.invoke({"message": f"This is the product you should evaluate:\n\n{product_string}", "context": context})
        final_res = f"{product_string}\n\n#### Sustainability evaluation\n{grade_to_markdown_color(res.low_c_mat_grade)} **Low carbon materials usage**: {res.low_c_mat_des}\n\n{grade_to_markdown_color(res.ren_en_grade)} **Renewable energies usage**: {res.ren_en_des}\n\n{grade_to_markdown_color(res.overall_grade)} **Overall sustainability**: {res.overall_des}\n\n-------------------------------------\n\n"
        final_strings.append(final_res)
    for final_string in final_strings:
        yield final_string
        

