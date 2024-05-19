# Script para ejecutar un modelo TFLite personalizado en imágenes de prueba para detectar objetos

# Importar paquetes
import cv2
import numpy as np
from tensorflow.lite.python.interpreter import Interpreter
from google.colab.patches import cv2_imshow

# Definir función para realizar inferencias con el modelo TFLite y mostrar los resultados
def tflite_detect_video(modelpath, videopath, min_conf):

    # Cargar el modelo TensorFlow Lite
    interpreter = Interpreter(model_path=modelpath)
    interpreter.allocate_tensors()

    # Obtener detalles del modelo
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    # Abrir el archivo de video
    video = cv2.VideoCapture(videopath)
    imW = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    imH = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    while(video.isOpened()):

        # Adquirir frame y redimensionar a la forma esperada [1xHxWx3]
        ret, frame = video.read()
        if not ret:
            print('¡Se alcanzó el final del video!')
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalizar valores de píxeles si se usa un modelo flotante (es decir, si el modelo no está cuantizado)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Realizar la detección ejecutando el modelo con la imagen como entrada
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Recuperar resultados de detección
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Coordenadas de las cajas delimitadoras de los objetos detectados
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confianza de los objetos detectados

        # Bucle sobre todas las detecciones y dibujar la caja de detección si la confianza está por encima del umbral mínimo
        for i in range(len(scores)):
            if ((scores[i] > min_conf) and (scores[i] <= 1.0)):

                # Obtener coordenadas de la caja delimitadora y dibujar la caja
                # El intérprete puede devolver coordenadas que están fuera de las dimensiones de la imagen, se necesita forzarlas a estar dentro de la imagen usando max() y min()
                ymin = int(max(1, (boxes[i][0] * imH)))
                xmin = int(max(1, (boxes[i][1] * imW)))
                ymax = int(min(imH, (boxes[i][2] * imH)))
                xmax = int(min(imW, (boxes[i][3] * imW)))

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 4)

        # Imprimir el número de objetos detectados (Aforo)
        print('Aforo: ' + str(len(scores)))

        # Todos los resultados se han dibujado en el frame, así que es hora de mostrarlo.
        cv2_imshow(frame)

        # Presionar 'q' para salir
        if cv2.waitKey(1) == ord('q'):
            break

    # Limpiar
    video.release()
    cv2.destroyAllWindows()

# Configurar variables para ejecutar el modelo del usuario
PATH_TO_MODEL = ''  # Ruta al archivo .tflite del modelo
PATH_TO_VIDEO = ''  # Ruta al archivo de video
MIN_CONF = 0.2  # Confianza mínima para considerar una detección como válida

# Ejecutar la función de inferencia!
tflite_detect_video(PATH_TO_MODEL, PATH_TO_VIDEO, MIN_CONF)