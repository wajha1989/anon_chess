from django.db import models


class GameRequest(models.Model):
    secret = models.CharField(max_length=64)


class Game(models.Model):
    player_white = models.OneToOneField(
        GameRequest,
        on_delete=models.CASCADE,
        related_name='white_player'
    )
    player_black = models.OneToOneField(
        GameRequest,
        on_delete=models.CASCADE,
        related_name="black_player"
    )
    game_moves = models.CharField(max_length=1000)
