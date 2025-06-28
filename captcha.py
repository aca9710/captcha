#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Arturo Castillo Alpizar'

import os

from werkzeug.utils import secure_filename
from flask import (Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory)
import time
import json
from flask import json, jsonify
import datetime, hashlib, base64
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps
import zlib
import math
from listado import Listado
import logging
from logging.config import dictConfig


app = Flask(__name__)

def obt_traza():
    if not hasattr(g, 'traza'):        
        logger = logging.getLogger('captchas')
        logger.setLevel(logging.DEBUG) 
        error_handler = logging.FileHandler(app.config['ferror'])
        error_handler.setLevel(logging.ERROR)
        traza_handler = logging.FileHandler(app.config['finfo'])
        traza_handler.setLevel(logging.DEBUG)
        error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d - %(funcName)s')
        traza_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        error_handler.setFormatter(error_formatter)
        traza_handler.setFormatter(traza_formatter)
        logger.addHandler(error_handler)
        logger.addHandler(traza_handler)
        g.traza = logger       
    return g.traza    





def carga_listado():
    g.listado = Listado()

    
def actualiza_listado(nombre, id, nodos, seleccion=[], texto=''):
    if not hasattr(g, 'listado'):
        carga_listado()
    g.listado.actualiza(nombre, id, nodos, seleccion, texto)


def obtener_listado():
    if not hasattr(g, 'listado'):
        carga_listado()
    return g.listado

