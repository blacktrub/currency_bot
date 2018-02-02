import telebot

from utils import currency_api
from constants import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['usd'])
def usd_currency(message):
    usd_to_rub = currency_api.rub_to_usd()
    bot.reply_to(message, f'1 USD - {usd_to_rub} RUB')


@bot.message_handler(commands=['eur'])
def eur_currency(message):
    eur_to_rub = currency_api.rub_to_eur()
    bot.reply_to(message, f'1 EUR - {eur_to_rub} RUB')


bot.polling()
