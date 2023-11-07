import streamlit as st

from streamlit_superapp.state import State
from streamlit import session_state as ss

a = 0


def main():
    global a
    a += 1
    print("render:", a)
    print("    page_changed:", ss["page_changed"])
    text = State("text", default_value="")

    value = st.text_input("Text", value=text.initial_value, key=text.key)
    text.bind(value)
