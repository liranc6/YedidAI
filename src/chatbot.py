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
        # self.messages.append({"role": "assistant", "content": self.opening_assistant_message_text})
        self.messages.append({"role": "assistant", "content": "הי, אני ישראלה ואני יכולה לעזור לך לקבל את מה שמגיע לך מהמדינה. בבקשה ספר לי על עצמך"})


    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model= self.model,
            messages=self.messages,

        )
        #self.messages.append({"role": "user", "content": message})
        response_text = response.choices[0].message.content
        if response_text:
            self.messages.append({"role": "assistant", "content": response_text})
            return response_text
            print(f"SYSTEM: {response_text[::-1]}")

        # function_call = response.choices[0].message.function_call
        # arguments = None
        # if function_call:
        #     if function_call.name == "end_conversation":
        #         reason = ast.literal_eval(function_call.arguments).get("reason")
        #         print("Completion Reason: ", arguments)


        return None

    def end_conversation(self):
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            functions=functions,
            function_call={'name': "get_conversation_summary"}
        )
        return response


def conversation_iterator(num_messages):
    chat_app = ChatApp()
    print(f"SYSTEM: {chat_app.opening_assistant_message_text[::-1]}")
    for i in range(num_messages//2):
        user_text = input("USER: ")
        yield user_text
        system_text = chat_app.chat(user_text)
        yield system_text

    chat_app.chat("Summarize the details about the user that are relevant for checking which rights he has. The summary should be in Hebrew. begin your summary with the prefix SUMMARY: ")




if __name__ == '__main__':
    # chat_app = ChatApp()
    # print(f"SYSTEM: {chat_app.opening_assistant_message_text[::-1]}")
    # for i in range(1):
    #     text = input("USER: ")
    #     if chat_app.chat(text):
    #         break
    chat_app.chat("Summarize the details about the user that are relevant for checking which rights he has. The summary should be in Hebrew. begin your summary with the prefix SUMMARY: ")

