#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Arturo Castillo Alpizar'

import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np
import base64
import time


def affine_distortion(image):
    """Inclina el texto aleatoriamente."""
    rows, cols = image.shape[:2]
    
    # Puntos de origen (esquinas)
    pts1 = np.float32([[0, 0], [cols, 0], [0, rows]])
    # Puntos de destino (inclinados)
    pts2 = np.float32([[0, 0], 
                       [cols, np.random.randint(0, 20)], 
                       [0, rows - np.random.randint(0, 20)]])
    
    M = cv2.getAffineTransform(pts1, pts2)
    distorted = cv2.warpAffine(image, M, (cols, rows), borderMode=cv2.BORDER_REFLECT)
    return distorted

def generate_advanced_captcha(text, width=200, height=100):
    # Create base image
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Use a messy font and random positions
    font = ImageFont.truetype("arial.ttf", np.random.randint(30, 40))
    for i, char in enumerate(text):
        draw.text((10 + i * 30 + np.random.randint(-5, 5)), np.random.randint(10, 40), char, font=font, fill=(np.random.randint(0, 100), 0, 0))
    
    # Convert to OpenCV for distortions
    cv_image = np.array(image)
    cv_image = add_elastic_distortion(cv_image)  # Usar función previa
    
    # Add noise
    noise = np.random.randint(0, 50, cv_image.shape, dtype=np.uint8)
    cv_image = cv2.add(cv_image, noise)
    
    return Image.fromarray(cv_image)

def distort_text(image):
    rows, cols = image.shape[:2]
    # Distorsión afín
    pts1 = np.float32([[0,0], [cols-1,0], [0,rows-1]])
    pts2 = np.float32([[0,0], [cols-1,0], [np.random.randint(0,50),rows-1]])
    M = cv2.getAffineTransform(pts1, pts2)
    distorted = cv2.warpAffine(image, M, (cols,rows))
    return distorted

def add_elastic_distortion(image, alpha=10, sigma=5):
    h, w = image.shape[:2]
    
    # Generar campos de desplazamiento aleatorios
    dx = cv2.GaussianBlur((np.random.rand(h, w) * 2 - 1), (0, 0), sigma) * alpha
    dy = cv2.GaussianBlur((np.random.rand(h, w) * 2 - 1), (0, 0), sigma) * alpha
    
    # Malla de coordenadas
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    map_x = np.clip(x + dx, 0, w - 1).astype(np.float32)
    map_y = np.clip(y + dy, 0, h - 1).astype(np.float32)
    distorted = cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR)
    return distorted

def elastic_distortion(image, alpha=15, sigma=5):
    """Distorsión elástica para simular texto ondulado."""
    h, w = image.shape[:2]
    
    # Generar campos de desplazamiento aleatorios
    dx = cv2.GaussianBlur((np.random.rand(h, w) * 2 - 1), (0, 0), sigma) * alpha
    dy = cv2.GaussianBlur((np.random.rand(h, w) * 2 - 1), (0, 0), sigma) * alpha
    
    # Malla de coordenadas
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    map_x = np.clip(x + dx, 0, w - 1).astype(np.float32)
    map_y = np.clip(y + dy, 0, h - 1).astype(np.float32)
    
    return cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def add_noise(image):
    """Añade ruido y líneas aleatorias."""
    # Ruido gaussiano
    noise = np.zeros_like(image)
    cv2.randn(noise, 0, 80)
    noisy_image = cv2.add(image, noise)
    
    # Líneas aleatorias
    for _ in range(np.random.randint(3, 7)):
        color = (np.random.randint(0, 255), 0, 0)
        pt1 = (np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0]))
        pt2 = (np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0]))
        cv2.line(noisy_image, pt1, pt2, color, thickness=3)
    
    return noisy_image

def pil_to_cv2(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def cv2_to_pil(cv2_image):
    return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))


# Pillow

def blur(imagen):
    blurImagen = imagen.filter(ImageFilter.BLUR)
    return blurImagen

def boxblur(imagen):
    blurImagen = imagen.filter(ImageFilter.BoxBlur(5))
    return blurImagen


def gaussianblur(imagen):
    blurImagen = imagen.filter(ImageFilter.GaussianBlur(5))
    return blurImagen


def leftright(imagen):
    blurImagen = imagen.transpose(Image.FLIP_LEFT_RIGHT)
    return blurImagen

