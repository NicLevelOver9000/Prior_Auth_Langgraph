import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()


class LLMClient:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-01"
        )
        self.model = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    def chat(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
