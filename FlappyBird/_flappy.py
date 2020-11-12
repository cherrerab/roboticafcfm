# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import random


# tamaño del canvas
WIN_WIDTH = 288
WIN_HEIGHT = 512

# obtener directorio actual
current_dir = os.getcwd()
img_dir = os.path.join( current_dir, 'FlappyBird/bin' )

# bird sprite
bird_path = os.path.join( img_dir, 'bird.png' )
BIRD_IMG = cv2.imread( bird_path, cv2.IMREAD_UNCHANGED )

# tubería sprite
pipe_path = os.path.join( img_dir, 'pipe.png' )
PIPE_IMG = cv2.imread( pipe_path, cv2.IMREAD_UNCHANGED )

# background sprite
bkgr_path = os.path.join( img_dir, 'bg.png' )
BKGR_IMG = cv2.imread( bkgr_path, cv2.IMREAD_UNCHANGED )

# ------------------------------------------------------------------------------
# definir clase Bird
class Bird:
  def __init__(self, x, y):
    # posición inicial
    self.x = x
    self.y = y

    # velocidad
    self.tick_count = 0
    self.vel = 0

    # display
    self.img = BIRD_IMG
    self.width = BIRD_IMG.shape[1]
    self.height = BIRD_IMG.shape[0] 

  def jump(self):
    self.vel = -6.75
    self.tick_count = 0

  def move(self):
    self.tick_count += 1

    d = self.vel*self.tick_count + self.tick_count**2

    # velocidad terminal
    if d >= 10.25:
      d = 10.25

    if d < 0:
      d -= 1.25

    # mover
    self.y = int( self.y + d )

    # adjust limits
    self.y = max(0, self.y)
    self.y = min(WIN_HEIGHT, self.y + self.height) - self.height

  def draw(self, canvas):

    # alpha mask
    alpha = self.img[:,:,3]/255.0

    # rectangle of interest
    x1 = self.x 
    x2 = self.x + self.width

    y1 = self.y
    y2 = self.y + self.height

    ROI = canvas[y1:y2, x1:x2, :]

    # dibujar
    for c in range(3):
      ROI[:,:,c] = np.multiply(ROI[:,:,c], 1 - alpha) + np.multiply(self.img[:,:,c], alpha)

    canvas[y1:y2, x1:x2, :] = ROI
    return canvas

# ------------------------------------------------------------------------------
# definir clase Pipe
class Pipe:
  VEL = 5

  def __init__(self, x):
    # posición inicial
    self.x = x

    # velocidad
    self.vel = 3.2

    # inicializar gap
    self.y = random.randint(100, 300)
    self.gap = 110

    self.top = self.y
    self.bottom = self.y + self.gap

    # display
    self.pipe_top = cv2.flip(PIPE_IMG, 0)
    self.pipe_bottom = PIPE_IMG

    self.height = self.pipe_bottom.shape[0]
    self.width = self.pipe_bottom.shape[1]

    # state
    self.passed = False

  def move(self):
    self.x = int( self.x - self.vel )

  def collide(self, bird):
    """
    -> bool
    Verifica si bird a chocado con pipe.
    """
    # si bird está entre pipe
    if (bird.x + bird.width > self.x) and (bird.x < self.x + self.width):
      if (bird.y < self.y) or (bird.y + bird.height > self.y + self.gap):
        # collide
        return True

  def draw(self, canvas):
    
    # top ----------------------------------------------------------------------

    # rectangle of interest
    x1 = min(WIN_WIDTH, max(0, self.x))
    x2 = min(WIN_WIDTH, max(0, self.x + self.width))

    y1 = 0
    y2 = self.y

    ix1 = 0 if self.x == x1 else x1 - self.x
    ix2 = self.width if self.x + self.width == x2 else self.width - (self.x + self.width - x2)

    iy1 = self.height - self.y
    iy2 = self.height

    ROI = canvas[y1:y2, x1:x2, :]

    IMROI = self.pipe_top[iy1:iy2, ix1:ix2, :]
    alpha = self.pipe_top[iy1:iy2, ix1:ix2, 3]/255.0

    for c in range(3):
      ROI[:,:,c] = np.multiply(ROI[:,:,c], 1 - alpha) + np.multiply(IMROI[:,:,c], alpha)

    canvas[y1:y2, x1:x2, :] = ROI

    # bottom -------------------------------------------------------------------

    # rectangle of interest
    x1 = min(WIN_WIDTH, max(0, self.x))
    x2 = min(WIN_WIDTH, max(0, self.x + self.width))

    y1 = self.y + self.gap
    y2 = WIN_HEIGHT

    ix1 = 0 if self.x == x1 else x1 - self.x
    ix2 = self.width if self.x + self.width == x2 else self.width - (self.x + self.width - x2)

    iy1 = 0
    iy2 = WIN_HEIGHT - (self.y + self.gap)

    ROI = canvas[y1:y2, x1:x2, :]

    IMROI = self.pipe_bottom[iy1:iy2, ix1:ix2, :]
    alpha = self.pipe_bottom[iy1:iy2, ix1:ix2, 3]/255.0

    for c in range(3):
      ROI[:,:,c] = np.multiply(ROI[:,:,c], 1 - alpha) + np.multiply(IMROI[:,:,c], alpha)

    canvas[y1:y2, x1:x2, :] = ROI
    return canvas

# ------------------------------------------------------------------------------
# dibujar frame
def draw_frame(birds, pipes, canvas):
  canvas = BKGR_IMG.copy()

  # dibujar pipes
  for pipe in pipes:
    canvas= pipe.draw(canvas)

  # dibujar bird
  for bird in birds:
    canvas = bird.draw(canvas)
    
  return canvas