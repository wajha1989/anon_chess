from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

import json

from .models import GameRequest, Game


def request_game(request):
    if request.session.get('userId'):
        return HttpResponseForbidden('You have already requested a game')

    if request.method == 'POST':
        other_player = other_user()
        new_key = GameRequest.objects.create()
        request.session['userId'] = new_key.pk
        if other_player:
            game = Game.objects.create(
                player_white=other_player,
                player_black=new_key,
                game_moves=""
            )
            return JsonResponse({
                'userId': new_key.pk,
                'key': str(new_key.secret),
                'gameId': game.pk,
                'side': 'black'
            })
        else:
            return JsonResponse({
                'userId': new_key.pk,
                'key': str(new_key.secret),
                'gameId': None,
                'side': None
            })
    else:
        return Http404("Accepts only POST requests")


def get_personal_game(request):
    if request.session.get('userId'):
        return get_game_data(request, request.session.get('userId'))
    else:
        return Http404("Not registered yet")


def get_game_data(request, user_id):
    if request.method == 'GET':
        game, side = find_corresponding_game(user_id)
        return JsonResponse({
            'gameId': game.pk if game else None,
            'side': side if side else None
        })
    else:
        return Http404("Accepts only GET requests")


def clear_session(request):
    try:
        associated_request = GameRequest.objects.get(pk=request.session.get('userId'))
        associated_request.delete()
    except GameRequest.DoesNotExist:
        pass
    request.session.clear()
    return JsonResponse({'status': 'Session cleared'})


# auxiliary function
def other_user():
    game_requests_not_in_game = GameRequest.objects.exclude(
        Q(player_white__isnull=False) | Q(player_black__isnull=False)
    )
    return game_requests_not_in_game[0] if game_requests_not_in_game else None


def find_corresponding_game(user_id):
    try:
        game = Game.objects.get(player_white_id=user_id)
        return game, 'white'
    except Game.DoesNotExist:
        pass

    try:
        game = Game.objects.get(player_black_id=user_id)
        return game, 'black'
    except Game.DoesNotExist:
        pass

    return None, None
