import bot_methods
import chat
import threading
import time
from irc import client



class Bot:
    def __init__(self, user_id):
        self.user_id = user_id
        self.methods = bot_methods.bot_methods(self)
        self.methods.init()
        self.reactor = client.Reactor()
        self.chat_manager = chat.ChatManager(self.reactor, self)
        self.chat_manager = chat.ChatManager(self.reactor, self)
        self.chat_manager.start()
        self.reactor.execute_every(5, self.test)

    def privmsg(self, message):
        self.chat_manager.privmsg(message)

    def test(self):
        self.privmsg("test")

    def chat_thread(self):
        while(1):
            self.reactor.process_once()
            time.sleep(0.1)

    def init_chat(self):
        return threading.Thread(target=self.chat_thread())