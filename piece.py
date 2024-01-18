import pygame
from constants import * 

class Piece:
  def __init__(self, row, col, color, type):
    self.row = row
    self.col = col

    self.color = color
    self.type = type

    # image_path = f"images/{self.color}_{self.type}.png"
    image_path = f"Projects/py_projects/chess/images/{self.color}_{self.type}.png" # full path
    self.image = pygame.image.load(image_path)
    
    self.has_moved = False

  def get_valid_moves(self, board):
    output = []
    for move in self.get_all_moves():
      dest_row, dest_col = move
      if self.is_valid_move(dest_row, dest_col, board):
        output.append(board.squares[dest_row][dest_col])
    return output

  def is_valid_move(self, dest_row, dest_col, board):
    if not (0 <= dest_row < ROWS and 0 <= dest_col < COLS):
      return False
    square = board.squares[dest_row][dest_col]
    return square.piece is None or square.piece.color != self.color

class Pawn(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color, 'pawn')
    self.notation = ""
    
  def get_all_moves(self):
    direction = -1 if self.color == 'white' else 1
    moves = [
      (self.row + direction, self.col),
      (self.row + direction, self.col - 1),
      (self.row + direction, self.col + 1),
      (self.row + 2 * direction, self.col)
    ]
    return moves

  def is_valid_move(self, dest_row, dest_col, board):
    if not (0 <= dest_row < ROWS and 0 <= dest_col < COLS):
      return False

    direction = -1 if self.color == 'white' else 1
    squares = board.squares    

    if dest_col == self.col and dest_row == self.row + direction:
      return squares[dest_row][dest_col].piece is None
    # first move
    if (dest_col == self.col
      and dest_row == self.row + 2 * direction
      and not self.has_moved
      and squares[self.row + direction][self.col].piece is None
      and squares[dest_row][dest_col].piece is None):
      return True
    # capture diagonally
    if (dest_row == self.row + direction
      and dest_col in {self.col + 1, self.col - 1}
      and squares[dest_row][dest_col].piece is not None
      and squares[dest_row][dest_col].piece.color != self.color):
      return True

class Rook(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color, 'rook')
    self.notation = 'R'

  def get_all_moves(self):
    moves = []
    for c in range(COLS):
      if c != self.col:
        moves.append((self.row, c))
    for r in range(ROWS):
      if r != self.row:
        moves.append((r, self.col))
    return moves
  
  def is_valid_move(self, dest_row, dest_col, board):
    if not (0 <= dest_row < ROWS and 0 <= dest_col < COLS):
      return False
    if dest_row != self.row and dest_col != self.col:
      return False
    # check paths
    if dest_row == self.row:
      start, end = min(self.col, dest_col), max(self.col, dest_col)
      for col in range(start + 1, end):
        if board.squares[self.row][col].piece is not None:
          return False
    elif dest_col == self.col:
      start, end = min(self.row, dest_row), max(self.row, dest_row)
      for row in range(start + 1, end):
        if board.squares[row][self.col].piece is not None:
          return False

    square = board.squares[dest_row][dest_col]
    return square.piece is None or square.piece.color != self.color

class Knight(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color, 'knight')
    self.notation = 'N'
  
  def get_all_moves(self):
    moves = []
    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for row, col in offsets:
      moves.append((self.row + row, self.col + col))
    return moves

class Bishop(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color, 'bishop')
    self.notation = 'B'

  def get_all_moves(self):
    moves = []
    for i in range(1, ROWS):
      moves.append((self.row + i, self.col + i))
      moves.append((self.row + i, self.col - i))
      moves.append((self.row - i, self.col + i))
      moves.append((self.row - i, self.col - i))
    return moves 

  def is_valid_move(self, dest_row, dest_col, board):
    if not (0 <= dest_row < ROWS and 0 <= dest_col < COLS):
      return False
    # check paths
    step_row = 1 if dest_row > self.row else -1
    step_col = 1 if dest_col > self.col else -1
    row, col = self.row + step_row, self.col + step_col
    while row != dest_row and col != dest_col:
      if board.squares[row][col].piece is not None:
        return False
      row += step_row
      col += step_col

    square = board.squares[dest_row][dest_col]
    return square.piece is None or square.piece.color != self.color  

class Queen(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color, 'queen')
    self.notation = 'Q'
  def get_all_moves(self):
    moves = []
    for move in Rook.get_all_moves(self):
      moves.append(move)
    for move in Bishop.get_all_moves(self):
      moves.append(move)
    return moves

  def is_valid_move(self, dest_row, dest_col, board):
    if not (0 <= dest_row < ROWS and 0 <= dest_col < COLS):
      return False
    # horizontal paths
    if dest_row == self.row:
      start, end = min(self.col, dest_col), max(self.col, dest_col)
      for col in range(start + 1, end):
        if board.squares[self.row][col].piece is not None:
          return False
    # vertical paths
    elif dest_col == self.col:
      start, end = min(self.row, dest_row), max(self.row, dest_row)
      for row in range(start + 1, end):
        if board.squares[row][self.col].piece is not None:
          return False
    # diagonal paths
    else:
      step_row = 1 if dest_row > self.row else -1
      step_col = 1 if dest_col > self.col else -1
      row, col = self.row + step_row, self.col + step_col
      while row != dest_row and col != dest_col:
        if board.squares[row][col].piece is not None:
          return False
        row += step_row
        col += step_col
    square = board.squares[dest_row][dest_col]
    return square.piece is None or square.piece.color != self.color

class King(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color, 'king')
    self.notation = 'K'

  def get_all_moves(self):
    moves = []        
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    for row, col in offsets:
      moves.append((self.row + row, self.col + col))
    return moves

  def can_castle(self, board):
    output = []
    if not self.has_moved and not board.in_check(self.color):
      row_index = self.row
      kingside_rook = board.squares[row_index][7].piece
      queenside_rook = board.squares[row_index][0].piece
      if kingside_rook and not kingside_rook.has_moved and all(board.squares[row_index][i].piece is None for i in range(5, 7)):
        output.append('kingside')
      if queenside_rook and not queenside_rook.has_moved and all(board.squares[row_index][i].piece is None for i in range(1, 4)):
        output.append('queenside')
    return output

  def get_valid_moves(self, board):
    output = []
    for move in self.get_all_moves():
      dest_row, dest_col = move
      if self.is_valid_move(dest_row, dest_col, board):
        output.append(board.squares[dest_row][dest_col])
    # castling
    for side in self.can_castle(board):
      if side == 'queenside':
        output.append(board.squares[self.row][self.col - 2])
      elif side == 'kingside':
        output.append(board.squares[self.row][self.col + 2])
    return output