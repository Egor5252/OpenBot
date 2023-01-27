import telebot
import openai
from deep_translator import GoogleTranslator
import APIs

openai.api_key = APIs.API_KEY_OPENAI

bot = telebot.TeleBot(APIs.API_KEY_TELEGRAM_BOT)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print(message.text)
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            temperature=0.5,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        print(response['choices'][0]['text'])
        # print(GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
        bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
        bot.send_message(chat_id=message.from_user.id,
                         text=GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
    except:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=message.text,
                temperature=0.5,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.0,
            )
            print(response['choices'][0]['text'])
            # print(GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
            bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
            bot.send_message(chat_id=message.from_user.id, text=GoogleTranslator(source='auto', target='ru').translate(
                response['choices'][0]['text']))
        except:
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=message.text,
                    temperature=0.5,
                    max_tokens=4000,
                    top_p=1,
                    frequency_penalty=0.5,
                    presence_penalty=0.0,
                )
                print(response['choices'][0]['text'])
                # print(GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
                bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
                bot.send_message(chat_id=message.from_user.id,
                                 text=GoogleTranslator(source='auto', target='ru').translate(
                                     response['choices'][0]['text']))
            except:
                try:
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=message.text,
                        temperature=0.5,
                        max_tokens=4000,
                        top_p=1,
                        frequency_penalty=0.5,
                        presence_penalty=0.0,
                    )
                    print(response['choices'][0]['text'])
                    # print(GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
                    bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
                    bot.send_message(chat_id=message.from_user.id,
                                     text=GoogleTranslator(source='auto', target='ru').translate(
                                         response['choices'][0]['text']))
                except ZeroDivisionError:
                    print('Ошибка')
                    bot.send_message(chat_id=message.from_user.id, text='Повторите попытку')


print("Бот запущен")
bot.polling()
