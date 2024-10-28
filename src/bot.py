from openai import OpenAI
from telegram import Update
from telegram.ext import (
    filters,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ApplicationBuilder,
)
import schedule
import time
import os
from alingo_assistant import ALingoAssistant
from user_store import UserStore, UserPreference


# Load environment variables from .env file
def load_env():
    with open(".env") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


load_env()
# Read tokens from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

assistant = ALingoAssistant(api_key=OPENAI_API_KEY, id=ASSISTANT_ID)
store = UserStore()
store.load_from_json()
# client = OpenAI(api_key=OPENAI_API_KEY)
print("Saved user data:", store.get_size())

# State definitions for conversation
TIME, LANGUAGE, LEVEL, TOPIC, CONFIRM_SETTINGS, ANSWER = range(6)
TEST_RESPONSE = 99
# Dictionary to store user preferences
user_preferences = {}


# Function to start the bot and check previous settings
async def start(update: Update, context):
    user_id = update.message.from_user.id
    print(f"User ID: {user_id}")
    print(f"User exists: {store.get_user(user_id)}")
    print(store.get_size())
    if store.check_user_exists(user_id):
        print("User exists")
        preferences = store.get_user(user_id)
        message = (
            f"Last time you set the following preferences:\n"
            f"Time: {preferences.time} minutes\n"
            f"Language: {preferences.language}\n"
            f"Level: {preferences.level}\n"
            f"Topic: {preferences.topic}\n"
            "Do you want to keep these settings? (yes/no)"
        )
        await update.message.reply_text(message)
        return CONFIRM_SETTINGS

    else:
        store.add_user(user_id)
        await update.message.reply_text(
            "Welcome! How much time do you have for learning today (in minutes)?"
        )
        return TIME


async def confirm_settings(update: Update, context):
    response = update.message.text.lower()

    if response == "yes":
        # Use stored preferences
        await send_exercises(update, context)
        return ConversationHandler.END
    else:
        # Ask for new settings
        await update.message.reply_text(
            "How much time do you have for learning today (in minutes)?"
        )
        return TIME


async def get_time(update: Update, context):
    context.user_data["time"] = update.message.text
    await update.message.reply_text("What language do you want to learn?")
    return LANGUAGE


async def language(update: Update, context):
    context.user_data["language"] = update.message.text
    await update.message.reply_text("What level are you (A1-C2)?")
    return LEVEL


async def level(update: Update, context):
    context.user_data["level"] = update.message.text
    await update.message.reply_text(
        "Which topic would you like to learn today? (e.g., restaurant, directions, groceries)"
    )
    return TOPIC


async def topic(update: Update, context):
    context.user_data["topic"] = update.message.text
    # Save preferences
    user_id = update.message.from_user.id

    store.set_user_preference(
        user_id=user_id,
        time=context.user_data["time"],
        language=context.user_data["language"],
        level=context.user_data["level"],
        topic=context.user_data["topic"],
    )

    await send_exercises(update, context)
    return ANSWER


async def submit_answer(update: Update, context):
    user_id = update.message.from_user.id
    preferences = store.get_user(user_id)
    if not preferences:
        await update.message.reply_text(
            "Please set your preferences first using /start."
        )
        return
    print("Got user Prefrences, checking answers")
    # Save the user's answers
    answers = update.message.text
    prompt = f"Based on the given exercies, correct this answers: \n {answers} "
    result = await assistant.check_answer(prompt)
    # Calculate the score
    score = 100
    await update.message.reply_text(f"Your score: {score}%")
    await update.message.reply_text(result)
    # Ask the user to submit more answers
    await update.message.reply_text(
        "Submit more answers or type /next to get new exercises."
    )
    return ConversationHandler.END


async def send_exercises(update: Update, context):
    user_id = update.message.from_user.id
    if store.check_user_exists(user_id):
        preferences = store.get_user(user_id)
    else:
        await update.message.reply_text(
            "Please set your preferences first using /start."
        )
        return
    # Create prompt for OpenAI based on user input
    prompt = (
        f"Create a {preferences.time}-minute language learning exercise for {preferences.language} at {preferences.level} level "
        f"on the topic of {preferences.topic}. Include questions and tasks."
    )

    exercises = await assistant.send_msg(prompt)

    await update.message.reply_text(exercises)

    # Ask the user to submit answers later
    await update.message.reply_text(
        "Complete the exercises and submit your answers for scoring."
    )


async def next_questions(update: Update, context):
    user_id = update.message.from_user.id
    store.load_from_json()
    print(store.get_size())
    if store.get_user(user_id):
        await send_exercises(update, context)
    else:
        await update.message.reply_text(
            "Please set your preferences first using /start."
        )

    return ANSWER


async def show_commands(update: Update, context):
    commands = [
        "/start - Set your language learning preferences",
        "/next - Get the next set of exercises",
        "/help - Show available commands",
    ]
    await update.message.reply_text("\n".join(commands))


async def test(update: Update, context):
    response = update.message.text

    await update.message.reply_text("Write some text to test the response.")
    return TEST_RESPONSE


async def test_response(update: Update, context):
    response = update.message.text
    print(response)
    await update.message.reply_text(response)
    return ConversationHandler.END


# Reminder function
def send_reminder(context):
    chat_id = "YOUR_CHAT_ID"
    context.bot.send_message(
        chat_id=chat_id,
        text="Don't forget to practice your language skills today! Type /start to begin.",
    )


async def simpleStart(update: Update, context):
    await update.message.reply_text("Hello World")


if __name__ == "__main__":
    print("Starting bot...")
    print(f"env: {BOT_TOKEN}")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("next", next_questions),
            CommandHandler("help", show_commands),
            CommandHandler("test", test),
        ],
        states={
            CONFIRM_SETTINGS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_settings)
            ],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language)],
            LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, level)],
            TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topic)],
            ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, submit_answer)],
            TEST_RESPONSE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, test_response)
            ],
        },
        fallbacks=[],
    )
    app.add_handler(conv_handler)
    app.run_polling()

    # TODO: Scheduler stuff
