from typing import List, Tuple, Optional, Dict


def main() -> None:
    """
    Main function to set up the chess board, add pieces, and find capturable pieces.
    """
    # Moved col_map here to be local to main()
    col_map: Dict[str, int] = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }

    board: List[List[str]] = create_board()
    print_board(board)
    # Pass col_map to functions that need it
    white_piece, white_row, white_column = add_white_piece(board, col_map)

    # Pass col_map to functions that need it
    add_black_pieces(board, col_map)

    captures = find_captures(board, white_piece, white_row, white_column)

    if captures:
        print("Capturable pieces:")
        for piece, pos_row, pos_col in captures:
            # Convert 0-indexed row to 1-indexed chess row
            # Convert 0-indexed col to char chess column using col_map
            chess_row = 8 - pos_row
            # Reverse lookup for column character
            chess_col = next(key for key, value in col_map.items() if value == pos_col)
            print(f"- {piece} at {chess_col}{chess_row}")
    else:
        print("No capturable pieces found.")


def create_board() -> List[List[str]]:
    board: List[List[str]] = [["__"] * 8 for _ in range(8)]
    return board


def print_board(board: List[List[str]]) -> None:
    for i, row in enumerate(board):
        print(8 - i, end=": ")
        for square in row:
            print(square, end=" ")
        print()
    print("   a  b  c  d  e  f  g  h")


def _get_validated_coords(
    coordinate: str, board: List[List[str]], col_map: Dict[str, int]
) -> Optional[Tuple[int, int]]:
    """
    Validates a chess coordinate string and converts it to 0-indexed board coordinates.

    Args:
        coordinate: The chess coordinate string (e.g., 'a1').
        board: The current state of the chess board.
        col_map: A dictionary mapping column characters to 0-indexed integers.

    Returns:
        A tuple (row_idx, column_idx) if valid and unoccupied, otherwise None.
    """
    if len(coordinate) != 2:
        print("Invalid coordinate format (e.g., 'a1')")
        return None

    col_char = coordinate[0]
    row_char = coordinate[1]

    if col_char not in col_map:
        print("Invalid column (must be 'a' through 'h')")
        return None

    if not row_char.isdigit():
        print("Invalid row (must be a digit)")
        return None

    row_int = int(row_char)
    if not (1 <= row_int <= 8):
        print("Row must be between 1 and 8")
        return None

    column_idx = col_map[col_char]
    row_idx = 8 - row_int  # Convert to 0-indexed board row

    # Check if the square is already occupied by any piece
    if board[row_idx][column_idx] != "__":
        print(f"Cannot place piece on an occupied square: {col_char}{row_int}")
        return None

    return row_idx, column_idx


def _validate_piece(piece: str, valid_pieces: List[str], piece_color: str) -> bool:
    """
    Validates if a given piece string is in the list of valid pieces for a given color.

    Args:
        piece: The name of the piece (e.g., 'rook', 'pawn').
        valid_pieces: A list of valid piece names for the color.
        piece_color: The color of the piece ('white' or 'black').

    Returns:
        True if the piece is valid, False otherwise.
    """
    if piece not in valid_pieces:
        print(f"Invalid {piece_color} piece. Must be one of {', '.join(valid_pieces)}.")
        return False
    return True


def _get_piece_and_coordinate_input(
    prompt_message: str, allow_done: bool = False
) -> Optional[Tuple[str, str]]:
    """
    Prompts the user for piece and coordinate input, handles basic format and 'done' command.
    Returns (piece, coordinate) tuple or None if 'done' or invalid format.
    """
    while True:
        user_input: str = input(prompt_message)
        if allow_done and user_input.lower() == "done":
            return None  # Signal for 'done'

        splitted_input: List[str] = user_input.split(" ")
        if len(splitted_input) != 2:
            print("Invalid input format. Please use 'piece coordinate'.")
            continue
        return splitted_input[0].lower(), splitted_input[1].lower()


def add_white_piece(
    board: List[List[str]], col_map: Dict[str, int]
) -> Tuple[str, int, int]:
    """
    Prompts the user to add a white piece to the board, validates input, and places the piece.

    Args:
        board: The current state of the chess board.
        col_map: A dictionary mapping column characters to 0-indexed integers.

    Returns:
        A tuple containing the white piece name, its row index, and column index.
    """
    valid_white_pieces: List[str] = ["rook", "pawn", "knight", "bishop"]

    while True:
        parsed_input = _get_piece_and_coordinate_input(
            "Enter white piece and position (e.g., 'rook d4'): "
        )

        # _get_piece_and_coordinate_input should not return None for white piece placement (no 'done' allowed)
        if parsed_input is None:
            continue  # Should not happen based on current usage

        piece, coordinate = parsed_input

        if not _validate_piece(piece, valid_white_pieces, "white"):
            continue

        validated_coords: Optional[Tuple[int, int]] = _get_validated_coords(
            coordinate, board, col_map
        )
        if validated_coords is None:
            continue

        row_idx, column_idx = validated_coords

        board[row_idx][column_idx] = piece
        print_board(board)
        return piece, row_idx, column_idx


