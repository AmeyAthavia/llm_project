from google import genai
from ai.base import AIBase
import os

class GeminiAI(AIBase):
    def __init__(self, api_key: str, system_prompt: str = None):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.client = genai.Client(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        if self.system_prompt:
            prompt = f"{self.system_prompt}\n\n{prompt}"
        print('== final prompt sent to model ==', prompt)
        response = self.client.models.generate_content(model = 'gemini-3-flash-preview',
                                                    contents=prompt)
        return response.text