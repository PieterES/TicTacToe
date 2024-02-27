import random
import copy

# Globals
players = ['X', 'O']

def initialize_board():
    # return [[" " for _ in range(3)] for _ in range(3)]
    board = []
    for _ in range(3):
        row = []
        for _ in range(3):
            row.append(" ")
        board.append(row)
    return board


def draw_board(board):
    row_count = 0
    for row in board:
        print(" | ".join(row))
        row_count += 1
        if row_count < len(board):
            print("-"*10)

def check_winner(board):
    # check rows
    if board[0][0] == board[0][1] == board[0][2] != " ":
        return True
    if board[1][0] == board[1][1] == board[1][2] != " ":
        return True
    if board[2][0] == board[2][1] == board[2][2] != " ":
        return True

    # check columns
    if board[0][0] == board[1][0] == board[2][0] != " ":
        return True
    if board[0][1] == board[1][1] == board[2][1] != " ":
        return True
    if board[0][2] == board[1][2] == board[2][2] != " ":
        return True

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return True
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return True
    return False

def check_available_moves(board):
    available_moves = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == " ":
                available_moves.append((row,col))
    return available_moves

def random_move(board):
    return random.choice(check_available_moves(board))

def calculate_value(board, current_player):
    token = players[current_player]
    opponent = "O" if token == "X" else "X"
    score = 0
    opponent_score = 0
    for row in board:
        score += row.count(token)
        opponent_score += row.count(opponent)
        for i in range(len(row)-1):
            if row[i] == row[i + 1] == token:
                score += 1
            if row[i] == row[i + 1] == opponent:
                opponent_score += 1
        if row == [token, token, " "] or row == [token, " ", token] or row == [" ", token, token]:
            score += 1
        if row == [opponent, opponent, " "] or row == [opponent, " ", opponent] or row == [" ", opponent, opponent]:
            opponent_score += 1
        if row == [token, token, token]:
            score += 50
        if row == [opponent, opponent, opponent]:
            opponent_score += 50
    for col in range(3):
        column = [board[row][col] for row in range(3)]
        score += column.count(token)
        opponent_score += column.count(opponent)
        for i in range(len(column) - 1):
            if column[i] == column[i + 1] == token:
                score += 1
            if column[i] == column[i + 1] == opponent:
                opponent_score += 1
            if column == [token, token, " "] or column == [token, " ", token] or column == [" ", token, token]:
                score += 1
            if column == [opponent, opponent, " "] or column == [opponent, " ", opponent] or column == [" ", opponent, opponent]:
                opponent_score += 1
            if column == [token, token, token]:
                score += 50
            if column == [opponent, opponent, opponent]:
                opponent_score += 50

    diagonal1 = [board[i][i] for i in range(3)]
    diagonal2 = [board[i][2 - i] for i in range(3)]

    for i in range(len(diagonal1) - 1):
        if diagonal1[i] == diagonal1[i+1] == token:
            score += 3
        if diagonal1[i] == diagonal1[i+1] == opponent:
            opponent_score += 3
        if diagonal1 == [token, token, " "] or diagonal1 == [token, " ", token] or diagonal1 == [" ", token, token]:
            score += 2
        if diagonal1 == [opponent, opponent, " "] or diagonal1 == [opponent, " ", opponent] or diagonal1 == [" ", opponent, opponent]:
            opponent_score += 2
        if diagonal2[i] == diagonal2[i+1] == token:
            score += 3
        if diagonal2[i] == diagonal2[i+1] == opponent:
            opponent_score += 3
        if diagonal2 == [token, token, " "] or diagonal2 == [token, " ", token] or diagonal2 == [" ", token, token]:
            score += 2
        if diagonal2 == [opponent, opponent, " "] or diagonal2 == [opponent, " ", opponent] or diagonal2 == [" ", opponent, opponent]:
            opponent_score += 2
    if diagonal1 == [token, token, token]:
        score += 50
    if diagonal1 == [opponent, opponent, opponent]:
        opponent_score += 50
    if diagonal2 == [token, token, token]:
        score += 50
    if diagonal2 == [opponent, opponent, opponent]:
        opponent_score += 50
    score += diagonal1.count(token) + diagonal2.count(token)
    opponent_score += diagonal1.count(opponent) + diagonal2.count(opponent)

    return score - opponent_score

def get_opponent(player):
    opponent = 0 if player == 1 else 1
    return opponent

def minimax(board, depth, maximizing_player, player):
    if depth == 0 or game_over(board):
        return calculate_value(board, player)

    if maximizing_player:
        max_eval = float("-inf")
        for move in check_available_moves(board):
            new_board = simulate_move(board, move, player)
            eval = minimax(new_board, depth - 1, False, player)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for move in check_available_moves(board):
            new_board = simulate_move(board, move, get_opponent(player))
            eval = minimax(new_board, depth - 1, True, player)
            min_eval = min(min_eval, eval)
        return min_eval

def game_over(board):
    if not check_available_moves(board):
        return True
    if check_winner(board):
        return True
    return False
def simulate_move(board, move, current_player):
    new_board = copy.deepcopy(board)
    row, col = move[0], move[1]
    new_board[row][col] = players[current_player]
    return new_board
def get_best_move(board, depth, current_player):
    best_move = None
    max_eval = float("-inf")
    for move in check_available_moves(board):
        new_board = simulate_move(board, move, current_player)
        eval = minimax(new_board, depth, False, current_player)
        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move

def main():
    global players
    CPU = str(input("Enter if you want CPU or no (y/n): "))
    AI = True if CPU == 'y' else False
    depth = int(input("Enter depth (0 - 5): ")) if AI else 0
    current_player = random.choice([0, 1])

    board = initialize_board()
    draw_board(board)

    while True:
        if not check_available_moves(board):
            print('Draw!')
            return
        if AI and current_player % 2 == 1:
            if depth == 0:
                ai_move = random_move(board)
            else:
                ai_move = get_best_move(board, depth, current_player)
            row = ai_move[0]
            col = ai_move[1]
        else:
            row = int(input("Enter row number (0, 1, 2): "))
            col = int(input("Enter column number (0, 1, 2): "))

        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == " ":
            board[row][col] = players[current_player]
            draw_board(board)
            print()
            if check_winner(board):
                print(f"Player {players[current_player]} wins!")
                break
            current_player  = (current_player + 1) % 2
        else:
            print("Invalid mode, try again")

if __name__ == "__main__":
    main()

