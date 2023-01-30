import telebot
import openai
from deep_translator import GoogleTranslator
import APIs
import mes

openai.api_key = APIs.API_KEY_OPENAI  # Api ключ OpenAI
bot = telebot.TeleBot(APIs.API_KEY_TELEGRAM_BOT)  # Api ключ Telegram бота


@bot.message_handler(commands=['start', 'clear'])
def handle_message(message):
    print('Команда обнаружена')
    if message.text == '/clear':
        mes.mes = 'You: Are elephants really afraid of mice?\nComputer: No, elephants are not afraid of mice. Elephants are ' \
                  'actually quite tolerant of small animals and have been known to interact with them in a friendly manner.' \
                  '\nYou: Who don`t they like?\nComputer: ' \
                  'Elephants are generally not fond of large predators such as lions, tigers, and leopards. They can also become ' \
                  'agitated around humans if they feel threatened or scared.'
        bot.send_message(chat_id=message.from_user.id, text='Память бота очищена')
    elif message.text == '/start':
        f = open(f'Logs/{message.from_user.id}.txt', 'w+')
        f.write(mes.mes)
        bot.send_message(chat_id=message.from_user.id, text='Задавайте любые вопрысы!')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
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


bot.infinity_polling()
