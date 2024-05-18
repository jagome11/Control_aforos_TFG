import webbrowser
import tkinter as tk
from tkinter import *
from tkinter import ttk
import paramiko
from PIL import Image, ImageTk
import os

ip = "bujaruelo.dacya.ucm.es"
port = 22
username = "tfg_2324"
password = "rLj%23_?"
#Esta información hay que editarla en función de la conexión que se vaya a realizar

#scripts de prueba
ruta_script_yolo = "/home/tfg_2324/hola.py" #script ara ejecutar la infrencia en yolo
ruta_script_SSDM = "/home/tfg_2324/hola2.py" #script ara ejecutar la infrencia en SSD-MobileNet
ruta_script_Effi = "/home/tfg_2324/hola3.py" #script ara ejecutar la infrencia en EfficentDet
ruta_imagen_remota = "/home/tfg_2324/sentados.jpg" #imagen a probar
ruta_imagen_local_yolo = "salida1.png" 
ruta_imagen_local_SSDM = "salida2.png"
ruta_imagen_local_Effi = "salida3.png"

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
        stdin, stdout, stderr = cliente_ssh.exec_command(f"python3 {ruta_script}")
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
