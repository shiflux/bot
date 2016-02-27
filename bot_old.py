__author__ = 'Artem'
import cfg_old
import re
import commands


def send_message(sock, msg):
    sock.send(bytes('PRIVMSG %s :%s\r\n' % (cfg_old.CHAN, msg), 'UTF-8'))

def send_whisper(sock, msg, user):
    sock.send(bytes('PRIVMSG %s :/w %s %s\r\n' % (cfg_old.CHAN, user, msg), 'UTF-8'))

def send_pong(sock, msg):
    sock.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

def ban(sock, user):
    send_message(sock, ".ban "+ user)

def timeout(sock, user, secs=600):
    send_message(sock, ".timeout "+ user + str(secs))

def send_nick(sock, nick):
    sock.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))

def send_pass(sock, password):
    sock.send(bytes('PASS %s\r\n' % password, 'UTF-8'))

def join_channel(sock, chan):
    sock.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))

def part_channel(sock, chan):
    sock.send(bytes('PART %s\r\n' % chan, 'UTF-8'))

def parse_message(message):
    CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    username = re.search(r"\w+", message).group(0) # return the entire match
    parsed_message = CHAT_MSG.sub("", message)
    return username, parsed_message

def check_commands(sock, message, username):
    msg = message.split(" ", 1)
    if len(msg) < 1:
        return
    elif len(msg) <2:
        msg.append(None)
    if msg[0] in commands.options:
        commands.options[msg[0]](sock, msg[1], username)

def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result
