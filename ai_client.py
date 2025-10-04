import os
from openai import OpenAI
import streamlit as st

API_KEY = st.secrets["OPENAI_KEY"]

client = OpenAI(api_key=API_KEY)
