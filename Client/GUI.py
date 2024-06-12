import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
import chess
import time
from games import Game
import math

colors = ["#DDB88C", "#A66D4F"]

tick_timeout = 0.01


class BlackWin(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.make_button()

    def make_button(self):
        button = tk.Button(self, text="Black Wins", font=('Helvetica', 48), compound='top', width=600, height=400,
                           command=self.go_back)
        button.pack()

    def go_back(self):
        self.master.switch_frame(MainMenu)


class WhiteWin(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.make_button()

    def make_button(self):
        button = tk.Button(self, text="White Wins", font=('Helvetica', 48), compound='top', width=600, height=400,
                           command=self.go_back)
        button.pack()

    def go_back(self):
        self.master.switch_frame(MainMenu)


class Draw(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.make_button()

    def make_button(self):
        button = tk.Button(self, text="Draw", font=('Helvetica', 48), compound='top', width=600, height=400,
                           command=self.go_back)
        button.pack()

    def go_back(self):
        self.master.switch_frame(MainMenu)


class ChessBoard(tk.Frame):
    def __init__(self, master, board_size=8, square_size=60):
        super().__init__(master)
        self.board_size = board_size
        self.square_size = square_size
        self.piece_images = self.load_piece_images()
        self.buttons = {}
        self.piece_locations = {}

        self.white_time_left = 600.0
        self.black_time_left = 600.0
        self.white_timer = tk.Label(self, text="00:00:00", font=("Helvetica", 48))
        self.black_timer = tk.Label(self, text="00:00:00", font=("Helvetica", 48))

        self.create_board_and_labels()
        self.current_clicked = None
        self.chessboard = master.game.chessboard
        self.interrupted = False
        self.update_thread = Thread(target=self.update_data_loop, daemon=True)
        self.update_thread.start()
        self.enemy_move = None
        self.check_for_enemy_moves()
        self.update()

    def update_timers(self):
        if self.master.game.white_move:
            self.white_time_left -= 1 * tick_timeout
            time = int(math.ceil(self.white_time_left))
            hours, remainder = divmod(time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.white_timer.config(text=time_str)
        else:
            self.black_time_left -= 1 * tick_timeout
            time = int(math.ceil(self.black_time_left))
            hours, remainder = divmod(time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.black_timer.config(text=time_str)

    def check_if_game_end(self):
        result = self.master.game.chessboard.result()
        print(f'Result: {result}')
        if result == "*":
            if self.white_time_left <= 0:
                self.interrupted = True
                self.update_thread.join()
                self.after(2000, self.master.switch_frame, BlackWin)
            if self.black_time_left <= 0:
                self.interrupted = True
                self.update_thread.join()
                self.after(2000, self.master.switch_frame, WhiteWin)
            else:
                pass
        else:
            if result == "1/2-1/2":
                self.interrupted = True
                self.after(2000, self.master.switch_frame, Draw)
            elif result == "1-0":
                self.interrupted = True
                self.after(2000, self.master.switch_frame, WhiteWin)
            else:
                self.interrupted = True
                self.after(2000, self.master.switch_frame, BlackWin)

    def update_data_loop(self):
        while not self.interrupted:
            print(f'last known move {self.master.game.last_move}')
            print(f'is it whites_turn? {self.master.game.white_move}')
            if self.master.game.update():
                print('the opponent apparently made a move, adding the move for completion')
                if self.master.game.last_move != '':
                    move = chess.Move.from_uci(self.master.game.last_move)
                    start_square = chess.square_rank(move.from_square), chess.square_file(move.from_square)
                    end_square = chess.square_rank(move.to_square), chess.square_file(move.to_square)
                    self.enemy_move = (start_square, end_square)
            time.sleep(tick_timeout)

    def check_for_enemy_moves(self):
        print(f'enemy move - {self.enemy_move}')
        if self.enemy_move is not None:
            print('opponent apparently made a move, making the move')
            self.make_move(self.enemy_move[0], self.enemy_move[1])
            self.enemy_move = None
        self.update_timers()
        self.check_if_game_end()
        if not self.interrupted:
            self.after(int(tick_timeout * 1000), self.check_for_enemy_moves)

    def create_board_and_labels(self):
        # self.white_timer.grid(row=0, columnspan=self.board_size)
        self.white_timer.pack()

        board_frame = tk.Frame(self, height=200, width=200)
        # board_frame.grid(row=1, column=0)
        board_frame.pack()

        self.create_board(board_frame)

        # self.black_timer.grid(row=2, columnspan=self.board_size)
        self.black_timer.pack()

    def create_board(self, parent):
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = colors[(row + col) % 2]
                btn = tk.Button(parent, bg=color, activebackground=color,
                                width=self.square_size // 4, height=self.square_size // 8,
                                command=lambda r=row, c=col: self.on_square_click(r, c))
                btn.grid(row=row, column=col, padx=0, pady=0)
                self.buttons[(row, col)] = btn

        for i in range(self.board_size):
            self.grid_columnconfigure(i, weight=1, uniform="column")
            self.grid_rowconfigure(i, weight=1, uniform="row")
        self.place_pieces()

    def load_piece_images(self):
        piece_images = {}
        pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
        colors = ["white", "black"]
        for color in colors:
            for piece in pieces:
                image_path = f"images/{color}_{piece}.png"
                image = Image.open(image_path)
                image = image.resize((self.square_size - 1, self.square_size - 1))
                piece_images[f"{color}_{piece}"] = ImageTk.PhotoImage(image)
        return piece_images

    def place_pieces(self):
        piece_positions = {
            "black_pawn": [(i, 6) for i in range(8)],
            "white_pawn": [(i, 1) for i in range(8)],
            "black_rook": [(0, 7), (7, 7)],
            "white_rook": [(0, 0), (7, 0)],
            "black_knight": [(1, 7), (6, 7)],
            "white_knight": [(1, 0), (6, 0)],
            "black_bishop": [(2, 7), (5, 7)],
            "white_bishop": [(2, 0), (5, 0)],
            "black_queen": [(3, 7)],
            "white_queen": [(3, 0)],
            "black_king": [(4, 7)],
            "white_king": [(4, 0)],
        }
        for piece, positions in piece_positions.items():
            for (col, row) in positions:
                btn = self.buttons[(row, col)]
                btn.config(image=self.piece_images[piece], width=110, height=110)
                self.piece_locations[(row, col)] = piece

    def on_square_click(self, row, col):
        print(f'clicked row: {row}, column: {col}')
        print(f'currently selected: {self.current_clicked}')
        if self.can_play():
            self.master.game.debug_square(row, col)
            if self.current_clicked is None:
                self.current_clicked = row, col
                legal_squares = self.master.game.get_legal_moves(row, col)
                if not legal_squares == []:
                    for button in self.buttons:
                        row, col = button
                        if (row, col) in legal_squares:
                            print(f'painting {button}')
                            self.buttons[button].config(bg="green", activebackground="green")
                else:
                    self.current_clicked = None
            else:
                selected_row, selected_col = self.current_clicked
                legal_squares = self.master.game.get_legal_moves(selected_row, selected_col)
                if (row, col) in legal_squares:
                    self.make_move(self.current_clicked, (row, col))
                else:
                    self.current_clicked = None
                    self.de_color()

    def make_move(self, start_square, end_square):
        print(f'moving square {start_square} to {end_square}')
        moving_piece = self.piece_locations.get(start_square, None)
        move = self.get_move(start_square, end_square)
        self.buttons[start_square].config(image='', width=self.square_size // 4, height=self.square_size // 8)
        self.buttons[end_square].config(image=self.piece_images[moving_piece], width=110, height=110)
        if self.chessboard.is_castling(move):
            if 'g' in move.uci():
                rook_start_square = start_square[0], 7
                rook_end_square = start_square[0], 5
            else:
                rook_start_square = start_square[0], 0
                rook_end_square = start_square[0], 3
            rook = self.piece_locations.get(rook_start_square, None)
            self.buttons[rook_start_square].config(image='', width=self.square_size // 4, height=self.square_size // 8)
            self.buttons[rook_end_square].config(image=self.piece_images[rook], width=110, height=110)
            self.piece_locations[rook_end_square] = rook

        if self.chessboard.is_en_passant(move):
            self.buttons[(start_square[0], end_square[1])].config(image='', width=self.square_size // 4,
                                                                  height=self.square_size // 8)
            del self.piece_locations[(start_square[0], end_square[1])]

        self.master.game.make_move(start_square, end_square)

        self.piece_locations[end_square] = moving_piece
        self.update()
        del self.piece_locations[start_square]
        self.current_clicked = None
        self.de_color()
        self.check_if_game_end()

    def de_color(self):
        for button in self.buttons:
            color = colors[(button[0] + button[1]) % 2]
            self.buttons[button].config(bg=color, activebackground=color)

    def get_move(self, start_square, end_square):
        start_square = chess.square(start_square[1], start_square[0])
        end_square = chess.square(end_square[1], end_square[0])
        return chess.Move(start_square, end_square)

    def can_play(self):
        if self.master.game.side == 'white' and self.master.game.white_move:
            return True
        if self.master.game.side == 'black' and not self.master.game.white_move:
            return True


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_buttons()
        self.t = None
        self.interrupted = False
        self.master.game = None

    def create_buttons(self):
        play_button = tk.Button(self, width=100, height=20, text="Play", command=self.play)
        play_button.pack(pady=10)

        exit_button = tk.Button(self, width=100, height=20, text="Exit", command=self.exit)
        exit_button.pack(pady=10)

    def play(self):
        self.master.game = Game()
        for widget in self.winfo_children():
            widget.destroy()
        label = tk.Label(self, text="Waiting for game...", font=("Helvetica", 16))
        label.pack(pady=10)
        self.master.update()
        t = Thread(target=self.master.game.begin, daemon=True)
        t.start()
        self.schedule_check(t)

    def schedule_check(self, t):
        self.after(int(tick_timeout * 1000), self.check_if_began, t)

    def check_if_began(self, t):
        print('checking if the game is found')
        if not t.is_alive():
            print('not yet found')
            self.master.switch_frame(ChessBoard)
        else:
            self.schedule_check(t)

    def connection_error_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
        label = tk.Label(self, text='CONNECTION ERROR', font=("Helvetica", 16))
        label.pack(pady=10)

        go_back_button = tk.Button(self, text="Go back to main menu", width=100, height=20,
                                   command=lambda: self.master.switch_frame(MainMenu))
        go_back_button.pack(pady=10)

    def exit(self):
        self.master.quit()


class SimpleGUI(tk.Tk):
    game: Game or None

    def __init__(self):
        super().__init__()
        self.title("anonchess")
        self.geometry("1920x1080")
        self.game = None
        self._frame = None
        self.switch_frame(MainMenu)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


if __name__ == "__main__":
    app = SimpleGUI()
    app.mainloop()
