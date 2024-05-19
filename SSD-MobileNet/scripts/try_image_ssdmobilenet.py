# Script para ejecutar un modelo TFLite personalizado en imágenes de prueba para detectar objetos

# Importar paquetes
import cv2
import numpy as np
import glob
import random
from tensorflow.lite.python.interpreter import Interpreter
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# Definir función para realizar inferencias con el modelo TFLite y mostrar los resultados
def tflite_detect_images(modelpath, folderpath, min_conf, num_test_images):
    # Obtener nombres de archivo de todas las imágenes en la carpeta de prueba
    images = glob.glob(folderpath + '/*.jpg') + glob.glob(folderpath + '/*.JPG') + glob.glob(folderpath + '/*.png') + glob.glob(folderpath + '/*.bmp')

    # Cargar el modelo TensorFlow Lite 
    interpreter = Interpreter(model_path=modelpath)
    interpreter.allocate_tensors()

    # Obtener detalles del modelo
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    float_input = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    # Seleccionar aleatoriamente imágenes de prueba
    images_to_test = random.sample(images, num_test_images)

    # Bucle sobre cada imagen y realizar detección
    for image_path in images_to_test:
        # Cargar la imagen y redimensionar a la forma esperada [1xHxWx3]
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        imH, imW, _ = image.shape
        image_resized = cv2.resize(image_rgb, (width, height))
        input_data = np.expand_dims(image_resized, axis=0)

        # Normalizar valores de píxeles si se usa un modelo flotante (es decir, si el modelo no está cuantizado)
        if float_input:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Realizar la detección ejecutando el modelo con la imagen como entrada
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Recuperar resultados de detección
        boxes = interpreter.get_tensor(output_details[1]['index'])[0]  # Coordenadas de las cajas delimitadoras de los objetos detectados
        scores = interpreter.get_tensor(output_details[0]['index'])[0]  # Confianza de los objetos detectados

        # Bucle sobre todas las detecciones y dibujar la caja de detección si la confianza está por encima del umbral mínimo
        for i in range(len(scores)):
            if ((scores[i] > min_conf) and (scores[i] <= 1.0)):
                # Obtener coordenadas de la caja delimitadora y dibujar la caja
                ymin = int(max(1, (boxes[i][0] * imH)))
                xmin = int(max(1, (boxes[i][1] * imW)))
                ymax = int(min(imH, (boxes[i][2] * imH)))
                xmax = int(min(imW, (boxes[i][3] * imW)))

                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

        # Imprimir el número de objetos detectados (Aforo)
        print('Aforo: ' + str(len(scores)))

        # Mostrar resultados
        plt.figure(figsize=(12, 16))
        plt.imshow(image)
        plt.show()

# Configurar variables para ejecutar el modelo del usuario
PATH_TO_MODEL = ''  # Ruta al archivo .tflite del modelo
PATH_TO_IMAGES = ''  # Ruta a la carpeta de imágenes de prueba
MIN_CONF = 0.2  # Confianza mínima para considerar una detección como válida
NUM_TEST_IMAGES = 1  # Número de imágenes de prueba a utilizar

# Ejecutar la función de inferencia!
tflite_detect_images(PATH_TO_MODEL, PATH_TO_IMAGES, MIN_CONF, NUM_TEST_IMAGES)