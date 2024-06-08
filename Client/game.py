from server_communication import register, get_game_data
import time
import requests


class Game:
    session = requests.Session()
    secret = None
    user_id = None
    game_id = None
    side = None

    def begin(self):
        game_data = register(self.session)
        self.secret = game_data['key']
        self.user_id = game_data['userId']
        if game_data['gameId'] is None:
            game_data = self.wait_for_game()
        self.game_id = game_data['gameId']
        self.side = game_data['side']
        print(self)

    def wait_for_game(self):
        while True:
            game_data = get_game_data(self.session)
            if game_data['gameId'] is not None:
                return game_data
            time.sleep(1)

    def __str__(self):
        return ("userId: " + str(self.user_id) + "\n" +
                "secret: " + str(self.secret) + "\n" +
                "gameId: " + str(self.game_id) + "\n" +
                "side: " + self.side + "\n")
