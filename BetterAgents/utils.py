import os 
from dotenv import load_dotenv
load_dotenv()

from langchain.llms import OpenAI

llm = OpenAI(os.getenv("OPENAI_API_KEY"))