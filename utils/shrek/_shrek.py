# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import random

# -----------------------------------------------------------------------------
# inicializar assets

# tamaño del canvas
WIN_WIDTH = 576
WIN_HEIGHT = 512

# obtener directorio actual
current_dir = os.getcwd()
img_dir = os.path.join( current_dir, 'utils/shrek/bin' )

# tubería sprite
pipe_path = os.path.join( img_dir, 'pipe.png' )
PIPE_IMG = cv2.imread( pipe_path, cv2.IMREAD_UNCHANGED )

# background sprite
bkgr_path = os.path.join( img_dir, 'bg.png' )
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
  
# -----------------------------------------------------------------------------
def drawImage(canvas, img, pos):
    """
    -> np.array(np.uint8)
    
    agrega la imagen img al canvas en la posición (row, col) especificada en el
    parámetro pos.
    
    :param np.array(np.uint8) canvas:
        imagen RGB en donde se agregará la imagen img.
    :param np.array(np.uint8) img:
        imagen RGB-alpha que se desea agregar al canvas.
    :param tuple(int) pos:
        posición (row, col) en donde agregar la imagen.
        
    :returns:
        la imagen compilada.
    """
    out = canvas.copy()
    
    HEIGHT, WIDTH, _ = canvas.shape
    height, width, _ = img.shape
    
    i, j = pos
    
    if (j >= WIDTH) or (j + width < 0):
        return out
    if (i >= HEIGHT) or (i + height < 0):
        return out
    
    # definir ROI
    ri1, ri2 = max(i, 0), min(i + height, HEIGHT - 1)
    rj1, rj2 = max(j, 0), min(j + width, WIDTH - 1)
    
    # definir corte img
    i1, i2 = ri1 - i, ri2 - i
    j1, j2 = rj1 - j, rj2 - j
    
    ROI = out[ri1:ri2, rj1:rj2, :]
    IMROI = img[i1:i2, j1:j2, :]
    
    mask = IMROI[:, :, 3]
    mask = np.dstack([mask, mask, mask, mask])
    
    ret = cv2.bitwise_and(ROI, 255-mask) + cv2.bitwise_and(IMROI, mask)
    out[ri1:ri2, rj1:rj2, :] = ret
    return out

# -----------------------------------------------------------------------------
class Shrek:
    """
    clase que contiene los atributos necesarios para mantener un registro
    de la posición y acciones de un Shrek.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.tick_count = 0
        self.vel = 0
        
        self.jumping = False
        
        self.imgList = SHREK_IMG
        self.imgIndex = 0
        
        self.img = self.imgList[self.imgIndex]
        self.height, self.width, _ = self.img.shape
        
    def jump(self):
        """
        actualiza los atributos cinemáticos producto del salto de Bird.
        """
        if not(self.jumping):
            self.vel = -1.3
            self.tick_count = 0
            
            self.jumping = True

    def move(self):
        """
        actualiza los atributos cinemáticos en función del tiempo registrado
        port el atributo tick_count.
        """
        self.tick_count += 1
        
        a = 0.1
        d = self.vel*self.tick_count + (a/2.0)*self.tick_count**2
        
        if d >= 10.25:
            d = 10.25
        
        self.y = int( self.y + d )
        self.y = max(0, self.y - self.height) + self.height
        
        if self.y >= 400:
            self.y = 400
            self.vel = 0
            self.tick_count = 0
            
            self.jumping = False
            
    def draw(self, canvas):
        """
        -> np.array(np.uint8)
        
        agrega la imagen de Shrek sobre el canvas ingresado.
        """
        self.imgIndex += 1
        self.imgIndex = self.imgIndex%len(self.imgList)
        
        self.img = self.imgList[self.imgIndex]
        self.height, self.width, _ = self.img.shape
        
        return drawImage(canvas, self.img, (self.y - self.height, self.x))

# -----------------------------------------------------------------------------
class Pipe:

    def __init__(self, x, vel=8):
        self.x = x
        self.y = random.randint(300, 350)
        
        self.vel = vel
        
        self.img = PIPE_IMG
        self.height, self.width, _ = self.img.shape
        
        self.passed = False

    def move(self):
        """
        actualiza los atributos cinemáticos producto del movimiento de Pipe.
        """
        self.x = int( self.x - self.vel )

    def collide(self, shrek):
        """
        -> bool
        
        Verifica si shrek a chocado con la geometría de Pipe.
        """
        if (shrek.x + shrek.width > self.x) and (shrek.x < self.x + self.width):
            if (shrek.y > self.y):
                return True
    

    def draw(self, canvas):
        """
        -> np.array(np.uint8)
        
        agrega la imagen de Pipe sobre el canvas ingresado.
        """
        canvas = drawImage(canvas, self.img, (self.y, self.x))
        return canvas

# ------------------------------------------------------------------------------
class Base:

    def __init__(self, y, vel=8):
        self.y = y
        
        self.img = BASE_IMG
        self.height, self.width, _ = self.img.shape
        
        self.x1 = 0
        self.x2 = self.width
        
        self.vel = vel

    def move(self):
        """
        actualiza los atributos cinemáticos producto del movimiento de Base.
        """
        self.x1 = int( self.x1 - self.vel )
        self.x2 = int( self.x2 - self.vel )
        
        if self.x1 + self.width <= 0:
            self.x1 = self.x2 + self.width
        
        if self.x2 + self.width <= 0:
            self.x2 = self.x1 + self.width
            
    def draw(self, canvas):
        """
        -> np.array(np.uint8)
        
        agrega la imagen de Base sobre el canvas ingresado.
        """
        canvas = drawImage(canvas, self.img, (self.y, self.x1))
        canvas = drawImage(canvas, self.img, (self.y, self.x2))
        return canvas
    
# -----------------------------------------------------------------------------
def renderFrame(shreks, pipes, base):
    """
    -> np.array(np.uint8)
    
    compila la imagen con todos los elementos ingresados agregados.
    
    :param list(Bird) birds:
        lista de objetos Bird a agregar al cuadro.
    :param list(Pipe) pipes:
        lista de objetos Pipe a agregar al cuadro.
    """
    canvas = BKGR_IMG.copy()
    for pipe in pipes:
        canvas = pipe.draw(canvas)
    for shrek in shreks:
        canvas = shrek.draw(canvas)
        
    canvas = base.draw(canvas)
    return canvas[:, :, :3]
