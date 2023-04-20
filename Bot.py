import telebot
from config import TOKEN, currencies
from utils import Convertor, ConvertionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = 'Вас приветствует бот-конвертер валют! Отправьте мне сообщение в виде: <Имя исходной валюты > \
<Имя валюты, в которую перевести > \
<Введите сумму для конвертации> \n Чтобы увидеть список доступных валют введите: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Я могу конвертировать только эти валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvertionException('Ошибка: Неверное количество параметров (Пример: Валюта1, Валюта2, Количество) ')
        quote, base, amount = values
        total_base = Convertor.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base)*float(amount)}'
        bot.send_message(message.chat.id, text)
bot.polling(none_stop=True)



