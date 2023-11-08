import streamlit as st

from streamlit_superapp.state import State
from streamlit import session_state as ss


def main():
    text = State("text", default_value="")

    value = st.text_input("Text", value=text.initial_value, key=text.key)
    text.bind(value)