def hash_fichero(fichero):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    md5 = hashlib.md5()
    with open(fichero, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()

def sha1(txt):
    import hashlib
    m = hashlib.sha1()
    m.update(txt)
    txt = m.hexdigest()
    return txt

import traceback, sys


def paginador(_paginador):    
    total = _paginador['total']
    ipp = _paginador['itemsxpag']
    _paginador['num_pages'] = int(_paginador['total'] // _paginador['itemsxpag']) 
    if (total / ipp) != (total // ipp) :
        _paginador['num_pages'] = _paginador['num_pages'] + 1

    _paginador['has_previous'] = _paginador['number'] > 1
    _paginador['previous_page_number'] = _paginador['number'] - 1
    _paginador['has_next'] = _paginador['number'] < _paginador['num_pages']
    _paginador['next_page_number'] = _paginador['number'] + 1
    _paginador['init'] = (_paginador['number'] - 1) * _paginador['itemsxpag']
    return _paginador


app.config.from_object(__name__)

SECRET_KEY=b'_5#y2L"F4Q8z\n\xec'


pagcaptchas= paginador({'number': 1, 'itemsxpag': 18, 'total': 0})

pagimagenes= paginador({'number': 1, 'itemsxpag': 9, 'total': 0})


local = os.path.dirname(__file__)

carp_log = os.path.join(local,'log')
carp_imp_tmp = os.path.join(local,'static/tmp')
carp_captchas = os.path.join(local,'static/captchas')
carp_captchas_tmp = os.path.join(local,'static/captchas/tmp')
carp_captchas_b64 = os.path.join(local,'static/captchas/b64')

if not os.path.isdir(carp_log):
    os.makedirs(carp_log)

if not os.path.isdir(carp_imp_tmp):
    os.makedirs(carp_imp_tmp)

if not os.path.isdir(carp_captchas_b64):
    os.makedirs(carp_captchas_b64)    

if not os.path.isdir(carp_captchas_tmp):
    os.makedirs(carp_captchas_tmp) 

app.config.update(
    SECRET_KEY=SECRET_KEY,
    carp_log=carp_log,
    ferror=os.path.join(carp_log, 'Error.log'),
    finfo=os.path.join(carp_log, 'Traza.log'),
    carp_imp_tmp=carp_imp_tmp,
    carp_captchas=carp_captchas,
    carp_captchas_tmp=carp_captchas_tmp,
    carp_captchas_b64=carp_captchas_b64,
    pagcaptchas=pagcaptchas, 
    pagimagenes=pagimagenes,
    sec_rect=['00', '01', '02', '10', '11', '12', '20', '21', '22']
)

if os.name == 'nt':
    app.config.update(
        SECRET_KEY=SECRET_KEY,
        carp_imp_tmp=app.config['carp_imp_tmp'].replace('/', os.sep),
        pngquant='pngquant.exe',

        deletefile='del',
        copyfile='copy'
    )
app.debug = True


@app.route('/')
# @login_required
def inicial():
    itemsxpag = 17
    _paginador = {'number': 1, 'itemsxpag': itemsxpag, 'total': 0}
    _paginador = paginador(_paginador)
    return render_template('base.html', STATIC_URL='/static/', paginator=_paginador)

def obt_listaimagenes(pag):
    _paginador, rejilla = rellena_reg_img(pag) 
    return render_template('listaimagenes.html', STATIC_URL='/static/', paginator=_paginador, rejilla=rejilla)


@app.route('/pag_im/')
# @login_required
def listaimg():
    pag = request.args.get('pag', 1, int)
    return obt_listaimagenes(pag)

def rellena_reg_img(pag):
    filas = 6
    columnas = 3
    rejilla = []
    for fila in range(filas):
        lista = []
        for col in range(columnas):
            nodo = {'id': 'n%s%s' % (fila, col), "img": ''}
            lista.append(nodo)
        rejilla.append(lista)

    tmp = sorted(os.listdir(app.config['carp_captchas']))
    imagenes = []
    for item in tmp:
        if os.path.isdir(os.path.join(app.config['carp_captchas'], item)):
            continue

        if item.lower()[-4:] != '.png':
            continue

        imagenes.append(item)               

    _paginador = app.config['pagimagenes']
    _paginador['itemsxpag'] = filas * columnas
    _paginador["total"] = len(imagenes)
    _paginador["number"] = pag    
    _paginador = paginador(_paginador)

    posicion = _paginador['init'] 
    tmp = []
    total = len(imagenes)
    if posicion < total:
        for fila in range(filas):
            for col in range(columnas):            
                if total > posicion:
                    rejilla[fila][col]["img"] = imagenes[posicion]
                posicion += 1


    return _paginador, rejilla

def obt_listanombres(pag, id):
    color = [0,2,4,6,8,10,12,14,16,18,20]
    colores = []
    for i in range(20):
        if i in color:
            colores.append("#e5ffe8")
        else:
            colores.append('white')
        i += 1    

    _listado = obtener_listado()  
    listado, total = _listado.data()     
    _paginador = app.config['pagcaptchas']
    _paginador['total'] = total
    _paginador['number'] = pag
    _paginador = paginador(_paginador)
    itemsxpag = _paginador['itemsxpag']
    i = 0
    data = []
    if total > 0:
        inicio = (pag - 1) * itemsxpag
        final = inicio+itemsxpag
        tmp = listado[inicio:final]
        for item in tmp:
            item['color'] = colores[i]
            data.append(item) 
            i += 1 
    
    


    
    return render_template('listanombres.html', STATIC_URL='/static/', captchas=data,
                            paginator=_paginador, pag=pag, idsel=id, color=colores)


@app.route('/listanombres/')
# @login_required
def listanombres():
    try:
        pag = request.args.get('pag', 1, type=int)
        id = request.args.get('id', '-')
        resultado = obt_listanombres(pag, id)
        return resultado
    except Exception as e:
        obt_traza().error(e)
        return jsonify('error')


@app.route('/listacaptchas123/')
# @login_required
def creacaptcha123():
    try:
        pag = request.args.geit('pag', 1, type=int)
        _listado = obtener_listado()
        listado, total = _listado.data()

        itemsxpag = 17
        _paginador = {'number': pag, 'itemsxpag': itemsxpag, 'total': total}
        _paginador = paginador(_paginador)
        data = []
        if total > 0:
            inicio = (pag - 1) * itemsxpag
            final = inicio+itemsxpag
            data = listado[inicio:final]
        tmp = os.listdir(os.path.join(os.path.dirname(__file__), app.config['carp_imp_tmp']))
        imagenes = []
        i = 0
        for img in tmp:
            if '.jpg' in img or '.gif' in img or '.png' in img:
                imagenes.append(img)
                i+=1
        
        idfilas= _listado.id_filas()

        return render_template('listacaptchas.html', STATIC_URL='/static/', captchas=data,
                               paginator=_paginador, pag=pag, imagenes=imagenes,  idfilas=idfilas)
    except Exception as e:
        obt_traza().error(e)
        return jsonify('error')


import string
import random
def id_alfagen(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/actualizar/', methods=['GET'])
def actualizar():
    try:
        nombre = request.args.get('nombre', '')
        pag = request.args.get('pag', 1, type=int)
        texto = request.args.get('texto', '')
        id = request.args.get('id', '')
        imagenes = request.args.get('img', '')
        selec = request.args.get('lista', '')
        selec = selec.split(',')
        activos = ''
        for item in selec:
            item = item.strip()
            if len(item) > 0:
                activos = activos + item + ','
        activos = activos[:-1]

        listado = obtener_listado()
        listado.actualiza(nombre, id, imagenes, activos.strip(), texto.strip())

        #apr(nombre, texto, activos)

        return jsonify(True)
    except Exception as e:
        obt_traza().error(e)
        return jsonify(False)



@app.route('/borrar_captcha/', methods=['GET'])
def borrar_captcha():
    
    id = request.args.get('id', '')
    pag = request.args.get('pag', 1, type=int)
    _listado = obtener_listado()
    _listado.borrar(id)
        
    return obt_listanombres(pag, id)




def tm(imagen, size):
    NEAREST = NONE = 0
    resample = NEAREST
    modos ={'LA':'La', 'RGBA':'RGBa'}
    try:
        size = tuple(size)
        box = (0, 0) + imagen.size

        if imagen.size == size and box == (0, 0) + imagen.size:
            return imagen.copy()

        if imagen.mode in ["1", "P"]:
            resample = NEAREST
        elif imagen.mode in ["LA", "RGBA"]:  
            return imagen.convert(modos[imagen.mode]).resize(size, resample, box).convert(imagen.mode) 

        imagen.load()
    except Exception as e:
        obt_traza().error(e)

    return imagen._new(imagen.im.resize(size, resample, box))


def trazaw(texto):
    ferror = os.path.join(os.path.dirname(__file__), 'log', 'trazai.log')
    if os.path.isfile(ferror):
        strad = open(ferror, 'a')
    else:
        strad = open(ferror, 'w')
    strad.write(texto)
    strad.close()


import base64
@app.route('/importar/', methods=['GET', 'POST'])
def importar_imagen():
    try:

        if request.method == 'POST':
            if 'file' in request.files:
                file = request.files['file']
                nombre_fichero = secure_filename(file.filename)
                nombre_local = camino = os.path.join(app.config['carp_imp_tmp'], nombre_fichero )
                if os.path.isfile(nombre_local):
                    os.remove(nombre_local)
                file.save(nombre_local)              
                trazaw('Guardado: %s\n' % nombre_local)
                importar(nombre_fichero, nombre_local)
                return 'ok'
    except Exception as e:
        obt_traza().error(e)
        return 'error'
    

def importar(nombre_fichero, nombre_local):
    carpeta_recorte_temporal = app.config['carp_captchas_tmp']
    carpeta_codificados = app.config['carp_captchas_b64']
    carpeta_captchas = app.config['carp_captchas']
    idimagen =  app.config['sec_rect']

    fich = open(nombre_local, 'rb')
    datos = fich.read()
    fich.close()
    nombre_hash = sha1(datos)
    del datos
   
    try:
        rangox = 3
        rangoy = 3
        try:
            imagen = Image.open(nombre_local)
            x = imagen.size[0]
            y = imagen.size[1]
            maxx = 300
            maxy = 300
            if x > maxx or y > maxy:
                size = maxx, maxy
                x, y = imagen.size
                if x > size[0]:
                    y = int(max(y * size[0] / x, 1))
                    x = int(size[0])
                if y > size[1]:
                    x = int(max(x * size[1] / y, 1))
                    y = int(size[1])
                size = x, y
                imagen = tm(imagen, size)

            ancho = int(imagen.size[0] / rangox)
            alto = int(imagen.size[1] / rangoy)
            
            indice = 0           
            
            for si in range(rangoy):
                for gh in range(rangox):
                    caja = (gh * ancho, si * alto, (gh * ancho) + ancho, (si * alto) + alto)
                    region = imagen.crop(caja)
                                       
                    nombgen =  nombre_hash + idimagen[indice]
                    
                    fichero = os.path.join(carpeta_recorte_temporal, nombgen + '.png')
                    if os.path.isfile(fichero):
                        os.remove(fichero)

                    region.save(fichero, quality=20, optimize=True)

                    dest = os.path.join(carpeta_captchas, nombgen + '.png') 
                    if os.path.isfile(dest):
                        os.remove(dest)

                    shutil.move(fichero, dest)
                        
                    b64 = os.path.join(carpeta_codificados, nombgen + '.b64')
                    if os.path.isfile(b64):
                        os.remove(b64)

                    indice += 1
                    data = base64.b64encode(open(dest, "rb").read()).decode('utf-8')
                    data = "data:image/png;base64, " + data
                    try:
                        f = open(b64, "w")
                        f.write(data)
                        f.close()
                        trazaw('guardado : %s.b64\n' % dest)
                    except Exception as e:
                        obt_traza().error(e)
        except Exception as e:
            obt_traza().error(e)
    except Exception as e:
        obt_traza().error(e)


@app.route('/captchajson/', methods=['GET'])
def expcaptchajson():
    try:
        fcaptchas = open(os.path.join(os.path.dirname(__file__), 'listado.json'), 'r')
        data = fcaptchas.read()
        fcaptchas.close()
        listado = json.loads(data)
        item = random.randint(0,  len(listado)-1)
        item = listado[item]
        newdic = {}
        nombre = item['nombre']
        carpeta = os.path.join(os.path.dirname(__file__), app.config['carp_imp_tmp'], 'captchas')
        time.sleep(5)
        for i in range(9):
            path = nombre + str(i) + '.png'
            textaleat(path, carpeta)  # adiciona texto + demora
            path = os.path.join(carpeta, path)
            if os.path.isfile(path+'.b64'):
                data = open(path+'.b64', "rb").read()
                data = data.replace("data:image/png;base64, ", '')
                newdic['img' + str(i)] = data
            else:
                data = base64.b64encode(open(path, "rb").read())
                newdic['img' + str(i)] = "" + data
                try:
                    f = open(path + '.b64', "w")
                    f.write(data)
                    f.close()
                except Exception as e:
                    obt_traza().error(e)

        newdic['id'] = item['id']
        newdic['activos'] = item['activos']
        newdic['texto'] = item['texto']

    except Exception as e:
        obt_traza().error(e)
        item = ''
    return jsonify(newdic)

@app.route('/captcha/', methods=['GET'])
def expcaptcha():
    try:
        id = request.args.get("id", "")
        return obt_captcha(id)
    except Exception as e:
        obt_traza().error(e)


def obt_captcha(id):
    try:
        _listado = obtener_listado()
        if _listado.existeid(id):
            nodo = _listado.nodo(id)
            prueba = True
        else:
            id, nodo = _listado.aleatorio()  
            prueba = False


        obt_traza().info("Captcha seleccionado %s" % id)  
  

        mapa = _listado.mapa_id()
        
        carpetai = os.path.join(os.path.dirname(__file__),app.config['carp_captchas'], 'b64')
        imgs = []


        idfilas = _listado.id_filas()

        rejilla = []
        fila = 0
        for columnas in idfilas:
            nodof = []
            for col in columnas:  
                if col in nodo: 
                    img = nodo[col]
                else: 
                    img = 'static/img/exclamation.svg'
                    data = ''
                   
                     
                
                if img.strip() == '':
                    img = 'static/img/exclamation.svg'
                    data = ''
                else:
                    fichero = os.path.join(carpetai, img).replace('.png', '.b64')
                    data = ""
                    if os.path.isfile(fichero):
                        fch = open(fichero, "rb")
                        data = fch.read().decode('utf-8')
                        fch.close()

                        if not 'data:' in data:
                            data = "data:image/png;base64," + data   
                nodof.append({'id': 'v' + col, 'img': data})
            rejilla.append(nodof)    

        serie = id
        id = ''   


        fichero = os.path.join(os.path.dirname(__file__), 'static', 'img', 'ok.png')
        if os.path.isfile(fichero + '.b64'):
            ok = open(fichero + '.b64', "rb")
            okb64 = ok.read().decode('utf-8')
            ok.close()            
        else:
            fch = open(fichero, "rb")
            okb64 = base64.b64encode(fch.read())
            fch.close()
            okb64 = okb64.decode('utf-8')

        if not 'data:' in okb64:
                okb64 = "data:image/png;base64," + okb64             
    except Exception as e:
        obt_traza().error(e)

    return render_template('captcha.html', STATIC_URL='/static/', serie=serie, ident=serie,
                           nombre=nodo['nombre'], texto=nodo['texto'], okb64=okb64, prueba=prueba, captchas=rejilla)


@app.route('/validar/', methods=['POST'])
def validar():
    try:
        resultado = {"resultado": "Denegado"}
        if request.method == 'POST':
            serie = request.form['serie']
            ident = request.form['ident']
            seleccion = request.form['seleccion'].strip().replace('v', '')[:-1]

       
            _listado = obtener_listado()
            if _listado.existeid(ident):
                nodo = _listado.nodo(ident)
                tmp = sorted(nodo['seleccion']) == sorted(seleccion)
                if tmp:
                    resultado = {"resultado": "Aceptado" }
                else:
                    resultado = {"resultado": "Denegado" }
                
            else:
                resultado = {"resultado": "Denegado"}
    except Exception as e:
        obt_traza().error(e)
        resultado = {"resultado": "Denegado"}

    return jsonify(resultado)

@app.route('/nuevo_captcha/', methods=['GET'])
def nuevo_captcha():
    try:
        resultado = False
        if request.method == 'GET':            
            _listado = obtener_listado()
            id, pag = _listado.nuevo(app.config['pagcaptchas']['itemsxpag'])            
            return redirect('/listanombres/?pag=%s&id=%s' % (pag, id))
    except:
        pass

@app.route('/guarda_captcha/', methods=['POST'])
def guarda_captcha():
    try:
        resultado = False
        if request.method == 'POST':
            nombre = request.form['nom']
            seleccion = request.form['sel']
            id = request.form['id']
            imagenes = request.form['img']
            texto = request.form['txt']
            pag = request.form['pag']
            
            _listado = obtener_listado()
            _listado.actualiza(nombre, id, imagenes, seleccion, texto)
            
            return redirect('/listanombres/?pag=%s&id=%s' % (pag, id))
    except Exception as e:
        obt_traza().error(e)

    return jsonify('')

@app.route('/listacaptchas/', methods=['GET'])
def nueva():
    try:
        pag = request.args.get('pag', 1, type=int)
        _listado = obtener_listado()  
        listado, total = _listado.data()          

        itemsxpag = 17
        _paginador = {'number': pag, 'itemsxpag': itemsxpag, 'total': total}
        _paginador = paginador(_paginador)
        data = []
        if total > 0:
            inicio = (pag - 1) * itemsxpag
            final = inicio+itemsxpag
            tmp = listado[inicio:final]
            for item in tmp:
                data.append(item)

        rejilla = [
            [['00', '01', '02'],['10', '11', '12'],['20', '21', '22']],
            []             
        ]           
        _paginadori, rejilla[1] = rellena_reg_img(1)        

        principal = render_template('principal.html', STATIC_URL='/static/', captchas=data,
                               paginator=_paginadori, paginatori=_paginadori, pag=pag, rejilla=rejilla)

        listanombres = obt_listanombres(1, '')
        listaimagenes = obt_listaimagenes(1)
        rejillacaptcha = obt_rejillacaptcha('')
        captcha = '' # obt_captcha('abcd')

        principal = principal.replace('&&listanombres', listanombres)
        principal = principal.replace('&&listaimagenes', listaimagenes)
        principal = principal.replace('&&rejillacaptcha', rejillacaptcha)
        principal = principal.replace('&&pruebacaptcha', captcha)
        
        return principal
    except Exception as e:
        obt_traza().error(e)
        return jsonify('error')

def obt_rejillacaptcha(id):
    _listado = obtener_listado()
    _ldata = _listado.nodo(id)
    idfilas = _listado.id_filas()
    rejilla = []
    fila = 0
    for columnas in idfilas:
        nodo = []
        for col in columnas:  
            if col not in _ldata:  
                _ldata[col] = ""        
            img = _ldata[col]
            if img.strip() == '':
                img = 'static/img/exclamation.svg'
            else:
                img = 'static/captchas/' + img    
            nodo.append({'id': col, 'img': img})
        rejilla.append(nodo)    
    return render_template('rejillacaptcha.html', STATIC_URL='/static/', rejilla=rejilla, 
                                    nombre=_ldata['nombre'], texto=_ldata['texto'], seleccionado=_ldata['seleccion'],id=id)


@app.route('/rejillacaptcha/', methods=['GET'])
def rejillacaptcha():    
    if request.method == 'GET':
        id = request.args.get('id', '')        
        return obt_rejillacaptcha(id)            
    return redirect('/?pag=1')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5002)
