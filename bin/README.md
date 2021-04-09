![banner](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/bin/banner.png)
Este repositorio contiene los talleres prácticos y el material complementario del curso ME4707 Robótica.

## Google Colab
Para la realización de los talleres prácticos de programación del curso, es conveniente que todos utilizemos la misma plataforma y así podamos evitar errores de compatibilidad o de instalación. [**Google Colaboratory**](https://colab.research.google.com/notebooks/welcome.ipynb) es un entorno de Jupyter notebook gratuito que se ejecuta completamente en la nube. La plataforma permite tanto escribir como ejecutar código, y solo se requiere de una cuenta google.

https://colab.research.google.com/notebooks/welcome.ipynb

Dentro de este repositorio podrá encontrar los notebooks (\*.ipynb) de los distintos workshops a realizar a lo largo del curso. Descárguelos y ábralos dentro de su propia sesión de Colab.

## Clonar GitHub
En caso de requerir importar archivos y/o elementos de este repositorio a un entorno de Google Colab, puede clonarlo directamente mediante:

`! git clone https://github.com/cherrerab/roboticafcfm.git`

Si el repositorio se ha clonado correctamente, notará que en la carpeta de archivos `/content` se habrá creado el directorio `roboticafcfm`. Para utilizar este directorio dentro de la sesión, utilice el siguiente comando:

`%cd /content/roboticafcfm`

## Tutorial Numpy
Numpy es quizás la librería más utilizada en lo que respecta a Python, se utiliza extensamente en la ciencia de datos y, más importante para el curso, en el procesamiento de imágenes. Fundamentalmente, está orientada a la manipulación de arreglos multidimensionales, para lo cual cuenta con estructuras de datos y operaciones especializadas. En este tutorial aprenderá las funcionalidades básicas de esta librería que le permitirán abordar los próximos workshops del curso.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cherrerab/roboticafcfm/blob/master/auxiliar_01/tutorial_01.ipynb)

## Color Segmentation
La segmentación, si bien bajo muchos aspectos consiste en una operación bastante simple, es un proceso bastante útil a la hora de desarrollar algoritmos de detección de objetos o tracking. En términos simples, segmentar una imagen consiste en seccionar o aislar zonas de una imagen en función de algún atributo, como por ejemplo, intensidad o color. En este tutorial aprenderá los primeros pasos en cuanto a procesamiento de imágenes, desde cargar las imágenes como arreglos numéricos, hasta manipular sus valores mediante filtros y segmentadores.


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cherrerab/roboticafcfm/blob/master/auxiliar_01/workshop_01.ipynb)

[![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_01/bin/auxvid.png)](https://youtu.be/CzYsunXRbhg)  [![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_01/bin/auxvid_2.png)](https://youtu.be/dP6y3Y88-Ao)

## Shape Detection
La Transformada de Hough es una técnica que permite detectar geometrías en una imagen, mientras esta pueda ser parametrizada matemáticamente. Mediante su matriz acumuladora de votos, logra detectar recta y círculos incluso si estos presentan ruido o irregularidades. En este worshop utilizaremos las implementaciones de la Transformada de Hough en OpenCV para trackear y orientar un cuaderno en una imagen.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cherrerab/roboticafcfm/blob/master/auxiliar_02/workshop_02.ipynb)

[![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_02/bin/auxvid_1.png)](https://youtu.be/cu0N7dTMcH0)  [![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_02/bin/auxvid_2.png)](https://youtu.be/lKKkzjR0a3U)


## Feature Detection
El Scale-Invariant Feature Transform (SIFT) es un algoritmo, desarrollado por D. Lowe en 2004, para la extracción de `features` de una imagen. En un sentido abstracto, las `features` de una imagen son patrones o regiones fácilmente detectables y trackeables, a partir de las cuales podemos identificar y reconocer toda de objetos presentes en la imagen. En este workshop utilizaremos la implementación de SIFT en OpenCV para identificar cartas Pokemon en una foto, a partir de una serie de cartas de referencia.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cherrerab/roboticafcfm/blob/master/auxiliar_03/workshop_03.ipynb)


