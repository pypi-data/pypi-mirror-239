import streamlit as st
from streamlit import session_state as ss
from streamlit_superapp.state import State

from streamlit_superapp.typing import Navigation

NAME = "Murilove"
DESCRIPTION = "Página do murilove"
ICON = "🌍"


def main(page, navigation: Navigation):
    st.write("Hello Murilove")

    state = State("name", "")

    name = st.text_input("Name", value=state.initial_value, key=state.key)

    previous_name = state.bind(name)

    st.write("hehe")

    st.write("ihuuuuu")
