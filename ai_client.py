import os
from openai import OpenAI

API_KEY = os.environ["STRAWBERRY_PATCH_AI_KEY"]

client = OpenAI(api_key=API_KEY)
