from g4f.client import Client
from DB.database import db


class ConversationManager:
    def __init__(self):
        self.db = db
        self.client = Client()

    async def get_response(self, user_id, user_message):
        await self.db.add_message(user_id, "user", user_message)
        history = await self.db.get_history(user_id)

        if not any(m["role"] == "system" for m in history):
            history.insert(0, {"role": "system", "content": "You are a helpful assistant."})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
            web_search=False
        )
        assistant_response = response.choices[0].message.content
        await self.db.add_message(user_id, "assistant", assistant_response)
        return assistant_response


conversation = ConversationManager()
