import socket
import urllib
import logging
import random
import threading
from irc import client
import math
import time

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


    def reduce_num_msg(self, n=1):
        self.num_msg_sent -= n
        if self.num_msg_sent <0:
            self.num_msg_sent = 0

    def disconnect(self):
        self.conn.disconnect()

    def privmsg(self, channel, message):
        self.conn.privmsg(channel, message)

    def is_connected(self):
        return self.conn.is_connected()



class SenderManager:
    lock = threading.Lock()

    def __init__(self, reactor, bot, connection_number=2):
        self.bot = bot
        self.reactor = reactor
        self.connections = []
        self.connection_number = connection_number
        self.reactor.execute_every((math.ceil(self.bot.MSG_LIMIT/30*10)/10), self.reduce_num_msg, arguments=([2]))


    def reduce_num_msg(self, number):
        for i in self.connections:
            i.reduce_num_msg(number)

    def start(self):
        for i in range(self.connection_number):
            self.connections.append(self.make_new_connection())


    def make_new_connection(self):
        ip, port = self.bot.HOST, self.bot.PORT
        try:
            newconn = BotServerConnection(self.reactor)
            with self.reactor.mutex:
                self.reactor.connections.append(newconn)
            newconn.connect(ip, port, self.bot.NICK, self.bot.PASS, self.bot.NICK)
            #newconn.cap('REQ', 'twitch.tv/membership')
            #newconn.cap('REQ', 'twitch.tv/commands')
            #newconn.cap('REQ', 'twitch.tv/tags')

            connection = Connection(newconn)
            return connection
        except client.ServerConnectionError:
            return

        else:
            logging.log.error("No proper data returned when fetching IRC servers")
            return None

    def privmsg(self, message, channel=None):
        if channel == None:
            channel = self.bot.CHAN
        with self.lock:
            for i in range(len(self.connections)):
                if self.connections[i].num_msg_sent < self.bot.MSG_LIMIT:
                    if not self.connections[i].is_connected():
                        while(not self.connections[i].is_connected()):
                            self.connections[i].disconnect()
                            self.connections[i] = self.make_new_connection()
                            time.sleep(5)
                    self.connections[i].privmsg(channel, message)
                    self.connections[i].num_msg_sent += 1
                    logging.debug("Connection: %d, messages: %d" % (i, self.connections[i].num_msg_sent))
                    return

            self.connections[0].disconnect()
            self.connections[0] = self.make_new_connection()
            self.connections[0].privmsg(channel, message)
            self.connections[0].num_msg_sent += 1