[![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_03/bin/auxvid_1.png)](https://youtu.be/GTrKaC4fBAM) [![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_03/bin/auxvid_2.png)](https://youtu.be/021FEbXY7AY)

## Genetic Algorithms
Los algoritmos genéticos (GA) son una heurística de optimización, inspirada en la evolución biológica, donde los problemas pasan a ser modelados como la simulación de una población de individuos. Durante estas simulaciones, los indiviudos son sometidos a los principios fundamentales de la Teoría de Darwin como la heredabilidad genética, la recombinación genética aleatoria (mutaciones) y la supervivencia de los más aptos (selección natural). En este workshop implementaremos un algoritmo genético utilizando la librería especializada `pyevolve` para resolver un problema de maximización multivariable.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cherrerab/roboticafcfm/blob/master/auxiliar_04/workshop_04.ipynb)


[![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_04/bin/auxvid.png)](https://youtu.be/ag53l1XeMJA)


## Neuroevolving of Augmenting Topologies
Entre los algoritmos más comunes dentro del Machine Learning, se encuantran las ya bastante conocidas Rede Neuronales o Neural Networks (NN) que consisten en arquitecturas bioinspiradas en la forma en que nuestros cerebros procesan información mediante la transmisión paralela y secuencial de señales eléctricas, entre las neuronas. Así, las Redes Neuronales consisten en una red de nodos, generalmente ordenados por capas, que mediante una serie de ponderaciones y conexiones convierten una serie de valores de entrada (`input`) en una serie de valores de salida (`output`).

En este workshop nos concentraremos en el campo del aprendizaje no supervizado y en particular, en el Reinforcement Learning. En el Reinforcement Learning, las Redes Neuronales son entrenadas (ajustan sus parámetros) para resolver una tarea específica mediante prueba y error, de la misma manera en que uno entrena un animal con recompensas ante aciertos y castigos ante equivocaciones. Una implementación directa de esta idea es la Neuroevolución donde los algoritmos evolutivos son combinados con Redes Neuronales para evolucionar una arquitectura de Red Neuronal capaz de cumplir con la tarea objetivo.


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cherrerab/roboticafcfm/blob/master/auxiliar_05/workshop_05.ipynb)

[![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_05/bin/auxvid_1.png)](https://youtu.be/qForldaNGJ0)   [![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_05/bin/auxvid_2.png)](https://youtu.be/liMUMoEwFmU)

## Deep Learning
En el campo del Aprendizaje Supervizado, los modelos son entrenados para inferir y _aprender_ las _features_ y los patrones contenidos en una colección de datos para desempeñar alguna tarea de clasificación y/o regresión. En este caso, para entrenar los modelos es necesario contar con una serie de datos de entrada `X` con los resultados deseados de estos `Y`, también llamados datos de salida. Para familiarizarnos con la implementación de estos modelos, en este workshop estudiaremos un caso sencillo de clasificación inspirado en el Playground de TensorFlow.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cherrerab/roboticafcfm/blob/master/auxiliar_06/workshop_06.ipynb)

[![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_06/bin/auxvid.png)](https://youtu.be/bX70gwjEUNA)   [![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_06/bin/auxvid_2.png)](https://youtu.be/Y6UnM1NZRuk)

## Convolutional Neural Networks
Las Redes Neuronales Convolucionales (CNN) consisten en arquitecturas muy similares a las redes Dense o Fully Connected vistas en el workshop anterior, pues estás también se constituyen de de nodos con parámetros entrenables, como son los pesos y biases encargados de ponderar la información de entrada o input. No obstante, la estructura de las Redes Convolucionales está diseñada particularmente para interpretar imágenes y aprender, durante su entrenamiento, a extraer patrones y características espaciales (features) de estas mediante la aplicación secuencial de filtros.

Con la finalidad de introducir la implementación de este tipo de arquitecturas en Tensorflow, en este workshop estudiaremos un caso de regresión simple, en donde entrenaremos un modelo CNN para detectar la posición (𝑥,𝑧) de una esfera en un espacio tridimensional.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cherrerab/roboticafcfm/blob/master/auxiliar_07/workshop_07.ipynb)

[![Open In Youtube](https://raw.githubusercontent.com/cherrerab/roboticafcfm/master/auxiliar_07/auxvid.png)](https://youtu.be/245WwEOlMos) 
