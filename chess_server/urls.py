from django.urls import path
from . import views

urlpatterns = [
    path('gamerequests', views.request_game, name='request_game'),
    path('clearsession', views.clear_session, name='flush_session'),
    path('gamerequests/<int:user_id>', views.get_game_data, name='get_game_data'),
    path('gamerequests/personal', views.get_personal_game, name='get_personal'),
    path('games/<int:game_id>/move', views.make_move, name='make_move'),
    path('games/personal/move', views.make_personal_move, name='make_personal_move'),
    path('games/<int:game_id>', views.get_game_update, name='get_game_data'),
    path('games/personal', views.get_personal_game_update, name='get_personal_game_data'),
    path('games/personal/cancel', views.cancel, name='cancel')
]
