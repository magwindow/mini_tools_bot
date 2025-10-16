import os
import logging
from dotenv import load_dotenv

load_dotenv()

from telegram import __version__ as TG_VER
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from filters.text import BadText
from messages.words import BAD_WORDS
from messages import rbc_news, news_3d_news, exchange_rates

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


async def clean_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for i in update.message.text.split(" "):
        if i in BAD_WORDS:
            await update.message.reply_text("Не ругайся матом в прямом эфире!")
            await update.message.delete()


# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    message = (f"Привет {user.mention_html()}!\nЧтобы узнать новости, напиши в чат новости или news.\n"
               f"Чтобы узнать курсы валют, напиши курсы валют или exchange.")
    await update.message.reply_html(message, reply_markup=ForceReply(selective=True))


async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and update.message.text.lower() in ("новости", "news"):
        await update.message.reply_text("\n\n".join(rbc_news.get_rbc_news()))
        await update.message.reply_text("\n\n".join(news_3d_news.get_3dnews_news()))
    elif update.message.text and update.message.text.lower() in ("курсы валют", "exchange"):
        await update.message.reply_text("\n\n".join(exchange_rates.get_exchange_rates()))


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message
    application.add_handler(MessageHandler(BadText() & ~filters.COMMAND, clean_bad_words))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, health_check))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
