import json
import streamlit as st
from streamlit.logger import get_logger

from ai_client import client
from tools import tools, function_handler

LOGGER = get_logger(__name__)


def analyze_product():
    iterations = 0
    input_list = [
        {
            "role": "user",
            "content": f"View the product page at this URL {st.session_state['product_url']}. Identify key features and differentiators for the product.",
        }
    ]
    while True:
        iterations += 1
        response = client.responses.create(
            model=st.session_state["openai_model"],
            tools=tools,
            input=input_list,
        )
        input_list += response.output
        tool_results = function_handler(response)
        for result in tool_results:
            input_list.append(result)
        else:
            st.session_state['product_context'] = response.output_text
        if iterations > 5:
            break

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
    st.title("Review Writer")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-5"
    
    with st.form("product_form"):
        st.markdown("## Product Definition")
        st.text_input("Product URL", key="product_url")
        st.form_submit_button("Go", on_click=analyze_product)
    
    if 'product_context' in st.session_state:
        with st.form("product_context_form"):
            st.markdown(st.session_state["product_context"])

if __name__ == "__main__":
    run()
