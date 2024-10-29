from openai import OpenAI


class ALingoAssistant:
    assistant = None
    thread = None
    role = "user"

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
        self.initialized = False

    async def load_assistant(self):
        if self.assistant:
            return True
        else:
            try:
                ass = self.client.beta.assistants.retrieve(assistant_id=self.id)
                self.assistant = ass
                ## creates thread, maybe save threads and call existing ones.
                self.thread = self.client.beta.threads.create()
                self.initialized = True
            except Exception as e:
                print(f"Failed to load assistant: {e}")
                self.initialized = False
                return False

        return True

    async def send_msg(self, msg):
        if not self.initialized:
            await self.load_assistant()
        ## Creates message
        t_msg = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role=self.role, content=msg
        )
        ## Creates run
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        if run.status == "completed":
            reply = self.client.beta.threads.messages.list(thread_id=self.thread.id)

        return reply.data[0].content[0].text.value

    async def check_answer(self, msg):
        t_msg = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role=self.role, content=msg
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        if run.status == "completed":
            reply = self.client.beta.threads.messages.list(thread_id=self.thread.id)

        return reply.data[0].content[0].text.value
