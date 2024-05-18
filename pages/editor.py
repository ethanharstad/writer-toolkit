import streamlit as st
from streamlit.logger import get_logger

from ai_client import client

LOGGER = get_logger(__name__)

def run():
    # Setup page
    st.set_page_config(layout="wide")
    st.title("Article Editor")

    # Setup state
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        option = st.selectbox(
            "OpenAI Model", (
                "gpt-3.5-turbo",
                "gpt-4",
                "gpt-4-32k",
                "gpt-4-turbo",
                "gpt-4o",
            ),
            key="openai_model",
        )

    col1, col2 = st.columns(2)

    with col1:
        # Display messages
        messages = st.container(height=500)
        with messages:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Prompt
        if prompt := st.chat_input("Message AI assistant"):
            # Add user message to history
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
            })
            
            # Display the message
            with messages:
                with st.chat_message("user"):
                    st.markdown(prompt)
            
                # Get response and display it
                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state["messages"]
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
            
            # Add the response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
            })
    
    with col2:
        st.text_area("Notes", key="notes", height=500)

if __name__ == "__main__":
    run()
