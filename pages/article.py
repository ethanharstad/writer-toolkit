import streamlit as st
from streamlit.logger import get_logger

from ai_client import client

LOGGER = get_logger(__name__)


def generate_titles():
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": "You are an expert in writing SEO optimized blog posts."},
            {"role": "user", "content": ""},
        ]
    )

def run():
    st.title("Article Writer")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    with st.form("topic_form"):
        st.text_area("Description", key="description_prompt")
        st.form_submit_button("Go", on_click=generate_titles)


if __name__ == "__main__":
    run()
