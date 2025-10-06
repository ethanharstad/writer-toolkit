import pandas as pd
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
    questions: list[str]

class ReviewScoreElement(BaseModel):
    name: str
    score: int
    comment: str

class ReviewScore(BaseModel):
    components: list[ReviewScoreElement]

def analyze_product():
    iterations = 0
    input_list = [
        {
            "role": "developer",
            "content": "You are an expert assisting with writing a product review."
        },
        {
            "role": "user",
            "content": f"View the product page at this URL {st.session_state['product_url']}. Identify key features and differentiators for the product.",
        },
    ]
    while True:
        iterations += 1
        response = client.responses.parse(
            model="gpt-5",
            tools=tools,
            input=input_list,
            reasoning={"effort": "low"},
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

def suggest_categories():
    input_list = [
        {
            "role": "developer",
            "content": "You are an expert assisting with writing a product review. Given the context for the product in JSON format, come up with several categories to evaluate the product on. Only provide the name field for each category, do not populate any other fields.",
        },
        {
            "role": "user",
            "content": st.session_state['product_context'].model_dump_json(),
        },
    ]
    response = client.responses.parse(
        model="gpt-5-mini",
        input=input_list,
        text_format=ReviewScore,
    )
    st.session_state['categories'] = response.output_parsed

def run():
    st.title("Review Writer")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-5-mini"
    
    with st.form("product_form"):
        st.markdown("## Product Definition")
        st.text_input("Product URL", key="product_url")
        st.form_submit_button("Go", on_click=analyze_product)
    
    if 'product_context' in st.session_state:
        with st.container():
            st.markdown(f"**Brand Name:** {st.session_state.product_context.brand_name}")
            st.markdown(f"**Product Name:** {st.session_state.product_context.product_name}")
            st.markdown(f"**Summary:** {st.session_state.product_context.summary}")
            with st.expander("Features"):
                features_text = ""
                for feature in st.session_state.product_context.features:
                    features_text += f"- {feature}\n"
                st.markdown(features_text)
            with st.expander("Differentiators"):
                differentiators_text = ""
                for differentiator in st.session_state.product_context.differentiators:
                    differentiators_text += f"- {differentiator}\n"
                st.markdown(differentiators_text)
            with st.expander("FAQs"):
                text = ""
                for question in st.session_state.product_context.questions:
                    text += f"- {question}\n"
                st.markdown(text)
        
        with st.form("categories_form"):
            st.form_submit_button("Generate Categories", on_click=suggest_categories)
            if 'categories' in st.session_state:
                st.data_editor(
                    pd.DataFrame(
                        map(
                            lambda x: x.dict(),
                            st.session_state['categories'].components,
                        )
                    ),
                    hide_index=True,
                    column_config={
                        "name":  st.column_config.TextColumn(
                            "Category",
                            disabled=True,
                        ),
                        "score": st.column_config.NumberColumn(
                            "Your rating",
                            min_value=1,
                            max_value=10,
                            step=1,
                            format="%d ⭐",
                        ),
                        "comment": st.column_config.TextColumn(
                            "Comment",
                        ),
                    },
                    )

if __name__ == "__main__":
    run()
