#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 17:50:26 2021

@author: oibm
"""
import manipulacionImagen as mi
from manipulacionImagen import AppImagenes
from PIL import Image

Lista_Fotos = AppImagenes["Lista_Fotos"]
Lista_Fotos_Modificadas = AppImagenes["Lista_Fotos_Modificadas"]

def ejecutar_cargar_imagen(ubicacion:str)->None:
    """
    Descripción:
    Ejecuta la función que carga la imagen solicitada en una Colección determinada.
    Parametros:
    -ubicacion(str): Nombre de la Colección donde se encuentra la información de la imagen a guardar. 
    Errores:
    -El nombre tiene que incluir la extención adecuada.
    -El nombre debe corresponder con el de una imagene en la carpeta <<Imagenes>>
    -El numero de imágenes a agregar debe corresponder con una entrada tipo <<int>>
    """
    cantidad_imagenes = int(input("\nCuántas imágenes desea agregar? (0 para cancelar): "))
    
    if cantidad_imagenes != 0:
        try:
            while cantidad_imagenes > 0:

                nombre_imagen = input("\nIngrese el nombre de la imagen con la extención JPG: ")
                try:
                    Image.open("Imagenes/"+nombre_imagen)
                    mi.cargar_imagen(nombre_imagen,ubicacion)
                    print("\nLa imagen fue cargada correctamente.")
                    cantidad_imagenes -= 1

                except:
                    print("\nIngrese un nombre válido.")
        except:
            print("\nIngrese un numero válido")

def ejecutar_mostrar_basedatos(ubicacion:str)->None:
    """  
    Descripción:
    Ejecuta la función para mostrar el listado de objetos de una Colección determinada dentro de la base de datos. 
    Parámetros:
    -ubicacion(str): Nombre de la Colección donde se encuentra la información de la imagenes para ser mostradas en una lista. 
    """
    mi.mostrar_basedatos(ubicacion)

def ejecutar_seleccionar_imagen(imagen_seleccionada:int, ubicacion:str)->Image:
    """
    Descripción:
    Ejecuta la función que retorna la imagen que desea ser mostrada en pantalla. 
    Parámetros:
    -imagen_seleccionada(int): Indice de la imagen que desea ser abierta en una Colección determinada.
    -ubicacion(str): Nombre de la Colección donde se encuentra la información de la imagen a mostrar. 
    Salidas:
    -imagen(Image): Imagen que desea ser abierta.
    """
    imagen = mi.seleccionar_imagen(imagen_seleccionada,ubicacion)
    return imagen

def ejecutar_mostrar_imagen(ubicacion:str)->None:
    """
    Descripción:
    Ejecuta la función que muestra la imagen que entra por parámetro
    Parametros:
    -imagen(Image): Imagen cargada
    Errores:
    -Debe existir al menos una imagen en la carpetas <<Imagenes>> y/o <<Imagenes_modificadas>>.
    -El numero de la imagen a mostrar debe corresponder al de alguna imagen en la base de datos. 
    """
    indice, objetolista, directorio = mi.info_listas(ubicacion)
    indice = objetolista.estimated_document_count()

    if indice > 0:
        ejecutar_mostrar_basedatos(ubicacion)
        completado = False
        while completado == False:
            try:
                imagen_seleccionada = int(input("\nSeleccione la imagen a mostrar (0 para candelar): "))
                if imagen_seleccionada == 0:
                    break
                else:
                    imagen = ejecutar_seleccionar_imagen(imagen_seleccionada,ubicacion)
                    mi.mostrar_imagen(imagen)
                    completado = True 
            except:
                print("\nIngrese un numero válido.")
    else:
        if ubicacion == "Lista_Fotos":
            print("\nCargue una imagen para poder realizar esta acción.")
        elif ubicacion == "Lista_Fotos_Modificadas":
            print("\nProcese una imagen y guardela para poder realizar esta acción.")
    
def ejecutar_procesar_imagen()->None:
    """
    Descripción:
    Ejecuta la función que procesa la imagen que entra por parámetro.
    Parametros:
    -imagen(Image): Imagen cargada
    Salidas:
    -imagen(Image): Imagen que desea ser abierta.
    Errores:
    -Debe existir al menos una imagen cargada en la base de datos.
    -El numero de la imagen a procesar debe corresponder al de alguna imagen en la base de datos.
    -El nombre de la imagen a guardar (de ser el caso) debe tener la extensión adecuada.
    """
    indice = Lista_Fotos.estimated_document_count()
    if indice > 0:
        mi.mostrar_basedatos("Lista_Fotos")
        completado = False
        while completado == False:
            try:
                imagen_seleccionada = int(input("\nSeleccionar la imagen a procesar (0 para cancelar): "))
                if imagen_seleccionada == 0:
                    break
                else:
                    imagen = ejecutar_seleccionar_imagen(imagen_seleccionada,"Lista_Fotos")
                    imagen = mi.procesar_imagen(imagen)
                    print("\n1. Si")
                    print("2. No")
                    guardar = input("\nDesea guardar la imagen?: ")
                    if guardar == "1":
                        nombrevalido = False
                        while nombrevalido == False:
                            try:
                                nombre_imagen = input("\nNombre de la imagen con la extensión (JPG): ")
                                mi.guardar_imagen(imagen, nombre_imagen, "Lista_Fotos_Modificadas")
                                nombrevalido = True
                                print("\nLa imagen fue cargada correctamente.")
                            except:
                                print("\nIngrese un nombre válido.")
                    completado = True
            except:
                print("\nIngrese un numero válido.")
    else:
        print("\nCargue una imagen para poder realizar esta acción.")
    
def ejecutar_eliminar_imagen()->None:
    """
    Descripción:
    Ejecuta la función que elimina la imagen de la base de datos y de la carpeta donde se encuentra guardada. 
    Parámetros:
    -imagen_seleccionada(int): Valor entero con el índice de la imagen que el usuario desea eliminar de una Colección determinada.
    -ubicacion(str): Nombre de la Colección donde se encuentra la información de la imagen a guardar. 
    Errores:
    -El numero de las carpetas para eliminar la imagen debe corresponder al de la lista dada.
    -Debe existir al menos una imagene en la carpeta elegida para poder ser eliminada. 
    -El numero de la imagen a eliminar debe corresponder al de alguna imagen en la base de datos. 
    """
    numerovalido = False
    while numerovalido == False:
        try:    
            print("\n1. Lista_Fotos")
            print("2. Lista_Fotos_Modificadas")
            ubicacion = input("\nEscoja la ubicación (0 para cancelar): ")
            if ubicacion == "0":
                break
            elif ubicacion == "1":
                ubicacion = "Lista_Fotos"
            elif ubicacion == "2":
                ubicacion = "Lista_Fotos_Modificadas"

            indice, objetolista, directorio = mi.info_listas(ubicacion)
            
            if indice > 0:
                ejecutar_mostrar_basedatos(ubicacion)
                eliminado = False
                while eliminado == False:
                    try:
                        imagen_seleccionada = int(input("\nSeleccionar la imagen a eliminar (0 para cancelar): "))
                        if imagen_seleccionada == 0:
                            break
                        else:
                            mi.eliminar_imagen(imagen_seleccionada, ubicacion)
                            print("\nLa imagen fue eliminada correctamente.")
                            eliminado = True
                    except:
                        print("\nIngrese un numero válido.")
            else:
                print("\nCargue y/o procese una imagen para poder realizar esta acción.")
            numerovalido = True
        except:
            print("\nIngrese un numero válido")


def menu()->None:
    """
    Descripción:
    Función que determina el menú a mostrar en la consola.
    CRUD (Create, Read, Update, Delete)
    """
    print("\nOPCIONES\n")
    print("0. Cargar Imagen")
    print("1. Mostrar Imagen")
    print("2. Procesar Imagen")
    print("3. Mostrar Imagen Procesada")
    print("4. Eliminar Imagen")
    print("5. Salir\n")

def iniciar_aplicacion()->None:
    """
    Descripción:
    Función para iniciar la aplicación.
    Ejecuta el menú y solicita un numero para llevar a cabo una acción determinada. 
    """
    continuar = True
    while continuar:
        menu()
        elegido = input("\nSeleccione una opcion del menu: ")

        if elegido == "0":
            ejecutar_cargar_imagen("Lista_Fotos")
    
        elif elegido == "1":
            ejecutar_mostrar_imagen("Lista_Fotos")
                
        elif elegido == "2":
            ejecutar_procesar_imagen()
        
        elif elegido == "3":
            ejecutar_mostrar_imagen("Lista_Fotos_Modificadas")
                        
        elif elegido == "4":
            ejecutar_eliminar_imagen()

        elif elegido == "5":
            continuar = False
        
        else:
            print("Seleccione una opción del menú:")
            
iniciar_aplicacion()
