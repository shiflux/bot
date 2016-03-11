from twisted.words.protocols import irc
import logging
import time
from twisted.internet import protocol, reactor
from twisted.internet.endpoints import clientFromString


class ServerConnection(irc.IRCClient):

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        logging.debug("[connected at %s]" % time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        logging.debug("[disconnected at %s]" % time.asctime(time.localtime(time.time())))


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        logging.debug("[I have joined %s]" % channel)


    def privmsg(self, user, channel, msg):
        """
        Whenever someone says "why" give a lazy programmer response
        """
        logging.debug("USER: %s, CHANNEL: %s, MESSAGE: %s" % user, channel, msg)


class MyBotFactory(protocol.ClientFactory):

    def __init__(self, nickname, channel, channel_key=None):
        self.protocol = ServerConnection
        self.nickname = nickname
        self.channel = channel
        self.channel_key = channel_key

    # def clientConnectionLost(self, reason):
    #     logging.debug("Lost connection (%s), reconnecting." % reason)


class ChatManager:
    def __init__(self, bot):
        self.bot = bot
        self.client = None
        self.main_connection = None

    def start(self):
        self.make_new_connection()
        reactor.run()

    def make_new_connection(self):
        try:
            self.main_connection = MyBotFactory(nickname=self.bot.NICK, channel=self.bot.CHAN,
                                                channel_key=self.bot.PASS)
            reactor.connectTCP(self.bot.HOST, self.bot.PORT, self.main_connection)
        except Exception as e:
            logging.log.error("Could not connect:", e)

    def privmsg(self, message):
        self.main_connection.msg(self.main_connection.factory.channel, message)
