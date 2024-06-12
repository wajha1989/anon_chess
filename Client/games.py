from server_communication import register, get_game_data, get_game_update, server_move, cancel, clear_session
import time
import requests
import chess

tick_timeout = 0.01


class Game:
    session = requests.Session()
    secret = None
    user_id = None
    game_id = None
    side = None
    chessboard = None
    white_move = True
    last_move = ''

    def begin(self):
        self.clear_session()
        self.chessboard = chess.Board()
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
            time.sleep(tick_timeout)

    def get_legal_moves(self, row, column):
        start_square = chess.square(column, row)
        legal_moves = [move for move in self.chessboard.legal_moves if move.from_square == start_square]

        legal_square = []
        for move in legal_moves:
            end_col = chess.square_file(move.to_square)
            end_row = chess.square_rank(move.to_square)
            legal_square.append((end_row, end_col))

        return legal_square

    def debug_square(self, row, col):
        print(f'clicked field row: {row} column: {col}')
        square = chess.square(col, row)
        print(f'chess square name {chess.square_name(square)}')
        print(f'piece at square {self.chessboard.piece_at(square)}')
        print(f'Legal square where this move could end - {self.get_legal_moves(row, col)}')
        print('\n')

    def update(self):
        game_data = get_game_update(self.session)
        print(f'game_data: {game_data}')
        if game_data:
            if self.white_move is not game_data['whiteMove']:
                self.white_move = game_data['whiteMove']
            if self.last_move != game_data['lastMove']:
                self.last_move = game_data['lastMove']
                return True
        return False

    def make_move(self, start_square, end_square, time_left=0):
        start_square = chess.square(start_square[1], start_square[0])
        end_square = chess.square(end_square[1], end_square[0])
        move = chess.Move(start_square, end_square)
        server_move(self.session, move.uci(), time_left)
        print(f'making move {move.uci()}')
        self.chessboard.push(move)
        print(self.chessboard)
        self.white_move = not self.white_move
        self.last_move = move.uci()
        return move

    def clear_session(self):
        clear_session(self.session)

    def cancel(self):
        cancel(self.session)

    def __str__(self):
        return ("userId: " + str(self.user_id) + "\n" +
                "secret: " + str(self.secret) + "\n" +
                "gameId: " + str(self.game_id) + "\n" +
                "side: " + self.side + "\n")
