# Chess Capture Project

## Project Description

This project is a Python-based chess board simulator that allows a user to:

1. Place one white chess piece on the board.
2. Place one or more black chess pieces on the board.
3. Determine which black pieces can be captured by the selected white piece according to chess movement rules.

The board is displayed using an 8x8 matrix and chess coordinates such as `a1`, `d4`, and `h8`.

---

## How to Run

### Requirements

* Python 3.10+
* Terminal or command line

### Run the program

```bash
python chess.py
```

Follow the prompts to:

1. Enter a white piece and position.
2. Enter black pieces and positions.
3. Type `done` when finished adding black pieces.

Example:

```text
Enter white piece and position: rook d4

Enter black piece and position: pawn d7
Enter black piece and position: bishop h4
Enter black piece and position: done
```

The program will then display all capturable black pieces.

---

## Implemented Requirements

### Board Creation

* 8x8 chess board created using nested lists.
* Chess coordinates are converted into board indexes.

### White Piece Input

* User can add a white piece.
* Input format validation is implemented.
* Piece validation is implemented.

### Black Piece Input

* User can add between 1 and 16 black pieces.
* User may type `done` only after at least one black piece has been added.
* Duplicate positions are prevented.

### Coordinate Validation

* Validates:

  * Column between `a` and `h`
  * Row between `1` and `8`
  * Correct coordinate length
  * Occupied squares

### Capture Detection

Currently implemented:

* Rook
* Pawn
* Knight
* Bishop

The program identifies black pieces that can be captured according to the movement rules of the selected white piece.

### Code Quality Improvements

* Type hints added throughout the project.
* Helper functions created to reduce duplicated code.
* Input validation separated into dedicated functions.
* Docstrings added to validation functions.

---

## Not Yet Implemented

### Missing Chess Pieces

Capture logic has not yet been implemented for:

* Queen
* King

### Advanced Chess Rules

The following are not supported:

* Check
* Checkmate
* Castling
* En passant
* Piece protection logic
* Full chess gameplay

The project focuses only on identifying capturable black pieces.

---

## Reviewer Feedback Still To Be Addressed

* Add missing docstrings for:

  * `main`
  * `add_white_piece`
  * `add_black_pieces`
  * `find_captures`

* Review unused parameters and remove any unnecessary arguments.

* Run a PEP 8 formatter such as:

  * Ruff
  * Black
  * Pylint
  * pycodestyle

* Simplify reverse column lookup logic.

Current implementation:

```python
list(col_map.keys())[list(col_map.values()).index(pos_col)]
```

Suggested implementation:

```python
next(key for key, value in col_map.items() if value == pos_col)
```

---

## Author

Precious Ikem
