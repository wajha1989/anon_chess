from django.db import models
import uuid


class GameRequest(models.Model):
    secret = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Game(models.Model):
    player_white = models.OneToOneField(
        GameRequest,
        on_delete=models.CASCADE,
        related_name='player_white',
    )
    player_black = models.OneToOneField(
        GameRequest,
        on_delete=models.CASCADE,
        related_name="player_black",
    )
    game_moves = models.CharField(max_length=1000)
    white_move = models.BooleanField(default=True)

    def get_last_move(self):
        if self.game_moves != '':
            return self.game_moves[-4:]
        else:
            return ''

    def __str__(self):
        return "moves: " + self.game_moves + '\n' + (' white move' if self.white_move else ' black move')
