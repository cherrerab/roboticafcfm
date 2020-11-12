# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import random


# tamaño del canvas
WIN_WIDTH = 576
WIN_HEIGHT = 512

# obtener directorio actual
current_dir = os.getcwd()
img_dir = os.path.join( current_dir, 'shrek/bin' )

# tubería sprite
pipe_path = os.path.join( img_dir, 'pipe.png' )
PIPE_IMG = cv2.imread( pipe_path, cv2.IMREAD_UNCHANGED )

# background sprite
bkgr_path = os.path.join( img_dir, 'bg02.png' )
BKGR_IMG = cv2.imread( bkgr_path, cv2.IMREAD_UNCHANGED )

# base sprite
base_path = os.path.join( img_dir, 'base.png' )
BASE_IMG = cv2.imread( base_path, cv2.IMREAD_UNCHANGED )

# shrek sprites
SHREK_IMG = []
for i in range(16):
  img_path = os.path.join(img_dir, 'shrek%02d.png' %(i))
  img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
  img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))
  SHREK_IMG.append(img)


class Shrek:
  def __init__(self, x, y):
    # posición inicial
    self.x = x
    self.y = y

    # movimiento
    self.vel = 0
    self.tick_count = 0

    self.jumping = False

    # display
    self.imgs = SHREK_IMG
    self.img_idx = 0
    self.img = self.imgs[self.img_idx]

    self.width = self.img.shape[1]
    self.height = self.img.shape[0]

  def jump(self):
    if not(self.jumping):
      self.vel = -1.3
      self.tick_count = 0
      self.jumping = True

  def move(self):
    self.tick_count += 1

    # calcular desplazamiento
    a = 0.1
    d = self.vel*self.tick_count + (a/2.0)*self.tick_count**2

    # velocidad terminal
    if d >= 10.25:
      d = 10.25

    # mover
    self.y = int( self.y + d )

    # adjust limits (chocar con el cielo)
    self.y = max(0, self.y - self.height) + self.height

    # tocar el suelo
    if self.y >= 400:
      self.y = 400
      self.vel = 0
      self.tick_count = 0

      self.jumping = False

  def draw(self, frame_count):
    global canvas

    # change sprite by frame
    self.img_idx += 1
    self.img_idx = self.img_idx%len(self.imgs)
    self.img = self.imgs[self.img_idx]

    # alpha mask
    alpha = self.img[:,:,3]/255.0

    # rectangle of interest
    x1 = self.x 
    x2 = self.x + self.width

    y1 = self.y - self.height
    y2 = self.y

    ROI = canvas[y1:y2, x1:x2, :]

    # dibujar
    for c in range(3):
      ROI[:,:,c] = np.multiply(ROI[:,:,c], 1 - alpha) + np.multiply(self.img[:,:,c], alpha)

    # modificar canvas
    canvas[y1:y2, x1:x2, :] = ROI

# ------------------------------------------------------------------------------
# definir clase Pipe
class Pipe:

  def __init__(self, x, vel=8):
    # posición inicial
    self.x = x
    self.y = random.randint(300, 350)

    # velocidad
    self.vel = vel

    # display
    self.img = PIPE_IMG

    self.height = self.img.shape[0]
    self.width = self.img.shape[1]

    # state
    self.passed = False

  def move(self):
    self.x = int( self.x - self.vel )

  def collide(self, shrek):
    """
    -> bool
    Verifica si bird a chocado con pipe.
    """
    # si shrek está entre pipe
    if (shrek.x + shrek.width > self.x) and (shrek.x < self.x + self.width):
      if (shrek.y > self.y):
        # collide
        return True

  def draw(self):
    global canvas

    # bottom -------------------------------------------------------------------

    # rectangle of interest
    x1 = min(WIN_WIDTH, max(0, self.x))
    x2 = min(WIN_WIDTH, max(0, self.x + self.width))

    y1 = self.y
    y2 = WIN_HEIGHT

    ix1 = 0 if self.x == x1 else x1 - self.x
    ix2 = self.width if self.x + self.width == x2 else self.width - (self.x + self.width - x2)

    iy1 = 0
    iy2 = WIN_HEIGHT - self.y

    ROI = canvas[y1:y2, x1:x2, :]

    IMROI = self.img[iy1:iy2, ix1:ix2, :]
    alpha = self.img[iy1:iy2, ix1:ix2, 3]/255.0

    for c in range(3):
      ROI[:,:,c] = np.multiply(ROI[:,:,c], 1 - alpha) + np.multiply(IMROI[:,:,c], alpha)

    canvas[y1:y2, x1:x2, :] = ROI


# ------------------------------------------------------------------------------
class Base:

  def __init__(self, y, vel=8):
    self.y = y
    self.img = BASE_IMG
    self.width = self.img.shape[1]
    self.height = self.img.shape[0]

    self.x1 = 0
    self.x2 = self.width

    self.vel = vel

  def move(self):

    self.x1 = int( self.x1 - self.vel )
    self.x2 = int( self.x2 - self.vel )

    if self.x1 + self.width < 0:
        self.x1 = self.x2 + self.width

    if self.x2 + self.width < 0:
        self.x2 = self.x1 + self.width

  def draw(self):
    global canvas

    # --------------------------------------------------------------------------
    # rectangle of interest
    x1 = min(WIN_WIDTH, max(0, self.x1))
    x2 = min(WIN_WIDTH, max(0, self.x1 + self.width))

    y1 = self.y
    y2 = WIN_HEIGHT

    ix1 = 0 if self.x1 == x1 else x1 - self.x1
    ix2 = self.width if self.x1 + self.width == x2 else self.width - (self.x1 + self.width - x2)

    iy1 = 0
    iy2 = WIN_HEIGHT - self.y

    ROI = canvas[y1:y2, x1:x2, :]

    IMROI = self.img[iy1:iy2, ix1:ix2, :]
    alpha = np.ones_like(IMROI[:,:,0])

    for c in range(3):
      ROI[:,:,c] = np.multiply(ROI[:,:,c], 1 - alpha) + np.multiply(IMROI[:,:,c], alpha)

    canvas[y1:y2, x1:x2, :] = ROI

    # --------------------------------------------------------------------------
    # rectangle of interest
    x1 = min(WIN_WIDTH, max(0, self.x2))
    x2 = min(WIN_WIDTH, max(0, self.x2 + self.width))

    y1 = self.y
    y2 = WIN_HEIGHT

    ix1 = 0 if self.x2 == x1 else x1 - self.x2
    ix2 = self.width if self.x2 + self.width == x2 else self.width - (self.x2 + self.width - x2)

    iy1 = 0
    iy2 = WIN_HEIGHT - self.y

    ROI = canvas[y1:y2, x1:x2, :]

    IMROI = self.img[iy1:iy2, ix1:ix2, :]
    alpha = np.ones_like(IMROI[:,:,0])

    for c in range(3):
      ROI[:,:,c] = np.multiply(ROI[:,:,c], 1 - alpha) + np.multiply(IMROI[:,:,c], alpha)

    canvas[y1:y2, x1:x2, :] = ROI

# ------------------------------------------------------------------------------
# dibujar frame
def draw_frame(shreks, pipes, base, frame_count):
  global canvas
  canvas = BKGR_IMG.copy()

  # dibujar pipes
  for pipe in pipes:
    pipe.draw()

  # dibujar bird
  for shrek in shreks:
    shrek.draw(frame_count)

  # dibujar base
  base.draw()
