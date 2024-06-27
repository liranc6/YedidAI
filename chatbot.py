import ast  # for converting embeddings saved as strings back to arrays
from openai import OpenAI # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
import os # for getting API token from env variable OPENAI_API_KEY
from scipy import spatial  # for calculating vector similarities for search
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# an example question about the 2022 Olympics
SYSTEM_MESSAGE = 'You answer questions about the 2022 Winter Olympics.'
USER_QUERY = 'Which athletes won the gold medal in curling at the 2022 Winter Olympics?'

response = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': SYSTEM_MESSAGE},
        {'role': 'user', 'content': USER_QUERY},
    ],
    model=os.environ.get("GPT_MODEL"),
    temperature=0,
)

print(response.choices[0].message.content)