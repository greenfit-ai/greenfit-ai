import streamlit as st
from scripts.utils import web_search, run_inference
from scripts.secretsStreamlit import courier_auth_token
from streamlit_supabase_auth_ui.widgets import __login__

def reply(query: str, num_results: int):
    res = web_search(query, num_results)
    return res

__login__obj = __login__(auth_token = courier_auth_token, 
                    company_name = "Beans AI🌱",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()


if LOGGED_IN == True:
    # Title of the web app
    st.title("Beans AI🌱")
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
