import streamlit as st

from streamlit_superapp.typing import Page, Navigation


def main(page: Page, navigation: Navigation):
    st.write("Hello World!")
    st.write("This is a demo page.")
    st.write("You can edit this file and change the content.")
    st.write("You can also add new pages to the app.")
    st.write("Check out the documentation to learn more.")
