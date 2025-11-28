import sys
import django
import os
from pathlib import Path

# Add parent directory to Python path so Django can find smart_bot module
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from django.conf import settings
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_bot.settings')
django.setup()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Smart Bot.")

def main():
    TOKEN = settings.BOT_TOKEN
    if not TOKEN:
        print("Error: BOT_TOKEN environment variable is not set!")
        sys.exit(1)
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))

    print("Bot started. Polling...")
    app.run_polling()

if __name__ == "__main__":
    main()