import bot_methods
import chat
import threading
import time
import logging
import sys



class Bot:
    def __init__(self, user_id):
        self.user_id = user_id #id of the user connected to the bot
        self.methods = bot_methods.bot_methods(self)
        self.methods.init()
        self.chat_manager = chat.ChatManager(self)
        self.handlers_list = []



    def privmsg(self, message):
        self.chat_manager.privmsg(message)

    def test(self):
        self.privmsg("test")

    def init_chat(self):
        return threading.Thread(target=self.chat_thread)

    def add_handler(self, handler):
        self.handlers_list.append(handler)


    def start(self):
        logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)
        self.chat_manager.start()