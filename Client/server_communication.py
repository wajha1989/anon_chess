import json


def get_game_data(session):
    url = f'http://127.0.0.1:8000/chess/gamerequests/personal'
    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Got data about user back")
        if data['gameId']:
            print("Found a game")
        else:
            print("still no game")
        return data
    else:
        print("Something went wrong")
        return None


def register(session):
    url = 'http://127.0.0.1:8000/chess/gamerequests'
    response = session.post(url)

    if response.status_code == 200:
        data = response.json()
        user_key = data['key']
        print(f'Registered user with key: {user_key} and id {data['gameId']}')
        return data
    else:
        print(f'Failed to register user. Status code: {response.status_code}')
        return None


def clear_session(session):
    url = 'http://127.0.0.1:8000/chess/clearsession'
    response = session.post(url)

    if response.status_code == 200:
        data = response.json()
        status = data['status']
        print(f'Status: {status}')
    else:
        print("Session not flushed. This is not supposed to happen")


def get_game_update(session):
    url = 'http://127.0.0.1:8000/chess/games/personal'
    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("game update - something went wrong.")


def server_move(session, move, time_left):
    url = 'http://127.0.0.1:8000/chess/games/personal/move'

    data = {'move': move,
            'time_left': time_left}

    json_data = json.dumps(data)

    response = session.post(url, json_data)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('move - something went wrong.')


def cancel(session):
    url = 'http://127.0.0.1:8000/chess/gamerequests/personal/cancel'

    response = session.post(url)
