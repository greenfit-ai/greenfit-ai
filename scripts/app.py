import streamlit as st
from utils import web_search, run_inference

def reply(query: str, num_results: int):
    res = web_search(query, num_results)
    return res

st.set_page_config(page_title="Beans AI", page_icon="🫘")
# Title of the web app
st.title("Beans AI🫘")
st.subheader("Find out about sustainability in your favorite sport clothing brands, in just one click!")
# Input text box for the search query
query = st.text_input("Describe what products you would like to explore:")

# Number of results to display
num_results = st.number_input("Number of results to display:", min_value=1, max_value=10, value=5)

# Button to initiate search
if st.button("Search"):
    if query:
        results = reply(query, num_results)
        res_true = run_inference(results)
        st.write(f"## Your results:")
        st.write_stream(res_true)
    else:
        st.write("Please enter a search term.")
