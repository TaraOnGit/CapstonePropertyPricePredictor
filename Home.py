import streamlit as st

st.set_page_config(
    page_title = "Hello",
)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fedcba;  /* Change this to your desired color */
    }
    </style>""",
    unsafe_allow_html=True
    )
st.title('MakeHome - The Home of Homes')
