import telebot
import openai
from deep_translator import GoogleTranslator
import APIs
import mes

openai.api_key = APIs.API_KEY_OPENAI

bot = telebot.TeleBot(APIs.API_KEY_TELEGRAM_BOT)



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    #print(message.text)
    mes.mes = mes.mes + ' You: ' + message.text + '\nComputer:'
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=mes.mes,
            temperature=0.5,
            max_tokens=4000,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["You:"]
        )
        #print(response['choices'][0]['text'])
        # print(GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
        bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
        bot.send_message(chat_id=message.from_user.id,
                         text=GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
        mes.mes = mes.mes + response['choices'][0]['text']
        print(mes.mes)
    except:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=mes.mes,
                temperature=0.5,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.0,
                stop=["You:"]
            )
            # print(response['choices'][0]['text'])
            # print(GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
            bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
            bot.send_message(chat_id=message.from_user.id,
                             text=GoogleTranslator(source='auto', target='ru').translate(
                                 response['choices'][0]['text']))
            mes.mes = mes.mes + response['choices'][0]['text'] + '\n'
            print(mes.mes)
        except:
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=mes.mes,
                    temperature=0.5,
                    max_tokens=4000,
                    top_p=1,
                    frequency_penalty=0.5,
                    presence_penalty=0.0,
                    stop=["You:"]
                )
                # print(response['choices'][0]['text'])
                # print(GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
                bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
                bot.send_message(chat_id=message.from_user.id,
                                 text=GoogleTranslator(source='auto', target='ru').translate(
                                     response['choices'][0]['text']))
                mes.mes = mes.mes + response['choices'][0]['text'] + '\n'
                print(mes.mes)
            except:
                try:
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=mes.mes,
                        temperature=0.5,
                        max_tokens=4000,
                        top_p=1,
                        frequency_penalty=0.5,
                        presence_penalty=0.0,
                        stop=["You:"]
                    )
                    # print(response['choices'][0]['text'])
                    # print(GoogleTranslator(source='auto', target='ru').translate(response['choices'][0]['text']))
                    bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
                    bot.send_message(chat_id=message.from_user.id,
                                     text=GoogleTranslator(source='auto', target='ru').translate(
                                         response['choices'][0]['text']))
                    mes.mes = mes.mes + response['choices'][0]['text'] + '\n'
                    print(mes.mes)
                except:
                    print(mes.mes)
                    bot.send_message(chat_id=message.from_user.id, text='Повторите попытку')


print("Бот запущен")
bot.polling()
