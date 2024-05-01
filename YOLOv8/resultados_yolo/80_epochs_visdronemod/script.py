from PIL import Image
from matplotlib import pyplot as plt
from pathlib import Path
import ultralytics
import sys
from ultralytics import YOLO, checks, hub

# Asegúrate de que las bibliotecas de Ultralytics estén instaladas
#try:
#    import ultralytics
#except ImportError:
#    sys.exit("Por favor, instala las bibliotecas de Ultralytics con: pip install 'git+https://github.com/ultralytics/ultralytics'")

# Ruta a la imagen de prueba
image_path = "test_image.jpg"

# Cargar la imagen
image = Image.open(image_path)

# Cargar el modelo YOLOv5 pre-entrenado (puedes especificar la versión y el tamaño)
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model = YOLO('modelo.pt')

# Realizar la inferencia en la imagen
results = model(image)

# Mostrar la imagen con las detecciones
results.show()

# Guardar las detecciones en una nueva imagen
results.save("detections.jpg")

# También puedes obtener las coordenadas de los cuadros delimitadores y las etiquetas de las clases
boxes = results.xyxy[0].numpy()[:, :4]  # Coordenadas de los cuadros delimitadores
labels = results.names[results.xyxy[0].numpy()[:, 5].astype(int)]  # Etiquetas de las clases

# Mostrar las coordenadas de los cuadros delimitadores y las etiquetas
for box, label in zip(boxes, labels):
    print("Etiqueta:", label, "Coordenadas del cuadro delimitador:", box)
