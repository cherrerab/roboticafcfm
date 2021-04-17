#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
import numpy as np
import cv2

# ----------------------------------------------------------------------------
# plotear rectas sobre la imagen
def plot_lines(img, lines, color=(255, 0, 255)):
    """
    -> np.array
    
    gráfica las rectas ingresadas sobre la imagen, retornando el arreglo
    numérico modificado.
    
    :param np.array img:
        imagen donde se dibujarán las rectas.
    :param list lines:
        serie de tuplas de la forma (rho, theta) que definen las rectas
        a intersectar.
        
    :returns:
        arreglo numérico con la imagen modificada.
    """
    newImage = img.copy()
    
    for rho, theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        
        newImage= cv2.line(newImage, (x1,y1), (x2,y2), color, 2)
    
    plt.imshow(newImage)
    return None

# ----------------------------------------------------------------------------
# plotear esquinas sobre la imagen
def plot_corners(img, corners, size=5, color=(255, 0, 255)):
    """
    -> np.array
    
    gráfica las puntos ingresados sobre la imagen como círculos, retornando
    el arreglo modificado.
    """
    newImage = img.copy()
    
    for i in range(corners.shape[0]):
        x, y = corners[i, :]
        
        newImage = cv2.circle(newImage, (x, y), size, color, 2 )
        
    plt.imshow(newImage)
    return None

# ----------------------------------------------------------------------------
# organizar coordenadas espacialmente
def sort_coords(coords):
    """
    -> np.array
    
    ordena las coordenadas ingresadas siguiendo un arreglo de malla
    rectangular, comenzando por la esquina superior izquierda.
    
    :param np.array coords:
        arreglo numérico de la forma (npoints, 2) con los pares (x, y)
        a ordenar geométricamente.
        
    :returns:
        arreglo numérico de la forma (npoints, 2) con los pares (x, y)
        ordenados.
    """
    new_coords = list()
    x = coords[:, 0].flatten()
    y = coords[:, 1].flatten()
    
    while x.size > 0:
        row_idx = np.where( np.abs( y - np.min(y) ) < 30 )[0]
        row_x, row_y = x[row_idx], y[row_idx]
        
        sort_idx = np.argsort(row_x)
        row_x, row_y = row_x[sort_idx], row_y[sort_idx]
        
        new_coords.append( np.vstack( [row_x, row_y] ).T )
        
        x = np.delete(x, row_idx, axis=None)
        y = np.delete(y, row_idx, axis=None)
        
    return np.vstack(new_coords) 
    
# ----------------------------------------------------------------------------
# obtener coordenadas de intersección
def get_intersections(img, lines):
    """
    -> np.array
    
    obtiene los puntos de intersección al interior de la imagen en función de
    la serie de rectas (rho, theta) ingresadas.
    
    :param np.array img:
        imagen que define los límites de busqueda de intersección.
    :param list lines:
        serie de tuplas de la forma (rho, theta) que definen las rectas
        a intersectar.
        
    :returns:
        arreglo numérico de la forma (nintersections, 2) con los pares de
        puntos (x, y) que describen los puntos de intersección en la imagen.
    """
    # inicializar imagen de intersección
    foo = np.zeros( (img.shape[0], img.shape[1], 1), dtype=np.uint8)
    
    # para cada recta en lines
    for rho, theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1, x2 = int(x0 + 1000*(-b)), int(x0 - 1000*(-b))
        y1, y2 = int(y0 + 1000*(a)), int(y0 - 1000*(a))
        
        # agregar recta
        mask = np.zeros_like(foo)
        cv2.line(mask, (x1,y1), (x2,y2), 1, 1)
        foo = foo + mask
        
    # obtener puntos de intersección
    y, x, _ = np.where( (foo > 1) )
    coords = np.vstack( [x, y] ).T
    
    return sort_coords(coords)

# ----------------------------------------------------------------------------
# aumentar resolución de contorno
def refine_contour(contour, res=500):
    """
    -> np.array
    
    aumenta la resolución de puntos de la serie de vertices ingresadas en
    función de la resolución ingresada.
    
    :param np.array contour:
        conjunto de puntos (x, y) que describen el contorno del perfil.
        este debe ser de la forma (npoints, 2)
        
    :param float res:
        resolución de puntos a generar en cada segmento del contorno.
        
    :returns:
        arreglo numérico de la forma (npoints, 2) con el contorno refinado.
    """
    # ---
    # procesar contorno
    if (len(contour.shape) != 2) or (contour.shape[1] != 2):
        raise ValueError('contour must be a (npoints, 2) array')
        
    if (contour[0, :] != contour[-1, :]).any():
        contour = np.vstack( [contour, contour[0, :]] )
        
    n_points, _ = contour.shape
    
    # ---
    # inicializar contorno    
    new_contour = list()

    # interpolar contorno
    for i in range(n_points - 1):
        x1, y1 = contour[i, :]
        x2, y2 = contour[i+1, :]
        
        x = np.linspace(x1, x2, num=res)
        y = np.linspace(y1, y2, num=res)
        
        new_contour.append( np.vstack([x, y]).T )

    new_contour = np.vstack( new_contour )
        
    return new_contour[:-1, :]

# ----------------------------------------------------------------------------
def mask_contour(img, contour, scale=1.0):
    """
    -> np.array
    
    retorna una imagen binaria con la máscara del contorno ingresado.
    es posible controlar el tamaño de la máscara mediante el parámetro scale.
    
    :param np.array img:
        imagen que define el tamaño de la imagen binaria a generar.
    :param np.array contour:
        arreglo numérico de la forma (npoints, 2) con los pares de puntos
        (x, y) que describen el contorno de la máscara a generar.
    :param float scale:
        parámetro que permite controlar la escala de la máscara.
        
    :returns:
        imagen binaria con la máscara del contorno ingresado.
    """
    # ---
    # procesar contorno
    if (len(contour.shape) != 2) or (contour.shape[1] != 2):
        raise ValueError('contour must be a (npoints, 2) array')
        
    # extraer coordenadas del contorno
    x = contour[:, 0].flatten()
    y = contour[:, 1].flatten()
    
    # obtener centroide
    x_center = np.mean(x)
    y_center = np.mean(y)
    
    # escalar contorno
    x = x_center + (x - x_center)*scale
    y = y_center + (y - y_center)*scale
    
    # refinar contorno
    contour = np.vstack( [x, y] ).T
    contour = refine_contour(contour)
    
    # ---
    # inicializar mask matrix
    height, width, _ = img.shape
    x = np.clip(contour[:, 0].flatten(), 0.0, width - 1)
    y = np.clip(contour[:, 1].flatten(), 0.0, height - 1)
    
    mask = np.zeros( (height, width, 1), dtype=np.uint8 )
    
    # por cada punto (x, y) del contorno
    for i in range( x.size ):
        # obtener posición en mask
        idx_x = int( x[i] )
        idx_y = int( y[i] )
        
        # agregar a la mask
        mask[idx_y, idx_x] = 1
        
    # fill mask
    for i in range( mask.shape[0] ):
        _pos = np.where(mask[i, :] == 1)[0]
        if _pos.size == 0:
            continue
        
        mask[i, _pos[0]:_pos[-1]] = 1
        
    return 255*mask
