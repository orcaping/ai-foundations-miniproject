import os
import sys
import asyncio
from alingo_assistant import ALingoAssistant


# Load environment variables from .env file
def load_env():
    with open(".env") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


# Read tokens from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ASSISTANT_ID = os.getenv("ASSISTANT_ID")


async def run():
    a = ALingoAssistant(api_key=OPENAI_API_KEY, id=ASSISTANT_ID)
    print(f"Assistant id: {ASSISTANT_ID}")
    await a.load_assistant()
    res = input("Ask me something:")
    try:
        while res != "exit":
            reply = await a.send_msg(res)
            print(reply)
            res = input("Ask me something:")
    except Exception as e:
        print(f"Failed to send message: {e}")
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    load_env()
    print(OPENAI_API_KEY)
    asyncio.run(run())
