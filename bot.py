import openai
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


# Load environment variables from .env file
def load_env():
    with open(".env") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


# Read tokens from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# State definitions for conversation
TIME, LANGUAGE, LEVEL, TOPIC, CONFIRM_SETTINGS = range(5)

# Dictionary to store user preferences
user_preferences = {}


# Function to start the bot and check previous settings
async def start(update: Update, context):
    user_id = update.message.from_user.id

    # Check if the user has previous settings
    if user_id in user_preferences:
        preferences = user_preferences[user_id]
        message = (
            f"Last time you set the following preferences:\n"
            f"Time: {preferences['time']} minutes\n"
            f"Language: {preferences['language']}\n"
            f"Level: {preferences['level']}\n"
            f"Topic: {preferences['topic']}\n"
            "Do you want to keep these settings? (yes/no)"
        )
        await update.message.reply_text(message)
        return CONFIRM_SETTINGS
    else:
        await update.message.reply_text(
            "Welcome! How much time do you have for learning today (in minutes)?"
        )
        return TIME


async def confirm_settings(update: Update, context):
    response = update.message.text.lower()

    if response == "yes":
        # Use stored preferences
        user_id = update.message.from_user.id
        preferences = user_preferences[user_id]
        send_exercises(update, context, preferences)
        return ConversationHandler.END
    else:
        # Ask for new settings
        await update.message.reply_text(
            "How much time do you have for learning today (in minutes)?"
        )
        return TIME


async def time(update: Update, context):
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
    user_preferences[user_id] = {
        "time": context.user_data["time"],
        "language": context.user_data["language"],
        "level": context.user_data["level"],
        "topic": context.user_data["topic"],
    }

    await send_exercises(update, context, user_preferences[user_id])
    return ConversationHandler.END


async def send_exercises(update: Update, context, preferences):
    time = preferences["time"]
    language = preferences["language"]
    level = preferences["level"]
    topic = preferences["topic"]

    # Create prompt for OpenAI based on user input
    prompt = (
        f"Create a {time}-minute language learning exercise for {language} at {level} level "
        f"on the topic of {topic}. Include questions and tasks."
    )

    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=500
    )

    # Send OpenAI response to the user
    exercises = response["choices"][0]["text"]
    await update.message.reply_text(exercises)

    # Ask the user to submit answers later
    await update.message.reply_text(
        "Complete the exercises and submit your answers for scoring."
    )


# Reminder function
def send_reminder(context):
    chat_id = "YOUR_CHAT_ID"
    context.bot.send_message(
        chat_id=chat_id,
        text="Don't forget to practice your language skills today! Type /start to begin.",
    )


async def simpleStart(update: Update, context):
    await update.message.reply_text("Hello World")


# Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CONFIRM_SETTINGS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_settings)
            ],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, time)],
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language)],
            LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, level)],
            TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topic)],
        },
        fallbacks=[],
    )

    # Schedule daily reminder at 10:00 AM
    # schedule.every().day.at("10:00").do(send_reminder, context=app.bot)

    # Start the bot
    await app.run_polling()

    # Keep the bot running
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    print("Starting bot...")
    print(f"env: {BOT_TOKEN}")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CONFIRM_SETTINGS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_settings)
            ],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, time)],
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language)],
            LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, level)],
            TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topic)],
        },
        fallbacks=[],
    )
    app.add_handler(conv_handler)
    app.run_polling()

    # TODO: Scheduler stuff
