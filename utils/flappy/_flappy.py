# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np

# -----------------------------------------------------------------------------
# inicializar assets

# tamaño del canvas
WIN_WIDTH = 288
WIN_HEIGHT = 512

# obtener directorio actual
current_dir = os.getcwd()
img_dir = os.path.join( current_dir, 'utils/flappy/bin' )

# bird sprite
bird_path = os.path.join( img_dir, 'bird.png' )
BIRD_IMG = cv2.imread( bird_path, cv2.IMREAD_UNCHANGED )

# tubería sprite
pipe_path = os.path.join( img_dir, 'pipe.png' )
PIPE_IMG = cv2.imread( pipe_path, cv2.IMREAD_UNCHANGED )

# background sprite
bkgr_path = os.path.join( img_dir, 'bg.png' )
BKGR_IMG = cv2.imread( bkgr_path, cv2.IMREAD_UNCHANGED )

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
class Bird():
    """
    clase que contiene los atributos necesarios para mantener un registro
    de la posición y acciones de un Bird.
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
        self.tick_count = 0
        self.vel = 0
    
        self.img = BIRD_IMG
        self.height, self.width, _ = BIRD_IMG.shape

    def jump(self):
        """
        actualiza los atributos cinemáticos producto del salto de Bird.
        """
        self.vel = -6.75
        self.tick_count = 0

    def move(self):
        """
        actualiza los atributos cinemáticos en función del tiempo registrado
        port el atributo tick_count.
        """
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
        """
        -> np.array(np.uint8)
        
        agrega la imagen de Bird sobre el canvas ingresado.
        """
        return drawImage(canvas, self.img, (self.y, self.x))

# -----------------------------------------------------------------------------
class Pipe():
    """
    clase que contiene los atributos necesarios para mantener un registro
    de la posición y acciones de un Bird.
    """
    
    def __init__(self, x):
        self.x = x
        
        self.vel = 3.2
        
        self.y = np.random.randint(100, 300)
        self.gap = 110
        
        self.top = self.y
        self.bottom = self.y + self.gap
        
        self.top_img = cv2.flip(PIPE_IMG, 0)
        self.bot_img = PIPE_IMG
        
        self.height, self.width, _ = self.bot_img.shape
        
        self.passed = False
        
    def move(self):
        """
        actualiza los atributos cinemáticos producto del movimiento de Pipe.
        """
        self.x = int( self.x - self.vel )
        
    def collide(self, bird):
        """
        -> bool
        
        Verifica si bird a chocado con la geometría de Pipe.
        """
        if (bird.x + bird.width > self.x) and (bird.x < self.x + self.width):
          if (bird.y < self.y) or (bird.y + bird.height > self.y + self.gap):
            return True
        
    def draw(self, canvas):
        """
        -> np.array(np.uint8)
        
        agrega la imagen de Pipe sobre el canvas ingresado.
        """
        canvas = drawImage(canvas, self.top_img, (self.top-self.height, self.x))
        canvas = drawImage(canvas, self.bot_img, (self.bottom, self.x))
        return canvas
        
# -----------------------------------------------------------------------------
def renderFrame(birds, pipes):
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
    for bird in birds:
        canvas = bird.draw(canvas)
    return canvas[:, :, :3]
    
    
    

