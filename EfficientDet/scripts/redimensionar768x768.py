# Este script redimensiona una imagen a 320x320 y modifica su fichero de anotaciones asociado

import os
import xml.etree.ElementTree as ET
from PIL import Image

def resize_image(input_path, min_dimension=768, max_dimension=768, pad_to_max_dimension=False):
    # Abrir la imagen
    image = Image.open(input_path)
    
    # Obtener las dimensiones originales
    width, height = image.size
    
    # Calcular el factor de escala para mantener la proporción entre la altura y anchura original
    scale_factor = min(max_dimension / max(width, height), min_dimension / min(width, height))
    
    # Calcular las nuevas dimensiones
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Redimensionar la imagen
    resized_image = image.resize((new_width, new_height), Image.BILINEAR)
    
    # Si se debe rellenar con blanco hasta la dimensión máxima
    if pad_to_max_dimension:
        # Crear una nueva imagen con el tamaño máximo
        padded_image = Image.new("RGB", (max_dimension, max_dimension), color=(255, 255, 255))
        
        # Calcular la posición de la imagen redimensionada en la imagen acolchada
        left = (max_dimension - new_width) // 2
        top = (max_dimension - new_height) // 2
        right = left + new_width
        bottom = top + new_height
        
        # Pegar la imagen redimensionada en la imagen acolchada
        padded_image.paste(resized_image, (left, top, right, bottom))
        
        # Utilizar la imagen acolchada como la imagen redimensionada
        resized_image = padded_image
    
    # Guardar la imagen redimensionada
    resized_image.save(input_path)

     # Actualizar el archivo XML con las nuevas dimensiones
    update_xml_annotation(input_path, new_width, new_height, width, height)

def update_xml_annotation(image_path, new_width, new_height, old_width, old_height):
    # Construir el nombre del archivo XML correspondiente
    xml_path = os.path.splitext(image_path)[0] + ".xml"
    
    # Verificar si el archivo XML existe
    if os.path.exists(xml_path):
        # Parsear el archivo XML
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Actualizar las etiquetas de ancho y alto
        size = root.find('size')
        w = size.find('width') 
        w.text = str(new_width)
        h = size.find('height') 
        h.text = str(new_height)
        
        # Obtener el factor de escala para ajustar las coordenadas
        width_scale = new_width / old_width
        height_scale = new_height / old_height
        
        # Actualizar las coordenadas de los objetos
        for obj in root.findall('object'):
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            
            # Ajustar las coordenadas proporcionales al nuevo tamaño de la imagen
            xmin = int(xmin * width_scale)
            ymin = int(ymin * height_scale)
            xmax = int(xmax * width_scale)
            ymax = int(ymax * height_scale)
            
            # Actualizar las coordenadas en el XML
            bbox.find('xmin').text = str(xmin)
            bbox.find('ymin').text = str(ymin)
            bbox.find('xmax').text = str(xmax)
            bbox.find('ymax').text = str(ymax)
        
        # Guardar los cambios en el archivo XML
        tree.write(xml_path)

def resize_images_in_folder(folder_path):
    # Obtener la lista de archivos en la carpeta
    file_list = os.listdir(folder_path)
    
    # Iterar sobre los archivos en la carpeta
    for file_name in file_list:
        # Verificar si el archivo es una imagen .jpg o .jpeg
        if file_name.lower().endswith(('.jpg', '.jpeg')):
            # Construir la ruta completa del archivo de entrada
            input_path = os.path.join(folder_path, file_name)

            # Redimensionar la imagen
            resize_image(input_path, pad_to_max_dimension=True)

def main():
    for folder in ['train','valid', 'test']:
        folder_path = os.path.join(os.getcwd(), ('images/' + folder))
        resize_images_in_folder(folder_path)
    print('Successfully done.')

main()
