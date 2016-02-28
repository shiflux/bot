import socket
import urllib
import logging
import random
from irc import client

class BotServerConnection(client.ServerConnection):
    def send_raw(self, string):
        """Send raw string to the server.
        The string will be padded with appropriate CR LF.
        """
        # The string should not contain any carriage return other than the
        # one added here.
        if '\n' in string:
            raise client.InvalidCharacters(
                "Carriage returns not allowed in privmsg(text)")
        bytes = string.encode('utf-8') + b'\r\n'
        # According to the RFC http://tools.ietf.org/html/rfc2812#page-6,
        # clients should not transmit more than 512 bytes.
        # However, Twitch have raised that limit to 2048 in their servers.
        if len(bytes) > 2048:
            raise client.MessageTooLong(
                "Messages limited to 2048 bytes including CR/LF")
        if self.socket is None:
            raise client.ServerNotConnectedError("Not connected.")
        sender = getattr(self.socket, 'write', self.socket.send)
        try:
            sender(bytes)
        except socket.error:
            self.disconnect("Connection reset by peer.")

class Connection:
    def __init__(self, conn):
        self.conn = conn
        self.num_msg_sent = 0

    def reduce_num_msg_sent(self, n=1):
        self.num_msg_sent -= n


class ChatManager:
    def __init__(self, reactor, bot):
        self.bot = bot
        self.reactor = reactor
        self.main_connection = None
        self.send_connection = None
        self.backup_connection = None

    def start(self):
        self.main_connection = self.make_new_connection()
        self.send_connection = self.make_new_connection()
        self.backup_connection = self.make_new_connection()
        self.send_connection


    def make_new_connection(self):
        ip, port = self.bot.HOST, self.bot.PORT
        try:
            newconn = BotServerConnection(self)
            newconn.connect(ip, port, self.bot.nickname, self.bot.password, self.bot.nickname)
            newconn.cap('REQ', 'twitch.tv/membership')
            newconn.cap('REQ', 'twitch.tv/commands')
            newconn.cap('REQ', 'twitch.tv/tags')

            connection = Connection(newconn)
            return connection
        except client.ServerConnectionError:
            return

        else:
            logging.log.error("No proper data returned when fetching IRC servers")
            return None

    def privmsg(self, message, channel = self.bot.CHAN)
        self.send_connection.conn.privmsg(channel, message)
