from django.urls import path
from . import views

urlpatterns = [
    path('gamerequests', views.request_game, name='request_game'),
    path('clearsession', views.clear_session, name='flush_session'),
    path('gamerequests/<int:user_id>', views.get_game_data, name='get_game_data'),
    path('gamerequests/personal', views.get_personal_game, name='get_personal'),
]
