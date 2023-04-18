import os
from dotenv import load_dotenv
import openai
from retry import retry


class OpenAiAPI():
    def __init__(self):
        load_dotenv()

        self.ai = openai
        self.ai.api_key = os.getenv("AI_KEY")

        self.model = os.getenv("MODEL")
        self.max_tokens = os.getenv("MAX_TOKENS")
    
    @retry(delay=1, backoff=2, max_delay=120, tries=3)
    async def _ai_moderation_call_retry(self, content):
        response = await self.ai.Moderation.acreate(
            input=content
        )
        return response
    
    async def check_content_safety(self, content: str, category: list):

        response = await self._ai_moderation_call_retry(
            content=content
        )

        response_results = response['results'][0]

        for i in category:
            if response_results['categories'][i]:
                return True

        return False
    
    @retry(delay=1, backoff=2, max_delay=120, tries=3)
    async def _ai_chat_call_retry(self, messages):
        """
        Retry-function for the chatgpt-call.

        Args:
            messages (dict): Contains all the messages
            that needs to be send to the api.

        Returns:
            AsyncGenerator: Response from the api.
        """

        response = await self.ai.ChatCompletion.acreate(
            model=self.model,
            messages=messages,
            max_tokens=int(self.max_tokens)
        )

        return response
    
    async def ai_chat_call(self, messages):
        response = await self._ai_chat_call_retry(
            messages=messages
        )
        return response
