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
        print(f'Registered user with key: {user_key}')
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
