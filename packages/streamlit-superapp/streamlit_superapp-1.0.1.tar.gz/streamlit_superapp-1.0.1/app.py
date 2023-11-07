import streamlit_superapp
import streamlit as st

from streamlit_superapp.navigation import Navigation

st.set_page_config(
    page_title="Streamlit Super App",
    page_icon="🚀",
    layout="wide",
)


def get_page_index(path, pages):
    index = -1

    for i, page in enumerate(pages):
        if page.path == path:
            return i
    return index


def search(page):
    pages = page.children

    current_path = Navigation.current_path()

    # check if current_path exists in pages

    index = get_page_index(current_path, pages)

    if index >= 0:
        page = st.selectbox("Search", options=pages, index=index)

        if page is not None:
            next_index = get_page_index(page.path, pages)

            if index != next_index:
                Navigation.go(page)


with st.sidebar:
    search(Navigation.root())


streamlit_superapp.run(hide_home_button=True, hide_back_button=True)
