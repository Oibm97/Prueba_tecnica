"""
Created on Tue Nov 2 11:11:00 2021

@author: oibm

Test de pruebas unitarias para el archivo <<manipulaciónImagen.py>>
"""
import unittest
import manipulacion_imagen as mi
from PIL import Image

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class test_manipulacion_imagen(unittest.TestCase):
    """
    Descripción:
    Clase que modela las pruebas unitarias.
    """

    def test_encontrar_tamano_vertical_mayor(self):
        """
        Descripción:
        Función para verificar el resultado cuanto ingresa una imagen vertical
        y con un tamaño mayor al de una hoja A4.
        """

        orientacion = "Vertical"
        hojaa4 = (796,1123)
        ancho = 796
        alto = 1124

        tamano = mi.encontrar_tamano(orientacion, hojaa4, ancho, alto)
        self.assertEqual(tamano, (795,1123))


    def test_encontrar_tamano_cuadrado_mayor(self):
        """
        Descripción:
        Función para verificar el resultado cuanto ingresa una imagen cuadrada
        y con un tamaño mayor al de una hoja A4.
        """

        orientacion = "Horizontal"
        hojaa4 = (1123,796)
        ancho = 2000
        alto = 2000

        tamano = mi.encontrar_tamano(orientacion, hojaa4, ancho, alto)
        self.assertEqual(tamano, (796,796))


    def test_encontrar_tamano_horizontal_mayor(self):
        """
        Descripción:
        Función para verificar el resultado cuanto ingresa una imagen horizontal
        y con un tamaño mayor al de una hoja A4.
        """

        orientacion = "Horizontal"
        hojaa4 = (1123,796)
        ancho = 1200
        alto = 1000

        tamano = mi.encontrar_tamano(orientacion, hojaa4, ancho, alto)
        self.assertEqual(tamano, (955,796))


    def test_procesar_imagen_horizontal(self):
        """
        Descripción:
        Función para verificar el tamaño de la imagen resultante cuanto ingresa
        una imagen horizontal y con un tamaño mayor al de una hoja A4.
        """

        imagen = Image.open("ImagenTestHorizontal.jpg")
        nuevaimagen = mi.procesar_imagen(imagen)

        ancho = nuevaimagen.width
        alto = nuevaimagen.height
        tamano = (ancho,alto)
        self.assertEqual(tamano, (1123,750))

    def test_procesar_imagen_vertical(self):
        """
        Descripción:
        Función para verificar el tamaño de la imagen resultante cuanto ingresa
        una imagen vertical y con un tamaño mayor al de una hoja A4.
        """

        imagen = Image.open("ImagenTestVertical.jpg")
        nuevaimagen = mi.procesar_imagen(imagen)

        ancho = nuevaimagen.width
        alto = nuevaimagen.height
        tamano = (ancho,alto)
        self.assertEqual(tamano, (796,1085))
