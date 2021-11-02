#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 16:25:20 2021

@author: oibm
"""

from PIL import Image
from pymongo import MongoClient
import os

uri = "mongodb+srv://Oscar:1234@appimagenes.uvok1.mongodb.net/AppImagenes?retryWrites=true&w=majority"
cliente = MongoClient(uri)
AppImagenes = cliente["AppImagenes"]

def info_listas(ubicacion:str):
    """
    Descripción:
    Función que accede a determinados valores de las Colecciones creadas en la Base de datos.
    Parámetros:
    -ubicacion(str): Nombre de la carpeta que contiene las imágenes a usar <<Imagenes/>> o la carpeta donde se almacenarán 
    las imágenes modificadas <<Imagenes_modificadas>>. Representan cada una las Colecciones usadas en la Base de Datos.
    Salidas:
    -indice(int): Valor entero con la cantidad actual de documentos dentro de una Colección determinada.
    -objetoLista(collection): Colección asociada a la ubicación dada por parámetro.
    -directorio(str): Nombre de la dirección donde se ubican las fotos. 
    """
    if ubicacion == "Lista_Fotos":
        objetoLista = AppImagenes["Lista_Fotos"]
        directorio = "Imagenes/"

    if ubicacion == "Lista_Fotos_Modificadas":
        objetoLista = AppImagenes["Lista_Fotos_Modificadas"]
        directorio = "Imagenes_modificadas/"

    indice = objetoLista.estimated_document_count()

    return indice, objetoLista, directorio

def cargar_imagen(nombre_imagen:str, ubicacion:str)->None:
    """ 
    Descripción:
    Función que accede a la base de datos en la nube en mongodb para insertar la información de una nueva imagen en una determinada Colección. 
    Parámetros:
    -nombre_imagen(str): Nombre de la foto
    -ubicacion(str): Nombre de la carpeta que contiene las imágenes a usar <<Imagenes/>> o la carpeta donde se almacenarán 
    las imágenes modificadas <<Imagenes_modificadas>>. Representan cada una las Colecciones usadas en la Base de Datos.
    Salidas:
    NA
    Errores:
    NA
    """ 
    
    indice, objetoLista, directorio = info_listas(ubicacion)
    datosFoto = {"id":indice+1, "Nombre imagen":nombre_imagen}
    objetoLista.insert_one(datosFoto)

def mostrar_basedatos(ubicacion:str):
    """
    Descripción:
    Función que despliega la lista de fotos guardadas en una determinada Colección de la base de datos de Mongodb.
    Parámetros:
    -ubicacion(str): Nombre de la carpeta que contiene las imágenes a usar <<Imagenes/>> o la carpeta donde se almacenarán 
    las imágenes modificadas <<Imagenes_modificadas>>. Representan cada una las Colecciones usadas en la Base de Datos.
    Salidas:
    NA
    Errores:
    Na
    """    
    indice, objetoLista, directorio = info_listas(ubicacion)
    print("")
    for i in objetoLista.find():
        print(i["id"]," ",i["Nombre imagen"])
    

def seleccionar_imagen(imagen_seleccionada:int, ubicacion:str)->Image:
    """
    Descripción:
    Función que retorna la imagen que desea ser mostrada en pantalla. 
    Parametros:
    -imagen_seleccionada(int): Indice de la imagen que desea ser abierta en una Colección determinada.
    -ubicacion(str): Nombre de la Colección donde se encuentra la información de la imagen a mostrar. 
    Salidas:
    -imagen(Image): Imagen que desea ser abierta.
    Errores:
    NA
    """
    indice, objetoLista, directorio = info_listas(ubicacion)

    imagen = objetoLista.find_one({"id":imagen_seleccionada})
    nombre_imagen = directorio + imagen["Nombre imagen"]
    imagen = Image.open(nombre_imagen)

    return imagen

def mostrar_imagen(imagen:Image)->None:
    """
    Descripción:
    Función que muestra la imagen que entra por parámetro con un visualizador externo.
    Parametros:
    -imagen(Image): Imagen cargada previamente. 
    Salidas:
    NA
    Errores:
    NA
    """
    imagen.show()
    
def encontrar_tamano(orientacion:str, hojaA4:tuple, ancho:int, alto:int)-> tuple:
    """
    Descripción:
    Función que calcula las nuevas dimensiones de la imagen requeridos para entrar en una hoja tamaño A4. Las nuevas dimensiones son calculadas con un error
    de 0.5%
    Restricciones:
    -La imagen no puede perder su ratio.
    -Se debe aprovechar el máximo de la hoja A4.
    -Ninguna imagen debe ser agrandada en el proceso, solo encogida cuando corresponda.
    -La orientación de la página se debe definir a partir de la orientación de la imagen.
    Parametros:
    -orientación(str): Orientación de la imagen cargada.
    -hojaA4(tuple): Una tupla con el tamaño de la hoja A4 respecto a la orientación requerida. (Ancho, Alto)
    -ancho(int): Ancho de la imagen cargada.
    -alto(int): Alto de la imagen cargada.
    Salidas:
    -tamaño(tuple): Una tupla con el nuevo tamaño de la imagen con un error de 0.05%. 
    Errores:
    NA
    """
    
    ratio = round((max(ancho,alto)/min(ancho,alto)),4)
    error = 0.0005
    topeMax = ratio*(1+error)
    topeMin = ratio*(1-error)
    
    i = 1
    j = 1
    areaMinima = 1000000*1000000
    
    for i in range(1,hojaA4[0]+1):
        for j in range(1,hojaA4[1]+1):
            nuevoRatio = round((max(i,j)/min(i,j)),4)
            area = hojaA4[0]*hojaA4[1] - i*j
            if nuevoRatio <= topeMax and nuevoRatio >= topeMin:
                
                areaMinima = min(areaMinima,area)
                
                if orientacion == "Vertical":
                    ancho = min(i,j)
                    alto = max(i,j)
    
                if orientacion == "Horizontal":
                    ancho = max(i,j)
                    alto = min(i,j)
    
    tamaño = (ancho,alto)
    return tamaño        

def procesar_imagen(imagen:Image)->Image:
    """
    Descripción:
    Función que procesa la imagen que entra por parámetro con la función "encontrar_tamano".
    Parametros:
    -imagen(Image): Imagen cargada previamente. 
    Salidas:
    -nuevaImagen(Image): Imagen con las nuevas dimensiones de acuerdo a las restricciones del problema. 
    Errores:
    NA
    """
    
    ancho = imagen.width
    alto = imagen.height
    
    mensaje = "\nLa imagen no fue modificada.\n"
    
    tamaño = (ancho,alto)
    
    orientacion = None
    if alto > ancho:
        orientacion = "Vertical"
        hojaA4 = (796,1123)
        
    elif alto <= ancho:
        orientacion = "Horizontal"
        hojaA4 = (1123,796)
    
    if hojaA4[0] <= ancho or hojaA4[1] <= alto:
        tamaño = encontrar_tamano(orientacion, hojaA4, ancho, alto)
        mensaje = "\nLas nuevas dimensiones de la imagen son: \n\nAncho: " + str(tamaño[0]) + " pixeles" + "\nAlto: " + str(tamaño[1]) + " pixeles"
    
    nuevaImagen = imagen.resize(tamaño)
    
    nuevaImagen.show()
    
    print(mensaje)
    
    return nuevaImagen

def guardar_imagen(imagen:Image, nombre_imagen:str,ubicacion:str):
    """  
    Descripción:
    Función que guarda la imagen modificada en la carpeta para tal fin y que guarda su información en la base de datos en la Colección adecuada. 
    Parámetros:
    -imagen(Image): Imagen a guardar
    -nombre_imagen(str): Nombre que el usuario ingresa para guardar la imagen. 
    -ubicacion(str): Nombre de la Colección donde se encuentra la información de la imagen a guardar. 
    Salidas:
    NA
    Errores:
    NA
    """
    
    imagen.save("Imagenes_modificadas/"+nombre_imagen)
    cargar_imagen(nombre_imagen,ubicacion)

def eliminar_imagen(imagen_seleccionada:int, ubicacion:str)->None:
    """ 
    Descripción:
    Función que elimina la imagen de la base de datos y de la carpeta donde se encuentra guardada. 
    Parámetros:
    -imagen_seleccionada(int): Valor entero con el índice de la imagen que el usuario desea eliminar de una Colección determinada.
    -ubicacion(str): Nombre de la Colección donde se encuentra la información de la imagen a guardar. 
    Salidas:
    NA
    Errores:
    NA
    """    
    indice, objetoLista, directorio = info_listas(ubicacion)
    imagen = objetoLista.find_one({"id":imagen_seleccionada})

    for i in range(imagen_seleccionada+1, indice+1):
        objetoLista.update_one({"id":i},{"$inc":{"id":-1}})
    
    objetoLista.delete_one({"_id":imagen["_id"]})
    os.remove(directorio+imagen["Nombre imagen"])