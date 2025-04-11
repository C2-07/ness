import asyncio
import logging
import os
import json

import google.generativeai as genai
from dotenv import load_dotenv
from utils.prompt_loader import load_prompt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
)
logger = logging.getLogger(__name__)


class GeminiThink:
    """
    GeminiThink provides filter, sort and extract user extents from user's request
    """

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-lite")
        self.system_prompt = load_prompt("GeminiThink")
        self.history = [{"role": "user", "parts": [self.system_prompt]}]
        self.chat = self.model.start_chat(history=self.history)

        logger.info("GeminiThink initialized successfully.")

    async def think(self, user_message):
        """_summary_

        Args:
            user_message (_type_): _description_
        """

        try:
            response = await asyncio.to_thread(
                self.chat.send_message, {"role": "user", "parts": [user_message]}
            )
            response = response.text.strip()
            logger.info("GeminiThink: Generated response.")
            logger.info("GeminiThink: Converting Response to Json Format")
            try:
                response = json.loads(response)
                logger.info("GeminiThink: Converted Response to Json Format")
            except Exception as e:
                logger.info(f"Failed to to Convert Response to Json: {e}")
                pass
            return response
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return f"Failed to generate a response: {e}"
