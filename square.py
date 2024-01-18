import pygame
from constants import * 

class Square:
  def __init__(self, row, col, color):
    self.row = row
    self.col = col
    
    self.x = self.col * SQUARE_SIZE
    self.y = self.row * SQUARE_SIZE

    self.color = WHITE if color == 'white' else BLACK

    self.piece = None

    self.pointed = False 
    self.selected = False
    self.highlighted = False
    
    self.notation = None
    self.move_indicated = False

    self.rect = pygame.Rect(self.x, self.y, SQUARE_SIZE, SQUARE_SIZE)

  def draw(self, board, screen):
    # draw in check
    if self.piece is not None and self.piece.type == 'king' and board.in_check(self.piece.color):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
    else:
      pygame.draw.rect(screen, self.color, self.rect)
    # draw notations
    if self.row == 7 and self.col == 0:
      font = pygame.font.Font(None, 20)
      row_label = font.render("1", True, (0, 0, 0))
      col_label = font.render("a", True, (0, 0, 0))
      row_rect = row_label.get_rect(topleft = self.rect.topleft)
      col_rect = col_label.get_rect(bottomright = self.rect.bottomright)
      screen.blit(row_label, row_rect)
      screen.blit(col_label, col_rect)
    elif self.notation:
      font = pygame.font.Font(None, 20)
      label = font.render(str(self.notation), True, (0, 0, 0))
      rect = label.get_rect()
      if type(self.notation) == int:
        rect.topleft = self.rect.topleft
      else:
        rect.bottomright = self.rect.bottomright
      screen.blit(label, rect)
    # draw selection
    if self.selected and self.piece is not None:
      select_color = (0, 0, 255)
      pygame.draw.rect(screen, select_color, self.rect, 3)
    # draw indicator
    if self.move_indicated:
      indicated_color = SQUARE_INDICATOR_COLOR
      pygame.draw.rect(screen, indicated_color, self.rect, 5)
    # draw pieces
    if self.piece:
      image = self.piece.image
      center_rect = image.get_rect(center = self.rect.center)
      screen.blit(self.piece.image, center_rect.topleft)
    # highlights
    if self.highlighted:
      highlight_color = WHITE_HIGHLIGHT if board.selected_square.piece.color == 'white' else BLACK_HIGHLIGHT
      if self.piece is not None:
        pygame.draw.circle(screen, highlight_color, self.rect.center, SQUARE_SIZE // 2, 3)
      else:
        pygame.draw.circle(screen, highlight_color, self.rect.center, SQUARE_SIZE // 6, 3)
      if self.pointed:
        pygame.draw.rect(screen, highlight_color, self.rect, 3)