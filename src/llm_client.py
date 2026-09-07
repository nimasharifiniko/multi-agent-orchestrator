"""
LLM Client - Centralized layer for all AI model interactions.
All agents use this client to communicate with the LLM.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Handles all communication with the LLM provider."""

    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("LLM_BASE_URL"),
            api_key=os.getenv("LLM_API_KEY"),
        )
        self.model = os.getenv("LLM_MODEL")

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a message to the LLM and return the response.

        Args:
            system_prompt: The role/instruction for the AI.
            user_prompt: The actual task or question.

        Returns:
            The LLM's response as a string.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"LLM_ERROR: {str(e)}"


# Global instance - all agents will use this
llm = LLMClient()