def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    return None

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn")
        
        try:
            row = int(input("Enter row (1-3): ")) - 1
            col = int(input("Enter column (1-3): ")) - 1
        except ValueError:
            print("Invalid input. Please enter numbers between 1 and 3.")
            continue
        
        if row not in range(3) or col not in range(3) or board[row][col] != " ":
            print("Invalid move. Try again.")
            continue
        
        board[row][col] = current_player
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
