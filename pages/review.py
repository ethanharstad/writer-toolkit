import streamlit as st
from streamlit.logger import get_logger
from pydantic import BaseModel

from ai_client import client
from tools import tools, function_handler

LOGGER = get_logger(__name__)

class ProductOverview(BaseModel):
    product_name: str
    brand_name: str
    summary: str
    features: list[str]
    differentiators: list[str]
    similar_products: list[str]

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
        response = client.responses.parse(
            model=st.session_state["openai_model"],
            tools=tools,
            input=input_list,
            text_format=ProductOverview,
        )
        input_list += response.output
        tool_results = function_handler(response)
        for result in tool_results:
            input_list.append(result)
        else:
            st.session_state['product_context'] = response.output_parsed
        if iterations > 5:
            break

def run():
    st.title("Review Writer")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-5"
    
    with st.form("product_form"):
        st.markdown("## Product Definition")
        st.text_input("Product URL", key="product_url")
        st.form_submit_button("Go", on_click=analyze_product)
    
    if 'product_context' in st.session_state:
        with st.container():
            st.markdown(f"**Brand Name:** {st.session_state.product_context.brand_name}")
            st.markdown(f"**Product Name:** {st.session_state.product_context.product_name}")
            st.markdown(f"**Summary:** {st.session_state.product_context.summary}")
            col1, col2 = st.columns(2)
            with col1:
                features_text = "## Features\n"
                for feature in st.session_state.product_context.features:
                    features_text += f"- {feature}\n"
                st.markdown(features_text)
            with col2:
                differentiators_text = "### Differentiators\n"
                for differentiator in st.session_state.product_context.differentiators:
                    differentiators_text += f"- {differentiator}\n"
                st.markdown(differentiators_text)

if __name__ == "__main__":
    run()
