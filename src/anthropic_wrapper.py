from anthropic import Anthropic
import os
from dotenv import load_dotenv


class AnthropicWrapper:
    load_dotenv()

    # Retrieve the API key from the environment variables
    api_key = os.getenv("ANTHROPIC_API_KEY")
    def __init__(self):
        self.client = Anthropic(api_key=api_key)     
        self.system_prompt = """Take the Answer paragraph and the relevant information that is included in the prompt and build the Answer based on the following structure. Wirth the Answer in Hebrew. 
            Step 1: Start with an emphatic general phrase related to the user's question. Manage the dialog as if you are a highly empathic social worker.
            Step 2: Described the Entitlement conditions (תנאים לזכאות): Described, based on the data the user provided, if the user is entitled to any kind of support or benefits. Mention any conditions / constraints / caveats that might be relevant to their situation.
            Step 3: Described what he is entitled to (למה אתם זכאי) : Described, based on the data the user provided, what he is entitled to. Describe any conditions that might be relevant to his situation and add a connection to calculators, if applicable.
            Step 4: Described how to exercise your entitlements  (כיצד לממש את הזכאות) : described the process, step by step, that the user needs to take to exercise his right and receive what he is entitled too. 
            Following that, ask if he has any follow-up questions or if you can help him with any new questions. """
    
    def create_prompt(self, document, query):
        return f"Query: {query}\nDocument: {document}"

    def generate_text(self, prompt, model="claude-3-haiku-20240307", max_tokens=1000, temperature=0):
        message = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        return message.content

