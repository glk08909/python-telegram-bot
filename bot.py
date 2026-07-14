import logging
import os
from typing import Optional

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging to see errors in the VS Code terminal
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def get_token() -> Optional[str]:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        return token

    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        with open(env_file, encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("TELEGRAM_BOT_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    return None


# Define what happens when a user types /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your VS Code bot. How can I help you today?")


# Define what happens when a user sends a normal text message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_received = update.message.text
    await update.message.reply_text(f"You said11: {text_received}")


def main():
    TOKEN = get_token()
    if not TOKEN:
        print("Bot token not found. Set the TELEGRAM_BOT_TOKEN environment variable or add it to a .env file.")
        return

    # Build the bot application
    app = Application.builder().token(TOKEN).build()

    # Register the command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot and keep it running
    print("Bot is starting up... Press Ctrl+C in VS Code to stop.")
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()
