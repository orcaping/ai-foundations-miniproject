from openai import OpenAI


class ALingoAssistant:
    assistant = None
    thread = None

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_user_preferences",
                "description": "Get Preferences of the current user'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's ID.",
                        },
                    },
                    "required": ["user_id"],
                    "additionalProperties": False,
                },
            },
        }
    ]

    def __init__(self, api_key, id):
        self.client = OpenAI(api_key=api_key)
        self.id = id

    async def load_assistant(self):
        if self.assistant:
            return True
        else:
            try:
                ass = self.client.beta.assistants.retrieve(assistant_id=self.id)
                self.assistant = ass
                ## creates thread, maybe save threads and call existing ones.
                self.thread = self.client.beta.threads.create()
            except Exception as e:
                print(f"Failed to load assistant: {e}")
                return False

        return True

    async def send_msg(self, msg):
        ## Creates message
        t_msg = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=msg
        )
        ## Creates run
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        if run.status == "completed":
            reply = self.client.beta.threads.messages.list(thread_id=self.thread.id)

        return reply.data[0].content[0].text.value