def topbottom(imagen):
    blurImagen = imagen.transpose(Image.FLIP_TOP_BOTTOM)
    return blurImagen


def marcaagua(imagen):
    
    width, height = imagen.size
    draw = ImageDraw.Draw(imagen)
    
    text = "sample watermark" 
    font = ImageFont.load_default(10)
    #font = ImageFont.truetype('Lato.ttf', 10)
    textwidth, textheight = draw.textsize(text, font)

    # calculate the x,y coordinates of the text
    margin = 1
    x = width - textwidth - margin
    y = height - textheight - margin

    # draw watermark in the bottom right corner
    draw.text((x, y), text, font=font)

    return imagen


import string
import random
def id_alfagen(size=8, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

def marcaag(imagen):
    marca = id_alfagen(6)
    im = imagen.convert('RGBA')
    # watermark
    font = ImageFont.load_default(20)
    size = font.getbbox(marca)
    opacity = int(256 * .5)
    mark_width = size[2]
    mark_height = size[3]
    watermark = Image.new('RGBA', (mark_width, mark_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    draw.text((0, 0), text=marca, font=font, fill=(0, 0, 0, opacity))
    angle =  random.randint(0, 85) # math.degrees(math.atan(100 / 100)) +
    watermark = watermark.rotate(angle, expand=1)

    # merge
    wx, wy = watermark.size
    px = int((100 - wx) / 2)
    py = int((100 - wy) / 2)
    im.paste(watermark, (px, py, px + wx, py + wy), watermark)
    return im







import random

if __name__ == '__main__':
    ofuscadores = [distort_text, add_elastic_distortion, elastic_distortion, add_noise, affine_distortion,]
    otxt = ['distort_text', 'add_elastic_distortion', 'elastic_distortion', 'add_noise', 'affine_distortion']

    ofuscpil = [blur, boxblur, leftright,  marcaag] 
    ofuscpiltxt = ['blur', 'boxblur', 'leftright',  'marcaag']

    ofuscadores.extend(ofuscpil)
    otxt.extend(ofuscpiltxt)

    carpeta_imagenes = os.path.join(os.path.dirname(__file__), 'static', 'captchas')
    carpetab64 = os.path.join(carpeta_imagenes,'b64')
    carpetaofusc = os.path.join(carpeta_imagenes,'ofusc')
    if not os.path.isdir(carpetaofusc):
        os.makedirs(carpetaofusc)

    imagenes = os.listdir(carpeta_imagenes)
    
    pendientes = []
    lista_o = os.listdir(carpetaofusc)
    for item in imagenes:
        if '.png' in item:
            # fich_imagen = os.path.join(carpeta_imagenes, item)
            xofuscar = os.path.join(carpetaofusc, item)
            if xofuscar in lista_o:
                continue
            pendientes.append(item)
    
    pendientes.extend(lista_o)
    while True:
        nombre_imagen = pendientes[0]
        
        fich_imagen = os.path.join(carpeta_imagenes, nombre_imagen)
        ofuscado = os.path.join(carpetaofusc, nombre_imagen)
        if os.path.isfile(ofuscado):
            os.remove(ofuscado)
        
        imagen = Image.open(fich_imagen)  
        ofuscador = random.randint(0, len(ofuscadores) - 1)
        txto = otxt[ofuscador] 
        if txto in ofuscpiltxt:
            try: 
                imagen1 = imagen
                imagen= ofuscadores[ofuscador](imagen1)                            
            except:
                print("Ha fallado %s" % txto)
                del imagen1
                del imagen
                continue

        else:
            imagen_cv2 = pil_to_cv2(imagen)
            del imagen            
            try:
                imagen_cv2 = ofuscadores[ofuscador](imagen_cv2)                         
            except:
                print("Ha fallado %s" % txto)
                del imagen_cv2
                continue
            imagen = cv2_to_pil(imagen_cv2)
            del imagen_cv2           

        imagen.save(ofuscado, quality=20, optimize=True)
        del imagen
        
        data = base64.b64encode(open(ofuscado, "rb").read()).decode('utf-8')
        data = "data:image/png;base64, " + data
        
        f = open(os.path.join(carpetab64, nombre_imagen.replace('.png', '.b64')), "w")
        f.write(data)
        f.close()

        pendientes.remove(nombre_imagen)
        pendientes.append(nombre_imagen)
        print("Se ha ofuscado %s con %s" % (nombre_imagen, txto))
        time.sleep(1)
