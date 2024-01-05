import pygame
from constants import *

class MoveLog:
  def __init__(self):
    self.white_moves = []
    self.black_moves = []

    self.surf = pygame.Surface((MOVE_LOG_WIDTH, MOVE_LOG_HEIGHT))
    self.surf.fill(MOVE_LOG_COLOR)
    self.rect = self.surf.get_rect(topleft = MOVE_LOG_POS)

    self.scroll_pos = 0        
    self.scroll_bar = pygame.Rect(self.rect.right, self.rect.top, 10, MOVE_LOG_HEIGHT)

  def get_move(self, move, color):
    if color == 'white':
      self.white_moves.append(move)
    else:
      self.black_moves.append(move)

  def clear(self):
    self.white_moves = []
    self.black_moves = []

  def draw(self, screen):
    # displaying moves
    font = pygame.font.Font(None, 30)

    visible_white = self.white_moves[self.scroll_pos : self.scroll_pos + MOVE_LOG_HEIGHT // TEXT_PADDING]
    visible_black = self.black_moves[self.scroll_pos : self.scroll_pos + MOVE_LOG_HEIGHT // TEXT_PADDING]

    for i, white_move in enumerate(visible_white):
      text = str(self.white_moves.index(white_move) + 1) + ".  " + white_move
      displayed_text = font.render(text, True, TEXT_COLOR)
      text_rect = displayed_text.get_rect(topleft = (TEXT_POS[0] - LOGGER_WIDTH // 5, TEXT_POS[1] + i * TEXT_PADDING))
      screen.blit(displayed_text, text_rect)

    for j, black_move in enumerate(visible_black):
      displayed_text = font.render(black_move, True, TEXT_COLOR)
      text_rect = displayed_text.get_rect(topleft = (TEXT_POS[0] + LOGGER_WIDTH // 3, TEXT_POS[1] + j * TEXT_PADDING))
      screen.blit(displayed_text, text_rect)

    # scrollbar 
    pygame.draw.rect(screen, SCROLLBAR_COLOR, self.scroll_bar)
    if len(self.white_moves) > 0:
      indicator_height = MOVE_LOG_HEIGHT // len(self.white_moves)
      indicator_pos = self.rect.top + (self.scroll_pos * MOVE_LOG_HEIGHT // len(self.white_moves))
      pygame.draw.rect(screen, INDICATOR_COLOR, (self.scroll_bar.x, indicator_pos, self.scroll_bar.width, indicator_height))

class Logger:
  def __init__(self):
    self.white_moves = []
    self.black_moves = []

    self.surf = pygame.Surface((LOGGER_WIDTH, LOGGER_HEIGHT))
    self.rect = self.surf.get_rect(topleft = (800, 0))
    
    icon = pygame.image.load("images/chess_board.png")
    self.icon = pygame.transform.scale(icon, (100, 100))
    self.move_log = MoveLog()
    
  def get_move(self, move, color):
    if color == 'white':
      self.white_moves.append(move)
    else:
      self.black_moves.append(move)

  def draw(self, screen):
    self.surf.fill(LOGGER_COLOR)

    title_font = pygame.font.Font(None, 40)
    title = title_font.render("MOVES", True, TITLE_COLOR)
    title_rect = title.get_rect(center = TITLE_POS)

    icon_rect = self.icon.get_rect(midtop = self.rect.midtop)

    screen.blit(self.surf, self.rect.topleft)

    # title and icon
    screen.blit(title, title_rect)
    screen.blit(self.icon, icon_rect)

    # move log
    screen.blit(self.move_log.surf, self.move_log.rect)

    self.move_log.draw(screen)