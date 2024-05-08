from dotenv import load_dotenv
import os
import requests 
import json

load_dotenv()

class TelegramBot:
    def __init__(self):
        TOKEN = os.getenv("API_KEY")
        self.url = f"https://api.telegram.org/bot{TOKEN}/"

    def start_bot(self):
        update_id = None
        while True:
            update = self.get_message(update_id)
            messages = update['result']
            if messages:
                for message in messages:
                    try:
                        update_id = message['update_id']
                        chat_id = message['message']['from']['id']
                        message_text = message['message']['text']
                        answer_bot = self.create_answer(message_text)
                        self.send_answer(chat_id,answer_bot)
                    except:
                        pass            


    def get_message(self, update_id):
        TIMEOUT = os.getenv("TIME_OUT_REQUEST")
        link_request = f"{self.url}getUpdates?timeout={TIMEOUT}"
        if update_id:
            link_request = f"{self.url}getUpdates?timeout={TIMEOUT}&offset={update_id + 1}"   
        result = requests.get(link_request)
        return json.loads(result.content)  
    
    def create_answer(self, messsage_text):
        return "Olá, tudo bem?"

    def send_answer(self, chat_id, answer):
        link_to_send = f"{self.url}sendMessage?chat_id={chat_id}&text={answer}"
        requests.get(link_to_send)
        return
    