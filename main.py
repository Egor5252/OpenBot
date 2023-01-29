import telebot
import openai
from deep_translator import GoogleTranslator
import APIs # Файл APIs.py, где хранятсямои API ключи
import mes

openai.api_key = APIs.API_KEY_OPENAI #Api ключ OpenAI

bot = telebot.TeleBot(APIs.API_KEY_TELEGRAM_BOT) #Api ключ Telrgram бота

resp = openai.Completion.create(           # В этом блоке кода OpenAI учится синтаксису ответов на вопросы
    model="text-davinci-003",
    prompt=mes.mes, # mes.py - это файл, содержащий логи переписки с ботом, в начале там хранится обучение бота на примере вопросов о слонах
    temperature=0.5,
    max_tokens=1000, # Это общее количество токенов, которое доступно боту для ответа на вопрос.
                     # Для понимаия ботом контекста неообходимо накапливать прошлые вопросы и ответы.
                     # Всего доступно чуть больше 4000 токинов. Поэтому я ограничил число токенов для ответа бота в размере 1000
                     # Получается вы можете накопить не меньше 3000 токенов для вопросов боту и ответов на старые вопросы.
                     # Один токен состовляет примерно 4 символа на английском языке (информация с сайта https://beta.openai.com/playground)
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.0,
    stop=['You:']
        )
mes.mes = mes.mes + resp['choices'][0]['text']
print("Бот запущен")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text[0] == '/': #проверка на использование команды
        print('Команда обнаружена')
        if message.text == '/clear':
            mes.mes = 'You: Are elephants really afraid of mice?\nComputer: No, elephants are not afraid of mice. Elephants are actually quite tolerant of small animals and have been known to interact with them in a friendly manner.\nYou: Who don`t they like?\nComputer:'
            resp = openai.Completion.create(    # При использовании команды /clear строка mes.mes возвращается в своё изначальное состояние
                                                # И заново происходит инициальзация бота
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
        mes.mes = mes.mes + '\nYou: ' + message.text + '\nComputer:'  # В случае, если текст не является командой
                                                                      # Он передаётся OpenAI для генерации ответа
                                                                      # В случае отказа, код пробует получить ответ еще 3 раза
                                                                      # Если ответ так и не был получен, скорее всего превышен лимит токенов
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
            bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text']) # Отправляет в чат оригинал сообщения
            bot.send_message(chat_id=message.from_user.id,
                             text=GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))  # Отправляет в чат переведённое на
                                                                                                                           # русский язык сообщение
            mes.mes = mes.mes + response['choices'][0]['text']
            print(mes.mes)
        except:
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
                                 text=GoogleTranslator(source='auto', target='ru').translate(
                                     response['choices'][0]['text']))
                mes.mes = mes.mes + response['choices'][0]['text']
                print(mes.mes)
            except:
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
                                     text=GoogleTranslator(source='auto', target='ru').translate(
                                         response['choices'][0]['text']))
                    mes.mes = mes.mes + response['choices'][0]['text']
                    print(mes.mes)
                except:
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
                                         text=GoogleTranslator(source='auto', target='ru').translate(
                                             response['choices'][0]['text']))
                        mes.mes = mes.mes + response['choices'][0]['text']
                        print(mes.mes)
                    except:
                        print(mes.mes)
                        bot.send_message(chat_id=message.from_user.id, text='Ошибка')


bot.polling(none_stop=True, interval=0)
