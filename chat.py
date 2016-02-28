import irc
import socket

class BotServerConnection(irc.client.ServerConnection):
    def send_raw(self, string):
        """Send raw string to the server.
        The string will be padded with appropriate CR LF.
        """
        # The string should not contain any carriage return other than the
        # one added here.
        if '\n' in string:
            raise irc.clientInvalidCharacters(
                "Carriage returns not allowed in privmsg(text)")
        bytes = string.encode('utf-8') + b'\r\n'
        # According to the RFC http://tools.ietf.org/html/rfc2812#page-6,
        # clients should not transmit more than 512 bytes.
        # However, Twitch have raised that limit to 2048 in their servers.
        if len(bytes) > 2048:
            raise irc.clientMessageTooLong(
                "Messages limited to 2048 bytes including CR/LF")
        if self.socket is None:
            raise irc.clientServerNotConnectedError("Not connected.")
        sender = getattr(self.socket, 'write', self.socket.send)
        try:
            sender(bytes)
        except socket.error:
            self.disconnect("Connection reset by peer.")

class ChatManager:
    def __init__(self, bot):
        self.bot = bot

