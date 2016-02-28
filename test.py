import bot
import re
import time
import cfg_old
import threading

# def test(b):
#         b.sock.connect((b.HOST, b.PORT))
#         b.methods.send_pass()
#         b.methods.send_nick()
#         b.methods.join_channel()
#         #b.methods.send_message("MingLee")
#         counter = 0
#         while True:
#             # response = ""
#             # response = response+b.sock.recv(1024).decode('UTF-8')
#             # response_split = re.split(r"[~\r\n]+", response)
#             # response = response_split.pop()
#             #
#             # for line in response_split:
#             #         line = str.rstrip(line)
#             #         line = str.split(line)
#             #
#             #         if len(line) >= 1:
#             #             if line[0] == 'PING':
#             #                 b.methods.send_pong(line[1])
#             if(counter<50):
#                 b.methods.send_message("RuleFive "+str(counter))
#                 counter+=1
#             else:
#                 b.methods.part_channel()
#                 break
#
#             time.sleep(0.1)
#
# #b = bot.Bot(2)
# #test(b)
# threads = []
# k = 3
# try:
#     for i in range(k):
#         b = bot.Bot(i)
#         t = threading.Thread(target=test, args=(b,))
#         threads.append(t)
#         t.start()
# except:
#     print("error")
#
# for th in threads:
#     th.join()

def test():
    b = bot.Bot(1)
    print("ci")
    b.privmsg("Hello")
    t = b.init_chat()
    t.start()
    t.join()



test()