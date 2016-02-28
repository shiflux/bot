import bot_methods



class Bot:
    def __init__(self, user_id):
        self.user_id = user_id
        self.methods = bot_methods.bot_methods(self)
        self.methods.init()

