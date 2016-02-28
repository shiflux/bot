import bot_methods
import chat
from irc import client



class Bot:
    def __init__(self, user_id):
        self.user_id = user_id
        self.methods = bot_methods.bot_methods(self)
        self.methods.init()
        self.reactor = client.Reactor()
        self.chat_manager = chat.ChatManager(self.reactor, self)
        self.chat_manager.start()

    def privmsg(self, message):
        self.chat_manager.privmsg(message)

