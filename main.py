import telebot
import openai
from deep_translator import GoogleTranslator
import APIs
import mes

openai.api_key = APIs.API_KEY_OPENAI #Api ключ OpenAI

bot = telebot.TeleBot(APIs.API_KEY_TELEGRAM_BOT) #Api ключ Telrgram бота

resp = openai.Completion.create(
    model="text-davinci-003",
    prompt=mes.mes,
    temperature=0.5,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.0,
    stop=['You:']
        )
mes.mes = mes.mes + resp['choices'][0]['text']
print("Бот запущен")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text[0] == '/':
        print('Команда обнаружена')
        if message.text == '/clear':
            mes.mes = 'You: Are elephants really afraid of mice?\nComputer: No, elephants are not afraid of mice. Elephants are actually quite tolerant of small animals and have been known to interact with them in a friendly manner.\nYou: Who don`t they like?\nComputer:'
            resp = openai.Completion.create(
                model="text-davinci-003",
                prompt=mes.mes,
                temperature=0.5,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.0,
                stop=['You:']
            )
            mes.mes = mes.mes + resp['choices'][0]['text']
            bot.send_message(chat_id=message.from_user.id, text='Память бота очищена')
        elif message.text == '/start':
            bot.send_message(chat_id=message.from_user.id, text='Приятного пользования ботом! Задавайте любые вопрысы!')
        else:
            bot.send_message(chat_id=message.from_user.id, text='Неизвестная команда')
    else:
        mes.mes = mes.mes + '\nYou: ' + message.text + '\nComputer:'
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=mes.mes,
                temperature=0.5,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.0,
                stop=['You:']
            )
            bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
            bot.send_message(chat_id=message.from_user.id,
                             text=GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
            mes.mes = mes.mes + response['choices'][0]['text']
            print(mes.mes)
        except:
            print(mes.mes)
            bot.send_message(chat_id=message.from_user.id, text='Ошибка')


bot.polling(none_stop=True, interval=0)
