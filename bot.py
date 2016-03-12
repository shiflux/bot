import bot_methods
import chat
import threading
import time
from irc import client
import logging


class Bot:
    def __init__(self, user_id):
        self.user_id = user_id
        self.methods = bot_methods.bot_methods(self)
        self.methods.init()
        self.reactor = client.Reactor()
        self.chat_manager = chat.SenderManager(self.reactor, self, 2)
        self.chat_manager.start()
        self.reactor.execute_every(0.1, self.privmsg, arguments=(["gachiGASM"]))
        self.reactor.execute_every(0.1, self.privmsg, arguments=(["gachiMMM"]))
        self.reactor.execute_every(0.1, self.privmsg, arguments=(["(ditto)"]))
        self.reactor.execute_every(0.1, self.privmsg, arguments=(["forsenPls"]))
        self.reactor.execute_every(0.1, self.privmsg, arguments=(["(ditto)"]))

    def privmsg(self, message):
        self.chat_manager.privmsg(message)


    def chat_thread(self):
        while(1):
            self.reactor.process_once()
            time.sleep(0.5)

    def read(self, connection, event):
        for i in event.arguments:
            print(i)

    def init_chat(self):
        logging.debug("Hell")
        return threading.Thread(target=self.chat_thread())