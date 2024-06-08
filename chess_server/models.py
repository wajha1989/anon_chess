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
