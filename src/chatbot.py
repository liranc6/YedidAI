import ast  # for converting embeddings saved as strings back to arrays
from openai import OpenAI # for calling the OpenAI API
import openai
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
import os # for getting API token from env variable OPENAI_API_KEY
from scipy import spatial  # for calculating vector similarities for search
from dotenv import load_dotenv
load_dotenv()
from openai_tools import functions, SYSTEM_PROMPT


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# an example question about the 2022 Olympics
SYSTEM_MESSAGE = SYSTEM_PROMPT.format()


class ChatApp:
    def __init__(self):
        # Setting the API key to use the OpenAI API

        self.model = os.getenv("GPT_MODEL")
        self.messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
        ]
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.opening_assistant_message = client.chat.completions.create(
            model= self.model,
            messages=self.messages,

        )
        self.opening_assistant_message_text = self.opening_assistant_message.choices[0].message.content
        self.messages.append({"role": "assistant", "content": self.opening_assistant_message_text})


    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model= self.model,
            messages=self.messages,
            functions= functions,
            function_call= "auto"
        )
        self.messages.append({"role": "user", "content": message})
        response_text = response.choices[0].message.content
        if response_text:
            self.messages.append({"role": "assistant", "content": response_text})
            print(f"SYSTEM: {response_text}")

        function_call = response.choices[0].message.function_call
        arguments = None
        if function_call:
            if function_call.name == "end_conversation":
                reason = ast.literal_eval(function_call.arguments).get("reason")
                conversation_summary = ast.literal_eval(function_call.arguments).get("conversation_summary")
                print("Completion Reason: ", arguments)
                print("Conversation summary: ", conversation_summary)

        return arguments





if __name__ == '__main__':
    chat_app = ChatApp()
    print(f"SYSTEM: {chat_app.opening_assistant_message_text}")
    for i in range(7):
        text = input("USER: ")
        if chat_app.chat(text):
            break