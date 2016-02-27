__author__ = 'Artem'
import json
import urllib.request as urllib2


def follow(user, channel):
    try:
        r = urllib2.urlopen("https://api.twitch.tv/kraken/users/"+user+"/follows/channels/"+channel).read().decode('utf8')
    except:
        pass
    if 'r' in locals():
        followJson = json.loads(r)
        if "error" in followJson:
            return False
        else:
            time = followJson["created_at"]
            return time[0:9]
    else:
        return False


def viewer_count(channel):
    try:
        r = urllib2.urlopen("http://tmi.twitch.tv/group/user/"+channel+"/chatters").read().decode('utf8')
        chattersJson = json.loads(r)
        return chattersJson["chatter_count"]
    except:
        pass
    return -1

def viewer_list(channel):
    try:
        print("http://tmi.twitch.tv/group/user/"+channel+"/chatters")
        r = urllib2.urlopen("http://tmi.twitch.tv/group/user/"+channel+"/chatters").read().decode('utf8')
        chattersJson = json.loads(r)
        return chattersJson["chatters"]["moderators"]+chattersJson["chatters"]["staff"]+chattersJson["chatters"]["admins"]+chattersJson["chatters"]["global_mods"]+chattersJson["chatters"]["viewers"]
    except:
        pass
    return []