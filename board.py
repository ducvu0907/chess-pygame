from constants import *
from square import Square
from piece import *
from logger import Logger

class Board:
  def __init__(self):
    self.squares = [[Square(row, col, 'white' if (row + col) % 2 == 0 else 'black') for col in range(COLS)] for row in range(ROWS)]
    self.setup_board()
    self.selected_square = None
    self.turn = 'white'
    self.logger = Logger()
    self.check_mate = False
    self.from_square = None
    self.to_square = None

  def setup_board(self):
    # set up pawns
    for col in range(COLS):
      self.squares[1][col].piece = Pawn(1, col, 'black')
      self.squares[6][col].piece = Pawn(6, col, 'white')
    # set up rooks
    self.squares[0][0].piece = Rook(0, 0, 'black')
    self.squares[0][7].piece = Rook(0, 7, 'black')
    self.squares[7][0].piece = Rook(7, 0, 'white')
    self.squares[7][7].piece = Rook(7, 7, 'white')
    # set up knights
    self.squares[0][1].piece = Knight(0, 1, 'black')
    self.squares[0][6].piece = Knight(0, 6, 'black')
    self.squares[7][1].piece = Knight(7, 1, 'white')
    self.squares[7][6].piece = Knight(7, 6, 'white')
    # set up bishops
    self.squares[0][2].piece = Bishop(0, 2, 'black')
    self.squares[0][5].piece = Bishop(0, 5, 'black')
    self.squares[7][2].piece = Bishop(7, 2, 'white')
    self.squares[7][5].piece = Bishop(7, 5, 'white')
    # set up queens
    self.squares[0][3].piece = Queen(0, 3, 'black')
    self.squares[7][3].piece = Queen(7, 3, 'white')
    # set up kings
    self.squares[0][4].piece = King(0, 4, 'black')
    self.squares[7][4].piece = King(7, 4, 'white')
    # set up notations
    for row in range(ROWS):
      self.squares[row][0].notation = 8 - row
    for col, n in enumerate("abcdefgh"):
      self.squares[7][col].notation = n

  def get_square_from_pos(self, x, y):
    for row in self.squares:
      for square in row:
        if square.row == y and square.col == x:
          return square

  def handle_click(self, mx, my):
    x, y = int(mx // SQUARE_SIZE), int(my // SQUARE_SIZE)
    
    if not (0 <= x < 8 and 0 <= y < 8):
      return 
    if self.selected_square is None:
      chosen_square = self.get_square_from_pos(x, y)
      # check turn 
      if chosen_square.piece is not None and chosen_square.piece.color == self.turn:
        chosen_square.selected = not chosen_square.selected
      # handle squares
      if chosen_square.selected:
        self.selected_square = chosen_square
        move_squares = self.get_legal_squares(chosen_square)
        # move_squares = chosen_square.piece.get_valid_moves(self)
        for square in move_squares:
          square.highlighted = True
    else:
      dest_square = self.get_square_from_pos(x, y)
      # if dest_square in self.get_highlighted_squares():
      if dest_square in self.get_highlighted_squares():
        self.make_move(dest_square)
      # unselect and clear highlights
      self.selected_square.selected = False
      self.selected_square = None
      for row in self.squares:
        for square in row:
          square.highlighted = False

  # check legal moves
  def get_legal_squares(self, chosen_square):
    output = []
    piece = chosen_square.piece
    for dest_square in piece.get_valid_moves(self):
      captured_piece = dest_square.piece
      dest_square.piece = chosen_square.piece
      dest_square.piece.row = dest_square.row
      dest_square.piece.col = dest_square.col
      chosen_square.piece = None
      if not self.in_check(self.turn):
        output.append(dest_square)
      chosen_square.piece = dest_square.piece
      chosen_square.piece.row = chosen_square.row
      chosen_square.piece.col = chosen_square.col
      dest_square.piece = captured_piece
    return output

  # hovering squares
  def handle_pointing(self, mx, my):
    x, y = int(mx // SQUARE_SIZE), int(my // SQUARE_SIZE)
    pointed_square = self.get_square_from_pos(x, y)
    for square in self.get_highlighted_squares():
      if square == pointed_square:
        square.pointed = True
      else:
        square.pointed = False

  # queen only
  def promoted(self, dest_square):
    piece = dest_square.piece
    if piece.type == 'pawn':
      if piece.color == 'white' and piece.row == 0:
        dest_square.piece = Queen(dest_square.row, dest_square.col, 'white')
        return True
      elif piece.color == 'black' and piece.row == 7:
        dest_square.piece = Queen(dest_square.row, dest_square.col, 'black')
        return True
    return False

  def make_move(self, dest_square):
    move = None
    against_color = 'black' if self.turn == 'white' else 'white'
    castling_type = self.castling(dest_square)
    if castling_type is not None:
      row = 0 if self.turn == 'black' else 7
      if castling_type == 'queenside':
        self.squares[row][3].piece = self.squares[row][0].piece
        self.squares[row][3].piece.row = row
        self.squares[row][3].piece.col = 3
        self.squares[row][3].piece.has_moved = True
        self.squares[row][0].piece = None
        move = "O-O-O"
      elif castling_type == 'kingside':
        self.squares[row][5].piece = self.squares[row][7].piece
        self.squares[row][5].piece.row = row
        self.squares[row][5].piece.col = 5
        self.squares[row][5].piece.has_moved = True
        self.squares[row][7].piece = None
        move = "O-O"
    # update move for logger
    if move is None:
      move = self.selected_square.piece.notation
      if dest_square.piece is not None:
        dest_square.piece = None
        move += "x"
        if self.selected_square.piece.type == 'pawn':
          move = "e" + move
      move += COL_NOTATIONS[dest_square.col] + ROW_NOTATIONS[dest_square.row]
    # update the piece 
    dest_square.piece = self.selected_square.piece    
    dest_square.piece.row = dest_square.row        
    dest_square.piece.col = dest_square.col
    src_square = self.selected_square
    self.selected_square.piece = None
    # update indicator 
    if self.from_square:
      self.from_square.move_indicated = False
    if self.to_square:
      self.to_square.move_indicated = False
    self.from_square = src_square
    self.to_square = dest_square
    # update logger 
    if self.promoted(dest_square):
      move += "=Q"
    if self.in_checkmate(against_color):
      move += "#"
      self.check_mate = True
    elif self.in_check(against_color):
      move += "+"
    self.logger.move_log.get_move(move, self.turn)
    self.turn = 'black' if self.turn == 'white' else 'white'
    dest_square.piece.has_moved = True

  def castling(self, dest_square):
    piece = self.selected_square.piece
    if piece is not None and piece.type == 'king':
      if dest_square.col - piece.col == 2:
        return 'kingside'
      if dest_square.col - piece.col == -2:
        return 'queenside'
    return None

  def in_check(self, color):
    king_pos = None
    pieces = []
    for row in self.squares:
      for square in row:
        if square.piece is not None:
          pieces.append(square.piece)
    for piece in pieces:
      if piece.type == 'king' and piece.color == color:
        king_pos = (piece.row, piece.col)
        break
    prev_has_moved = None
    king = None
    for piece in pieces:
      if piece.color != color:
        # avoid infinite callbacks
        if piece.type == 'king':
          prev_has_moved = True if piece.has_moved else False
          king = piece
          piece.has_moved = True
        for square in piece.get_valid_moves(self):
          if (square.row, square.col) == king_pos:
            return True
    if king is not None:
      king.has_moved = prev_has_moved 
    return False

  def in_checkmate(self, color):
    king = None
    for row in self.squares:
      for square in row:
        if square.piece is not None and square.piece.type == 'king' and square.piece.color == color:
          king = square.piece
          break
    if king is None:
      return True
    if self.turn == color and self.in_check(color):
      return True
    for row in self.squares:
      for square in row:
        if square.piece is not None and square.piece.color == color:
          if self.get_legal_squares(square):
            return False 
    return True

  def get_highlighted_squares(self):
    output = []
    for row in self.squares:
      for square in row:
        if square.highlighted:
           output.append(square) 
    return output

  def draw(self, screen):
    if self.from_square:
      self.from_square.move_indicated = True
    if self.to_square:
      self.to_square.move_indicated = True
    for row in self.squares:
      for square in row:
        square.draw(self, screen)
    self.logger.turn = self.turn
    self.logger.draw(screen)