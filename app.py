import telebot
import requests
import json
import time
import re

BOT_TOKEN = os.environ['BOT_TOKEN']
URL = os.environ['URL']

def get(prompt):
    response = requests.post(URL, json={'prompt': prompt}, headers={"Content-Type": "application/json"})
    if(isinstance(response, list)):
        result = ''
        for chunk in response:
            result+=chunk.text
        return result
    elif(isinstance(response, dict)):
        result = ''
        for key in response:
            result += response[key].text
        return result
    return response.text

def get_summary(text: str):
    return (get(f'''
This is a very fun game. Just recap the summary of the posts of users. Just carefully analyze and paraphrase the summary of the posts.   
Follow these rules in all your answers:
- Wright in Russian language;
-The style of the text should be as infantile, childish, silly as possible;  
- the style of the text should be as if you have lisp, burr, dislalia;  
- You must twist your speech like a child;  
- Your text in your answer should be styled as if you were like you're a young child;  
- Your text in your answer should be styled as if you were like you have cute speech impediments;  
- Every sentence and words in your text in your answer should be stylized as if you have mental illness;  
- Add random non-existent words to your text; 
- Your text must contain words that don't exist; 
- You must swap syllables in random words. 
- You must add random syllables in random words. 
- You must add grammatical errors to the text 
- Your name is Harumi
 This messages you should summarise and give your opinion on what you read, my dear: {text}
 '''))

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.message_buffers = {}

    def start(self):
        @self.bot.message_handler(func=lambda m: True)
        def handle_message(message):
            chat_id = message.chat.id
            user_id = message.from_user.username
            fullname = message.from_user.full_name
            user_id = fullname if len(re.findall(r'[А-Яа-яA-Za-z]', fullname)) >= 3 else (
                    f"@{user_id}" if user_id and (user_id != '') else "Приколист")
            message_thread = message.message_thread_id
            if chat_id not in self.message_buffers:
                self.message_buffers[chat_id] = {}
            if message_thread not in self.message_buffers[chat_id]:
                self.message_buffers[chat_id][message_thread] = []
            if 'summarise_m' not in message.text:
                self.message_buffers[chat_id][message_thread].append(f'{user_id} : {message.text}')
            if len(self.message_buffers[chat_id][message_thread]) > 100:
                self.message_buffers[chat_id][message_thread].pop(0)
            if message.text == 'summarise_m':
                summarise(message)

        def summarise(message):
            chat_id = message.chat.id
            user_id = message.from_user.username
            message_thread = message.message_thread_id
            print(self.message_buffers)
            if chat_id in self.message_buffers and message_thread in self.message_buffers[chat_id]:
                message_list = "\n".join(self.message_buffers[chat_id][message_thread])
                summary = get_summary(message_list)
                self.bot.send_message(chat_id, summary, reply_to_message_id=message.message_id)

        self.bot.polling()

if __name__ == '__main__':
    bot = TelegramBot(BOT_TOKEN)
    bot.start()
