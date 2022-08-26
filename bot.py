## Telegram BOT ##
import logging, gsheet, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))

def start(update, context):
    update.message.reply_text(
    """
    Hai,
    Welcome to the Monitor BOT by Yein
    The command as follow:
    /menu
    /help
    """
    )

def help(update, context):
    update.message.reply_text('Call the helpline +60137594904')

def menu(update, context):
    update.message.reply_text("""
    MAIN MENU
    Click to display data
    /latest
    /today
    /yesterday
    /7days
    """)

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def latest(update, context):
    dl = gsheet.display_latest()
    update.message.reply_text(
    """
    Today date is: {}
    Time: {}
    The PIC for today: {}
    Temperature: {}
    Humidity: {}
    """.format(dl[0], dl[1], dl[2], dl[3], dl[4])
    )


def today(update, context):
    gsheet.get_specify_date(gsheet.today)
    update.message.reply_text(
    """
    Today date is: {}
    The PIC for today: {}
    The Averange Temperature: {:.2f}
    The Averange Humidity: {:.2f}
    """.format(gsheet.today_data[0][0], gsheet.today_data[0][2], gsheet.average()['Temperature'], gsheet.average()['Humidity'])
    )
    gsheet.today_data.clear()

def yesterday(update, context):
    gsheet.get_specify_date(gsheet.yesterday)
    update.message.reply_text(
    """
    Yesterday date is: {}
    The PIC for Yesterday: {}
    The Averange Temperature: {:.2f}
    The Averange Humidity: {:.2f}
    """.format(gsheet.today_data[0][0], gsheet.today_data[0][2], gsheet.average()['Temperature'], gsheet.average()['Humidity'])
    )
    gsheet.today_data.clear()
    
# Calculate data for 7 days
def seven_day(update, context):
    update.message.reply_text("""
    Please add your own algorithm
    """)

# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "{}" caused error "{}"'.format(update, context.error))

def main():
    """Start the bot."""
    TOKEN = "5425406766:AAEzQ2Ol_rqdASl6_s9Ov1VPWlVaNf_397c"
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("today", today))
    dp.add_handler(CommandHandler("latest", latest))
    dp.add_handler(CommandHandler("yesterday", yesterday))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()

# if __name__ == '__main__':
#     main()