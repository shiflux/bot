import cfg_old
import socket

class bot_methods:
    def __init__(self, bot):
        self.bot = bot

    def init(self):
        self.bot.sock = socket.socket()
        self.bot.HOST = cfg_old.HOST
        self.bot.PORT = cfg_old.PORT
        self.bot.PASS = cfg_old.PASS
        self.bot.NICK = cfg_old.NICK
        self.bot.CHAN = cfg_old.CHAN
        self.bot.MSG_LIMIT = cfg_old.MSG_LIMIT

    def send_message(self, msg):
        self.bot.sock.send(bytes('PRIVMSG %s :%s\r\n' % (self.bot.CHAN, msg), 'UTF-8'))

    def send_whisper(self, msg, user):
        self.bot.sock.send(bytes('PRIVMSG %s :/w %s %s\r\n' % (self.bot.CHAN, user, msg), 'UTF-8'))

    def send_pong(self, msg):
        self.bot.sock.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

    def ban(self, user):
        self.send_message(".ban "+ user)

    def timeout(self, user, secs=600):
        self.send_message(".timeout "+ user + str(secs))

    def send_nick(self):
        self.bot.sock.send(bytes('NICK %s\r\n' % self.bot.NICK, 'UTF-8'))

    def send_pass(self):
        self.bot.sock.send(bytes('PASS %s\r\n' % self.bot.PASS, 'UTF-8'))

    def join_channel(self):
        self.bot.sock.send(bytes('JOIN %s\r\n' % self.bot.CHAN, 'UTF-8'))

    def part_channel(self):
        self.bot.sock.send(bytes('PART %s\r\n' % self.bot.CHAN, 'UTF-8'))