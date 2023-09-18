import telebot
from config import keys, TOKEN
from extensions import CurrencyConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'To get started, enter the command to the bot in the following format: \n<currency> \
<what currency to convert to> \
<amount> \
<see a list of all available currencies: /values >'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Number of parameters is incorrect.')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'User error\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Failed to process command\n{e}')
    else:
        text = f'Amount {amount} {quote} to {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
