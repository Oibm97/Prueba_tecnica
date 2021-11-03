#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 2 11:11:00 2021

@author: oibm
"""

import manipulacionImagen as mi
import unittest
from PIL import Image

class testManipulacionImagen(unittest.TestCase):

    def test_encontrar_tamano_vertical_mayor(self):

        orientacion = "Vertical"
        hojaA4 = (796,1123)
        ancho = 796
        alto = 1124

        tamano = mi.encontrar_tamano(orientacion, hojaA4, ancho, alto)
        self.assertEqual(tamano, (795,1123))


    def test_encontrar_tamano_cuadrado_mayor(self):
        orientacion = "Horizontal"
        hojaA4 = (1123,796)
        ancho = 2000
        alto = 2000

        tamano = mi.encontrar_tamano(orientacion, hojaA4, ancho, alto)
        self.assertEqual(tamano, (796,796))     


    def test_encontrar_tamano_horizontal_mayor(self):

        orientacion = "Horizontal"
        hojaA4 = (1123,796)
        ancho = 1200
        alto = 1000

        tamano = mi.encontrar_tamano(orientacion, hojaA4, ancho, alto)
        self.assertEqual(tamano, (955,796))   

    
    def test_procesar_imagen_horizontal(self):

        imagen = Image.open("ImagenTestHorizontal.jpg")
        nuevaImagen = mi.procesar_imagen(imagen)

        ancho = nuevaImagen.width
        alto = nuevaImagen.height
        tamano = (ancho,alto)
        self.assertEqual(tamano, (1123,750))

    def test_procesar_imagen_vertical(self):

        imagen = Image.open("ImagenTestVertical.jpg")
        nuevaImagen = mi.procesar_imagen(imagen)
        

        ancho = nuevaImagen.width
        alto = nuevaImagen.height
        tamano = (ancho,alto)
        self.assertEqual(tamano, (1123,750))
