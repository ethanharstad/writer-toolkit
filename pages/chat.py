import streamlit as st
from streamlit.logger import get_logger

from ai_client import client

LOGGER = get_logger(__name__)


def run():
    st.title("Chat")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
        })
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })


if __name__ == "__main__":
    run()
