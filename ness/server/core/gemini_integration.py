import asyncio
import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv
from utils.prompt_loader import load_all_prompts  # adjust path if needed

logger = logging.getLogger(__name__)


class GeminiIntegration:
    """
    GeminiIntegration provides a wrapper around the Gemini generative AI model.

    Handles prompt loading, session management, and response generation.
    """

    MAX_SESSION_TOKENS = 128_000

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.token_count = 0
        self.prompts = load_all_prompts()
        self.chat = None

        logger.info("GeminiIntegration initialized successfully.")

    def _get_prompt_by_type(self, intent: str = None) -> str:
        if not intent:
            return None
        prompt = self.prompts.get(intent.lower())
        if not prompt:
            raise ValueError(f"No prompt found for intent: {intent}")
        return prompt

    def _reset_chat(self, initial_prompt: str = None) -> None:
        system_prompt = self._get_prompt_by_type("system")
        history = [{"role": "user", "parts": [system_prompt]}]
        if initial_prompt:
            history.append({"role": "user", "parts": [initial_prompt]})
        self.chat = self.model.start_chat(history=history)
        self.token_count = 0
        logger.info("Chat session reset with system context.")

    async def generate_response(self, user_message: str, intent: str = None) -> str:
        """
        Generates a response using Gemini based on user input and intent.

        Args:
            user_message (str): User's message.
            intent (str): Optional, defines the prompt context to load.

        Returns:
            str: Model's response or an error message.
        """
        if self.token_count > self.MAX_SESSION_TOKENS or self.chat is None:
            logger.warning("Token limit hit or chat uninitialized. Resetting chat...")
            initial_prompt = self._get_prompt_by_type(intent)
            self._reset_chat(initial_prompt)

        try:
            response = await asyncio.to_thread(
                self.chat.send_message, {"role": "user", "parts": [user_message]}
            )

            response_text = response.text.strip()
            self.token_count += len(user_message.split()) + len(response_text.split())
            logger.info(f"Generated response. Tokens used: {self.token_count}")
            return response_text

        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return "Failed to generate a response. Please try again."
