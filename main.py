import pygame
import sys
from tkinter import messagebox
from constants import *
from board import Board

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
board = Board() 
move_log = board.logger.move_log

def restart():
  board.__init__()
  move_log.clear()

def end_game_popup(winner):
  messagebox.showinfo(title="Checkmate", message=f"{winner} wins!")
  response = messagebox.askyesno("Restart", "Do you want to restart?")
  if response:
    restart()
  else:
    pygame.quit()
    sys.exit()

while True:
  mx, my = pygame.mouse.get_pos()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit() 
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left mouse button only
      board.handle_click(mx, my)
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP and move_log.scroll_pos > 0:
        move_log.scroll_pos -= 1
      elif event.key == pygame.K_DOWN and move_log.scroll_pos < len(move_log.white_moves) - 1:
        move_log.scroll_pos += 1

  board.handle_pointing(mx, my)
  screen.fill('white')
  board.draw(screen)
  pygame.display.update()
  if board.check_mate:
    winner = 'white' if board.turn == 'black' else 'black'
    end_game_popup(winner)  
  clock.tick(FRAMERATE)