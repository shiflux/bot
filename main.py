__author__ = 'Artem'

import cfg
import socket
import re
import bot
import time

sock = socket.socket()
sock.connect((cfg.HOST, cfg.PORT))
bot.send_pass(sock, cfg.PASS)
bot.send_nick(sock, cfg.NICK)
bot.join_channel(sock, cfg.CHAN)

bot.send_message(sock, "hello")


#MAIN LOOP

while True:
    response = ""
    response = response+sock.recv(1024).decode('UTF-8')

    response_split = re.split(r"[~\r\n]+", response)
    response = response_split.pop()

    for line in response_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    bot.send_pong(sock, line[1])

                if line[1] == 'PRIVMSG':
                    username = bot.get_sender(line[0])
                    message = bot.get_message(line)
                    bot.check_commands(sock, message, username)

                    print(username + ": " + message)


    time.sleep(1 / cfg.RATE)



#    if response == "PING :tmi.twitch.tv\r\n":
#        sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
#    else:
#        username, msg = bot.parse_message(response)
#        bot.check_commands(sock, msg, username)
#        print(response)
#
# timeout instructions
#        for pattern in cfg.PATT:
#            if re.match(pattern, message):
#                bot.timeout(s, username, 5)
#                break
