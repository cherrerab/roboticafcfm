#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix

from scipy.stats import kurtosis
from scipy.stats import skew

from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------------------------------------------   
def plot_tour_img(coords, tour, img_file):
    """
    -> None
    
    this functiones generates a .png of the graph of the especified tour.
    
    :param np.array coords:
        arreglo numérico de la forma (ncities, 2) con las coordenadas (x, y)
        de cada una de las ciudades.
    :param list tour:
        arreglo de la forma (ncities, ) con el orden las ciudades que define
        el recorrido.
    :param str img_file:
        path de destino de la imagen .png
    """
    padding = 20
    x = coords[:, 0] + padding
    y = coords[:, 1] + padding

    xmax, ymax = np.max(x), np.max(y)
    
    img = Image.new("RGB", (int(xmax), int(ymax)), color=(255, 255, 255))
    font = ImageFont.load_default()
    d = ImageDraw.Draw(img);

    num_cities=len(tour)
    for i in range(num_cities):
        j = (i+1)%num_cities
        city_i = tour[i]
        city_j = tour[j]
        x1, y1 = coords[city_i, :]
        x2, y2 = coords[city_j, :]
        d.line((int(x1), int(y1), int(x2), int(y2)),fill=(0, 0, 0))
        d.text((int(x1)+7, int(y1)-5), str(i), font=font, fill=(32, 32, 32))

    for x,y in coords:
        x, y = int(x), int(y)
        d.ellipse((x-5, y-5, x+5, y+5), outline=(0, 0, 0), fill=(196, 196, 196))

    del d

    img.save(img_file, 'PNG')
    print('The plot was saved into the %s file.' % (img_file,))
    
# -----------------------------------------------------------------------------   
def plot_evolution(GA_STATS):
    """
    -> None
    
    Plotea la evolución del algoritmo genético durante las generaciones.
    
    :param DataFrame GA_STATS: DataFrame que contiene las estadísticas.
    
    :return: None
    """

    # plot
    plt.figure(figsize=(10,6))
    
    plt.plot(GA_STATS.index, GA_STATS['Max'], 'b', label='Max')
    plt.plot(GA_STATS.index, GA_STATS['Min'], 'r', label='Min')
    plt.plot(GA_STATS.index, GA_STATS['Mean'], 'k:', label='Mean')
      
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    
    plt.show()
    
    return None

# ----------------------------------------------------------------------------
def plot_confusion_matrix(Y_true, Y_pred, target_names,
                          title='Confusion matrix',
                          cmap=None, normalize=False,
                          figsize=(5,5)):
    
    """
    given the true (Y_true) and the predicted (Y_pred) labels,
    makes the confusion matrix.
    
    :param np.array Y_true:
        the true labels of the data. (no one hot encoding).
    :param np.array Y_pred:
        the predicted labels of the data by the model. (no one hot encoding).
    :param list target_names:
        given classification classes such as [0, 1, 2] the class names,
        for example: ['high', 'medium', 'low'].
    :param str title:
        the text to display at the top of the matrix.
    :param str cmap:
        the gradient of the values displayed from matplotlib.pyplot.cm
        see http://matplotlib.org/examples/color/colormaps_reference.html
        plt.get_cmap('jet') or plt.cm.Blues.
    :param bool normalize:
        if False, plot the raw numbers, if True, plot the proportions.
        
    :reference:
        http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
        
    """
    import itertools
    
    cm = confusion_matrix(Y_true, Y_pred)
    
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy
    
    if cmap is None:
        cmap = plt.get_cmap('Blues')
    
    plt.figure(figsize=figsize)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    
    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)
    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    
    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                      verticalalignment="center",
                      horizontalalignment="center",
                      color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                      verticalalignment="center",
                      horizontalalignment="center",
                      color="white" if cm[i, j] > thresh else "black")
    
    
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()
    
# ----------------------------------------------------------------------------
def plot_loss_function(train_info, figsize=(5,5)):
    """
    -> None
    
    this function plots de evolution of the loss function of the model 
    during the training epochs.
    
    :param train_info:
        training history of the classification model.
        
    """
    # crear figura
    plt.figure(figsize=figsize)
    
    plt.plot(train_info.history['loss'])
    plt.plot(train_info.history['val_loss'])
    
    # caracteristicas del plot
    plt.title('Model loss')
    plt.ylabel('Loss'); plt.xlabel('Epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()
 
# ----------------------------------------------------------------------------
def plot_classification_map(model, xlim, ylim, res):
  """
  This function plots de classification map on the specified 2D region.
  """
  # initialize 2D region
  x = np.linspace(xlim[0], xlim[1], res)
  y = np.linspace(ylim[0], ylim[1], res)
  
  x, y = np.meshgrid(x, y)
  
  X = np.zeros( (x.size, 2) )
  
  X[:, 0] = x.flatten()
  X[:, 1] = y.flatten()

  # generate the classification map
  Y = model.predict(X)
  Y_map = np.reshape( Y[:,1], (res, res))

  plt.figure(figsize=(7,7))
  plt.imshow(Y_map, cmap='bwr')
  return

# ----------------------------------------------------------------------------
def plot_img_samples(dataset, index, grid=None,
                     figsize=(5,5), title=''):
    """
    -> None
    
    this function concatenates and plot the index samples of the dataset, 
    following the rows and columns of the grid parameter.
    
    :param np.array dataset:
        dataset containing the image samples.
        it is assumed a (samples, height, width) shape.
    :param array-like index:
        list of the samples indexes to plot.
    :param tuple grid:
        (rows, cols) of images to follow in the concatenation.
        if None, it is assumed only a row of images.
        
    :returns:
        None.
    """
    
    index = np.array( index )
    
    rows, cols = grid
    _, h, w = dataset.shape
    
    # verificar que la cantidad de imagenes coincide con el grid
    assert index.size >= rows*cols
    
    # concatenar imágenes
    img = np.zeros( (rows*h, cols*w) )
    
    for i, idx in enumerate(index):
        
        # extraer imagen del dataset
        image = dataset[idx, :, :]
        image = np.reshape( image, (h, w) )
        
        vmin, vmax = np.min(image, axis=None), np.max(image, axis=None)
        
        if (vmax - vmin)!=0.0:
            image = (image - vmin)/(vmax - vmin)
        else:
            image = np.zeros_like(image)
        
        # agregar imagen a img
        k, j = i%cols, i//cols
        img[j*h:(j+1)*h, k*w:(k+1)*w] = image
        
    # plotear
    plt.figure(figsize=figsize)
    plt.imshow(img, cmap='jet')
    plt.title(title)