def add_black_pieces(board: List[List[str]], col_map: Dict[str, int]) -> None:
    """
    Prompts the user to add black pieces to the board until 'done' is entered, validating each input.

    Args:
        board: The current state of the chess board.
        col_map: A dictionary mapping column characters to 0-indexed integers.
    """
    valid_black_pieces: List[str] = [
        "pawn",
        "rook",
        "bishop",
        "knight",
        "queen",
        "king",
    ]
    counter: int = 0

    while True:
        parsed_input = _get_piece_and_coordinate_input(
            "Enter black piece and position (e.g., 'pawn a7') or 'done' to finish: ",
            allow_done=True,
        )

        if parsed_input is None:  # User entered 'done'
            if counter > 0:
                break
            else:
                print("Add at least one black piece first.")
                continue

        if counter >= 16:
            print("Maximum black pieces reached (16). Cannot add more.")
            break

        piece, coordinate = parsed_input

        if not _validate_piece(piece, valid_black_pieces, "black"):
            continue

        validated_coords: Optional[Tuple[int, int]] = _get_validated_coords(
            coordinate, board, col_map
        )
        if validated_coords is None:
            continue

        row_idx, column_idx = validated_coords

        board[row_idx][column_idx] = "b_" + piece
        counter += 1
        print_board(board)


def find_captures(
    board: List[List[str]], white_piece: str, white_row: int, white_column: int
) -> List[Tuple[str, int, int]]:
    """
    Finds all capturable black pieces for a given white piece at a specific position.

    Args:
        board: The current state of the chess board.
        white_piece: The type of the white piece (e.g., 'rook', 'pawn', 'knight', 'bishop').
        white_row: The 0-indexed row of the white piece.
        white_column: The 0-indexed column of the white piece.

    Returns:
        A list of tuples, where each tuple contains (piece_name, row_idx, col_idx)
        of a capturable black piece.
    """
    capturable_pieces: List[Tuple[str, int, int]] = []

    def _check_and_add_capture(r, c):
        if 0 <= r < 8 and 0 <= c < 8:
            square_content: str = board[r][c]
            if square_content.startswith("b_"):
                capturable_pieces.append((square_content, r, c))
            return (
                square_content != "__"
            )  # Return True if any piece (black or white) is found
        return False

    if white_piece == "rook":
        directions: List[Tuple[int, int]] = [
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1),  # Right
        ]

        for dr, dc in directions:
            current_row, current_col = white_row + dr, white_column + dc

            while 0 <= current_row < 8 and 0 <= current_col < 8:
                square_content: str = board[current_row][current_col]

                if square_content == "__":  # Empty square, continue in this direction
                    current_row += dr
                    current_col += dc
                elif not square_content.startswith(
                    "b_"
                ):  # Encountered a white piece, stop in this direction
                    break
                else:  # Encountered a black piece, it's capturable, add and stop
                    capturable_pieces.append((square_content, current_row, current_col))
                    break

    elif white_piece == "pawn":
        # White pawn captures diagonally forward (row - 1)
        # Column - 1 (left) and Column + 1 (right)
        potential_captures = [
            (white_row - 1, white_column - 1),
            (white_row - 1, white_column + 1),
        ]
        for r, c in potential_captures:
            _check_and_add_capture(r, c)

    elif white_piece == "knight":
        knight_moves: List[Tuple[int, int]] = [
            (white_row + 2, white_column + 1),
            (white_row + 2, white_column - 1),
            (white_row - 2, white_column + 1),
            (white_row - 2, white_column - 1),
            (white_row + 1, white_column + 2),
            (white_row + 1, white_column - 2),
            (white_row - 1, white_column + 2),
            (white_row - 1, white_column - 2),
        ]
        for r, c in knight_moves:
            _check_and_add_capture(r, c)

    elif white_piece == "bishop":
        diagonal_directions: List[Tuple[int, int]] = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        for dr, dc in diagonal_directions:
            current_row, current_col = white_row + dr, white_column + dc
            while 0 <= current_row < 8 and 0 <= current_col < 8:
                square_content: str = board[current_row][current_col]
                if square_content == "__":
                    current_row += dr
                    current_col += dc
                elif not square_content.startswith("b_"):
                    break
                else:
                    capturable_pieces.append((square_content, current_row, current_col))
                    break

    return capturable_pieces


if __name__ == "__main__":
    main()
