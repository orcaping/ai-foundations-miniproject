from openai import OpenAI


class ALingoAssistant:
    assistant = None
    thread = None

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
                self.thread = self.client.beta.threads.create()
            except Exception as e:
                print(f"Failed to load assistant: {e}")
                return False

        return True

    async def send_msg(self, msg):
        t_msg = self.client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=msg
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        if run.status == "completed":
            reply = self.client.beta.threads.messages.list(thread_id=self.thread.id)

        return reply.data[0].content[0].text.value
