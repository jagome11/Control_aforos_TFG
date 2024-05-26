import webbrowser
import tkinter as tk
from tkinter import *
from tkinter import ttk
import paramiko
from PIL import Image, ImageTk
import os

ip = "pc-fran.dacya.ucm.es"
port = 16994
username = "sergio"
password = "Raspi2023!"

ruta_script_yolo = "/home/sergio/tutorial-env/yolov8_test_img.py"
ruta_script_SSDM = "/home/sergio/tutorial-env/yolov8_test_img.py"
ruta_script_Effi = ""
ruta_imagen_remota = "/home/sergio/tutorial-env/test_image2.jpg"
ruta_imagen_local_yolo = "salida1.png"


ruta_imagen_local_SSDM = "salida2.png"
ruta_imagen_local_Effi = "salida3.png"
ruta_entorno_virtual = "/home/sergio/tutorial-env/bin/activate"

def ssh_connect():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=password)
        print("Conexion establecida con usuario", username)
        return client
    except Exception as e:
        print("Error al conectar:", str(e))
        return None

def ejecutar_script_remoto(cliente_ssh, ruta_script, ruta_imagen_local, text_widget):
    try:
        comando = f"source {ruta_entorno_virtual} && python3 {ruta_script}"
        stdin, stdout, stderr = cliente_ssh.exec_command(comando)
        salida = stdout.read().decode()
        errores = stderr.read().decode()
        if errores:
            print("Errores al ejecutar el script:", errores)
        else:
            text_widget.insert(END, salida)
            sftp = cliente_ssh.open_sftp()
            sftp.get(ruta_imagen_remota, ruta_imagen_local)
            sftp.close()
            imagen = Image.open(ruta_imagen_local)
            imagen = imagen.resize((300, 300))  # Redimensionar la imagen
            imagen_tk = ImageTk.PhotoImage(imagen)
            label_imagen.config(image=imagen_tk)
            label_imagen.image = imagen_tk
            text_widget.delete('1.0', END)
            text_widget.insert(END, f"Aforo: {salida}")
    except Exception as e:
        print(f"Error al ejecutar el script {ruta_script}:", str(e))

def abrir_pagina_web():
    webbrowser.open("www.google.com")

root = Tk()
root.title("GUI Aforos")
root.geometry("600x550")

label_imagen = Label(root)
label_imagen.pack()

text_widget = Text(root)
text_widget.pack(pady=10, fill=BOTH, expand=True)


Acciones = ttk.Combobox(state="readonly")
Acciones['values'] = ['YOLOv8', 'SSD-MobileNet', 'EfficentDet']
Acciones.place(relx=0.075, rely=0.65, relwidth=0.2)

def AccionElegida(eventObject):
    cliente_ssh = ssh_connect()
    if cliente_ssh is None:
        text_widget.insert(END, "Error: No se pudo establecer la conexion SSH.\n")
        return
    if eventObject.widget.get() == 'YOLOv8':
        ejecutar_script_remoto(cliente_ssh, ruta_script_yolo, ruta_imagen_local_yolo, text_widget)
    elif eventObject.widget.get() == 'SSD-MobileNet':
        ejecutar_script_remoto(cliente_ssh, ruta_script_SSDM, ruta_imagen_local_SSDM, text_widget)
    elif eventObject.widget.get() == 'EfficentDet':
        ejecutar_script_remoto(cliente_ssh, ruta_script_Effi, ruta_imagen_local_Effi, text_widget)
    cliente_ssh.close()

Acciones.bind("<<ComboboxSelected>>", AccionElegida)
Acciones.current(0)

root.mainloop()
