import json
import streamlit as st
from streamlit.logger import get_logger

from ai_client import client

LOGGER = get_logger(__name__)


def generate_titles():
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an expert in writing SEO optimized blog posts. Output JSON."},
            {"role": "user", "content": f"Generate ten potential titles for an article with this description: {st.session_state['description_prompt']}"},
        ]
    )
    titles = json.loads(response.choices[0].message.content)['titles']
    st.session_state['title_options'] = titles

def generate_description():
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an expert in writing SEO optimized blog posts. Output JSON."},
            {"role": "user", "content": "Generate a meta description for an article from the following information. The description should be about 150 characters long."},
            {"role": "user", "content": f"Title: {st.session_state['title']}"},
            {"role": "user", "content": f"Inspiration: {st.session_state['description_prompt']}"},
        ]
    )
    description = json.loads(response.choices[0].message.content)['meta_description']
    st.session_state['description'] = description

def generate_outline():
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an expert in writing SEO optimized blog posts. Do not generate any additional text than what is asked for."},
            {"role": "user", "content": "Generate an outline for an article from the following information."},
            {"role": "user", "content": f"Title: {st.session_state['title']}"},
            {"role": "user", "content": f"Inspiration: {st.session_state['description_prompt']}"},
            {"role": "user", "content": f"Meta Description: {st.session_state['description']}"},
        ]
    )
    outline = response.choices[0].message.content
    st.session_state["outline"] = outline

def run():
    st.title("Article Writer")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    with st.form("topic_form"):
        st.markdown("## Article Inspiration")
        st.text_area("Inspiration", key="description_prompt")
        st.form_submit_button("Go", on_click=generate_titles)
    
    if 'title_options' in st.session_state:
        with st.form("title_form"):
            st.markdown("## Article Title\n\nSelect an article title with help from these suggestions.")
            st.markdown("\n".join(f"- {t}" for t in st.session_state['title_options']))
            st.text_input("Title", key="title")
            st.form_submit_button("Go", on_click=generate_description)
    
    if 'description' in st.session_state:
        with st.form("description_form"):
            st.markdown("## Article Description\n\nTweak the meta description of your article.")
            st.text_area("Description", key="description")
            st.form_submit_button("Go", on_click=generate_outline)
    
    if 'outline' in st.session_state:
        st.markdown(st.session_state['outline'])


if __name__ == "__main__":
    run()
