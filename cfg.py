__author__ = 'Artem'

HOST = "irc.twitch.tv"              # the Twitch IRC server
PORT = 6667                         # always use port 6667!
NICK = "weeeebot"            # your Twitch username, lowercase
PASS = "oauth:c35jmcnxnnwbhcuba80kfsvd2dx98p" # your Twitch OAuth token
CHAN = "#shiflux"                   # the channel you want to join
STREAMER = "shiflux"
RATE = (20/30) # messages per second


PATT = [
    r"swear",
    # ...
    r"some_pattern"
]

#POINTS BOT
SLEEP_TIME = 120