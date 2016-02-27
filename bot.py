import bot_functions


class Bot():
    def __init__(self, id):
        user_id = id
        bot_functions.dispatch(self)

