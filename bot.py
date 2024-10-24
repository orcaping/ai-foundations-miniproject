import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import schedule
import time

# OpenAI and Telegram bot setup
openai.api_key = 'YOUR_OPENAI_API_KEY'
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# State definitions for conversation
TIME, LANGUAGE, LEVEL, TOPIC, CONFIRM_SETTINGS = range(5)

# Dictionary to store user preferences
user_preferences = {}

# Function to start the bot and check previous settings
def start(update, context):
    user_id = update.message.from_user.id

    # Check if the user has previous settings
    if user_id in user_preferences:
        preferences = user_preferences[user_id]
        message = (f"Last time you set the following preferences:\n"
                   f"Time: {preferences['time']} minutes\n"
                   f"Language: {preferences['language']}\n"
                   f"Level: {preferences['level']}\n"
                   f"Topic: {preferences['topic']}\n"
                   "Do you want to keep these settings? (yes/no)")
        update.message.reply_text(message)
        return CONFIRM_SETTINGS
    else:
        update.message.reply_text("Welcome! How much time do you have for learning today (in minutes)?")
        return TIME

def confirm_settings(update, context):
    response = update.message.text.lower()

    if response == 'yes':
        # Use stored preferences
        user_id = update.message.from_user.id
        preferences = user_preferences[user_id]
        send_exercises(update, context, preferences)
        return ConversationHandler.END
    else:
        # Ask for new settings
        update.message.reply_text("How much time do you have for learning today (in minutes)?")
        return TIME

def time(update, context):
    context.user_data['time'] = update.message.text
    update.message.reply_text("What language do you want to learn?")
    return LANGUAGE

def language(update, context):
    context.user_data['language'] = update.message.text
    update.message.reply_text("What level are you (A1-C2)?")
    return LEVEL

def level(update, context):
    context.user_data['level'] = update.message.text
    update.message.reply_text("Which topic would you like to learn today? (e.g., restaurant, directions, groceries)")
    return TOPIC

def topic(update, context):
    context.user_data['topic'] = update.message.text
    # Save preferences
    user_id = update.message.from_user.id
    user_preferences[user_id] = {
        'time': context.user_data['time'],
        'language': context.user_data['language'],
        'level': context.user_data['level'],
        'topic': context.user_data['topic']
    }

    send_exercises(update, context, user_preferences[user_id])
    return ConversationHandler.END

def send_exercises(update, context, preferences):
    time = preferences['time']
    language = preferences['language']
    level = preferences['level']
    topic = preferences['topic']

    # Create prompt for OpenAI based on user input
    prompt = (f"Create a {time}-minute language learning exercise for {language} at {level} level "
              f"on the topic of {topic}. Include questions and tasks.")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    
    # Send OpenAI response to the user
    exercises = response['choices'][0]['text']
    update.message.reply_text(exercises)
    
    # Ask the user to submit answers later
    update.message.reply_text("Complete the exercises and submit your answers for scoring.")

# Reminder function
def send_reminder(context):
    chat_id = 'YOUR_CHAT_ID'
    context.bot.send_message(chat_id=chat_id, text="Don't forget to practice your language skills today! Type /start to begin.")

# Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONFIRM_SETTINGS: [MessageHandler(Filters.text & ~Filters.command, confirm_settings)],
            TIME: [MessageHandler(Filters.text & ~Filters.command, time)],
            LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, language)],
            LEVEL: [MessageHandler(Filters.text & ~Filters.command, level)],
            TOPIC: [MessageHandler(Filters.text & ~Filters.command, topic)],
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    # Schedule daily reminder at 10:00 AM
    schedule.every().day.at("10:00").do(send_reminder, context=updater.bot)

    # Start the bot
    updater.start_polling()
    
    # Keep the bot running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
