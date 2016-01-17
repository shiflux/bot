__author__ = 'Artem'
import bot
import cfg
import utils

def command_test(sock, message, username):
    bot.send_message(sock, "the test command is working")

def command_hi(sock, message, username):
    bot.send_message(sock, "hello is working")

def command_mmm(sock, message, username):
    bot.send_message(sock, "gachiMMM MMM gachiMMM MMM gachiMMM MMM gachiMMM MMM gachiMMM")

def command_gachi(sock, message, username):
    bot.send_message(sock, "gachiGASM "+username+" gachiGASM IS gachiGASM FUCKING gachiGASM CUMMING gachiGASM")

def command_follow(sock, message, username):
    if message == None or message == "":
        user = username
        channel = cfg.STREAMER
    else:
        msg = message.split(" ")
        if len(msg)<2 or msg[1]=="":
            user = msg[0]
            channel = cfg.STREAMER
        else:
            user = msg[0]
            channel = msg[1]
    time = utils.follow(user, channel)
    if time == False:
        bot.send_message(sock, user+" doesn't follow " + channel)
    else:
        bot.send_message(sock, user+" follows " + channel + " since "+time)

def command_points(sock, message, username):
    print("hi")
    bot.send_whisper(sock, "hidd", username)


options = {'!test': command_test,
           'hi': command_hi,
           '!mmm': command_mmm,
           '!gachi': command_gachi,
           "!follow": command_follow,
           "!points": command_points}