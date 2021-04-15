#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
class ChessBoard:
    """
    esta clase permite compilar imágenes de un tablero de ajedrez.
    al inicilizar un ChessBoard el tablero comienza vacío.
    """
    
    def __init__(self):
        module_path = os.path.abspath( inspect.getfile( inspect.currentframe() ) )
        module_path = os.path.dirname(module_path)
        bin_path = os.path.join( module_path, 'bin')
        
        self.bin_path = bin_path
        
        board_path = os.path.join(self.bin_path, 'board.png')
        self.board = cv2.imread( board_path )
        
        self.height = self.board.shape[0]
        self.width = self.board.shape[1]
        
        self.square = self.height/8.0
        
    def drawPiece(self, name, position=(0, 0)):
        """
        agrega la pieza name al tablero siguiendo la posición descrita
        por el parámetro position.
        """
        
        piece_png = '{:s}.png'.format(name)
        piece_path = os.path.join(self.bin_path, piece_png)
        
        piece_img = cv2.imread(piece_path, cv2.IMREAD_UNCHANGED)
        
        alpha = piece_img[:, :, 3]/255
        height, width, _ = piece_img.shape
        
        # determinar ROI
        y1 = int( self.square*position[0] )
        y2 = int( self.square*position[0] + height )
        
        x1 = int( self.square*position[1] )
        x2 = int( self.square*position[1] + width )
        
        ROI = self.board[y1:y2, x1:x2, :]
        
        # draw
        for c in range(3):
            ROI[:, :, c] = np.multiply(ROI[:,:,c], 1 - alpha) + np.multiply(piece_img[:,:,c], alpha)
        
        self.board[y1:y2, x1:x2, :] = ROI
    
    @property
    def image(self):
        """
        retorna la imagen BGR compilada del tablero.
        """
        return self.board
    
    def plot(self, figsize=(8, 8)):
        """
        gráfica mediante matplotlib.pyplot la imagen del tablero.
        """
        bgr = self.image
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        
        plt.figure( figsize=figsize )
        plt.imshow(rgb)
        plt.axis('off')
        
        
