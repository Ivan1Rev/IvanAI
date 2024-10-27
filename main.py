import google.generativeai as genai
from telegram import ForceReply, Update
import logging
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('api_key')
TELEG_KEY = os.getenv('teleg_key')


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
genai.configure(api_key=SECRET_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
talk = True



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello {user.mention_html()}, I am an AI, I am here to help you complete your "
                                    f"mundane tasks",
        reply_markup=ForceReply(selective=True),
    )



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    await update.message.reply_html(f"Hello {user.mention_html()}, I am an AI, I am here to help you complete your "
                                    f"mundane tasks. Please ask me any question and I will try to answer them as well "
                                    f"as possible."
                                    f" Please write /ask then write your following question.")

async def AI (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = model.generate_content(update.message.text)
    print(response.text)

    await update.message.reply_html (response.text)



def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEG_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ask", AI))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
