import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class Player:
    def __init__(self, name="", symbol=""):
        self.name = name
        self.symbol = symbol

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.geometry("780x600")  
        self.master.configure(bg="#f0f8ff")  

        self.create_database()

        self.players = [Player(), Player()]
        self.current_player_index = 0
        self.board = [None] * 9

        self.setup_entry_frame()

        self.buttons = []
        for i in range(9):
            button = ttk.Button(master, text="", style="TButton", command=lambda i=i: self.play_turn(i), width=10)
            button.grid(row=i // 3 + 5, column=i % 3, padx=10, pady=10)
            self.buttons.append(button)

        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=('Helvetica', 24), padding=20, relief='flat', background="#FFFFFF", foreground="#000000")
        style.map("TButton", background=[("active", "#c0c0c0"), ("pressed", "#a0a0a0")])  

        label_style = {'bg': "#f0f8ff", 'font': ('Helvetica', 14), 'fg': "#000080"}  
 

    def create_database(self):
        conn = sqlite3.connect('tic_tac_toe.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY,
            player1_name TEXT,
            player1_symbol TEXT,
            player2_name TEXT,
            player2_symbol TEXT,
            winner TEXT,
            result TEXT
        )''')
        conn.commit()
        conn.close()

    def save_game_result(self, winner_name, result):
        conn = sqlite3.connect('tic_tac_toe.db')
        c = conn.cursor()
        c.execute('''INSERT INTO game_results (player1_name, player1_symbol, player2_name, player2_symbol, winner, result)
                     VALUES (?, ?, ?, ?, ?, ?)''', (self.players[0].name, self.players[0].symbol, 
                                                      self.players[1].name, self.players[1].symbol, 
                                                      winner_name, result))
        conn.commit()
        conn.close()

    def fetch_game_results(self):
        conn = sqlite3.connect('tic_tac_toe.db')
        c = conn.cursor()
        c.execute('SELECT * FROM game_results')
        results = c.fetchall()
        conn.close()
        return results

    def show_game_results(self):
        results = self.fetch_game_results()
        result_message = "Game Results:\n"
        for row in results:
            result_message += f"Player 1: {row[1]} ({row[2]}) vs Player 2: {row[3]} ({row[4]}) - Winner: {row[5] if row[5] else 'Draw'}\n"
        
        messagebox.showinfo("Game Results", result_message)

    def setup_entry_frame(self):
        frame = ttk.Frame(self.master)
        frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Player 1 Name
        tk.Label(frame, text="Player 1 Name (X):", **{'bg': "#f0f8ff", 'font': ('Helvetica', 14), 'fg': "#000080"}).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.player1_name_entry = tk.Entry(frame, font=('Helvetica', 14))
        self.player1_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Player 1 Symbol
        tk.Label(frame, text="Player 1 Symbol:", **{'bg': "#f0f8ff", 'font': ('Helvetica', 14), 'fg': "#000080"}).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.player1_symbol_entry = tk.Entry(frame, width=5, font=('Helvetica', 14))
        self.player1_symbol_entry.grid(row=1, column=1, padx=10, pady=5)

        # Player 2 Name
        tk.Label(frame, text="Player 2 Name (O):", **{'bg': "#f0f8ff", 'font': ('Helvetica', 14), 'fg': "#000080"}).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.player2_name_entry = tk.Entry(frame, font=('Helvetica', 14))
        self.player2_name_entry.grid(row=2, column=1, padx=10, pady=5)

        # Player 2 Symbol
        tk.Label(frame, text="Player 2 Symbol:", **{'bg': "#f0f8ff", 'font': ('Helvetica', 14), 'fg': "#000080"}).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.player2_symbol_entry = tk.Entry(frame, width=5, font=('Helvetica', 14))
        self.player2_symbol_entry.grid(row=3, column=1, padx=10, pady=5)

        self.start_button = ttk.Button(frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=4, columnspan=2, pady=10)


    def start_game(self):
        player1_name = self.player1_name_entry.get()
        player1_symbol = self.player1_symbol_entry.get().upper()
        player2_name = self.player2_name_entry.get()
        player2_symbol = self.player2_symbol_entry.get().upper()

        # Validate symbols
        if len(player1_symbol) != 1 or len(player2_symbol) != 1 or player1_symbol == player2_symbol:
            messagebox.showerror("Invalid Input", "Please choose different single letter symbols for each player.")
            return

        self.players[0].name = player1_name
        self.players[0].symbol = player1_symbol
        self.players[1].name = player2_name
        self.players[1].symbol = player2_symbol
        
        self.reset_board()
        self.start_button.config(state=tk.DISABLED)

    def reset_board(self):
        for i in range(9):
            self.board[i] = None
            self.buttons[i].config(text="", state=tk.NORMAL)

    def play_turn(self, index):
        if self.board[index] is None:
            self.board[index] = self.players[self.current_player_index].symbol
            self.buttons[index].config(text=self.board[index], state=tk.DISABLED)
            if self.check_win():
                self.display_winner()
            elif None not in self.board:
                self.display_draw()
            else:
                self.switch_player()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def check_win(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] is not None):
                return True
        return False

    def display_winner(self):
        winner = self.players[self.current_player_index]
        self.save_game_result(winner.name, 'Win')
        self.show_game_results()
        response = messagebox.askyesno("Game Over", f"Congratulations {winner.name}! You win! Do you want to play again?")
        if response:
            self.reset_board()
        else:
            self.master.quit()

    def display_draw(self):
        self.save_game_result(None, 'Draw')
        self.show_game_results()
        response = messagebox.askyesno("Game Over", "It's a draw! Do you want to play again?")
        if response:
            self.reset_board()
        else:
            self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
