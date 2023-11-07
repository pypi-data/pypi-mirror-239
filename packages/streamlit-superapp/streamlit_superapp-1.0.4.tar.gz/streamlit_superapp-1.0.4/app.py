import streamlit_superapp
import streamlit as st

from streamlit_superapp.page_loader import PageLoader

st.set_page_config(
    page_title="Streamlit Super App",
    page_icon="🚀",
    layout="wide",
)

PageLoader.root = "aaaaa"


streamlit_superapp.run()
