import bot
import re
import time
import cfg_old

def test(b):
        b.sock.connect((b.HOST, b.PORT))
        b.methods.send_pass()
        b.methods.send_nick()
        b.methods.join_channel()
        b.methods.send_message("hello")
        while True:
            response = ""
            response = response+b.sock.recv(1024).decode('UTF-8')

            response_split = re.split(r"[~\r\n]+", response)
            response = response_split.pop()

            for line in response_split:
                    line = str.rstrip(line)
                    line = str.split(line)

                    if len(line) >= 1:
                        if line[0] == 'PING':
                            b.methods.send_pong(line[1])

            time.sleep(1 / cfg_old.RATE)

b = bot.Bot(2)
test(b)