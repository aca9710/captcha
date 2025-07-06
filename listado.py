#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Arturo Castillo Alpizar'

import os, json
import string
import random
def id_alfagen(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Listado():

    def __init__(self):
        flistado = os.path.join(os.path.dirname(__file__), 'listado.json')
        if not os.path.isfile(flistado):
            fch = open(flistado, 'w')
            fch.write('{}')
            fch.close()
        fcaptchas = open(flistado, 'r')
        listado = fcaptchas.read()
        fcaptchas.close()
        try:
            self._listado = json.loads(listado)
        except:
            self._listado = {}

        self._listaid = []
        for id in self._listado:
            self._listaid.append(id)  

        self._usoimagen = {}   
        mapa = self.mapa_id()
        for id in self._listado:
            for posicion in mapa:
                imagen = self._listado[id][posicion]
                if imagen not in self._usoimagen:
                    self._usoimagen[imagen] = []
                self._usoimagen[imagen].append(id)     


        

    def existeid(self, id):
        return id in self._listado

    def nuevo(self, ipp):        
        id = id_alfagen()
        while id in self._listado:
            id = id_alfagen()
        self._listado[id] = {"nombre": "", "seleccion": "", "texto": ""}  
        for item in self.mapa_id():
            self._listado[id][item] = ""

        if id not in self._listaid:
            self._listaid.append(id)

        self.guardar()    

        pag = self.localiza_id(id, ipp)

        return id, pag

    def localiza_id(self, idnuevo, ipp):
        pag = 1
        contador = 0
        for id in self._listado:
            contador += 1
            if id == idnuevo:
                break
            if contador > ipp:
                contador = 0
                pag += 1
        return pag        





    def actualiza(self, nombre, id, nodos, seleccion, texto):
        _lista = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
        if not self.existeid(id):
            if id.strip() == '':
                id = id_alfagen()
                while id in self._listado:
                    id = id_alfagen()
                self._listado[id] = {}    
            else:
                return
        try:    
            if seleccion[-1] == ',':
                seleccion = seleccion[:-1]    
        except:
            pass
        self._listado[id]['nombre'] = nombre
        self._listado[id]['seleccion'] = seleccion
        self._listado[id]['texto'] = texto

        if id not in self._listaid:
            self._listaid.append(id)

        nodos = nodos.split(',')
        contador = 0 
        for item in nodos:
            # imagen = item.split('/')[-1].split('?')[0]
            img_anterior = self._listado[id][_lista[contador]]
            self._listado[id][_lista[contador]] = item

            if item not in self._usoimagen:
                self._usoimagen[item] = []
            
            if img_anterior in self._usoimagen:
                lista = self._usoimagen[img_anterior]
                posicion = lista.index(id)
                self._usoimagen[img_anterior].pop(posicion)
            self._usoimagen[item].append(id)

            contador += 1

        self.guardar()    

        return
    
    def guardar(self):
        fich = open(os.path.join(os.path.dirname(__file__), 'listado.json'), 'w')
        fich.write(json.dumps(self._listado))
        fich.close()

    def id_filas(self):
        return [['00', '01', '02'], ['10', '11', '12'], ['20', '21', '22']]
    
    def mapa_id(self):
        return ['00', '01', '02', '10', '11', '12', '20', '21', '22']
    
    def lista(self):
        _lst = [] 
        for item in self._listado:
            nodo = self._listado[item]
            nodo['id'] = item
            _lst.append(nodo)
        return _lst
    
    def data(self):
        _lst = self.lista()
        return _lst, len(_lst)
    
    def borrar(self, id):
        existe = self.existeid(id)
        if existe:
            self._listado.pop(id)
            self.guardar()
            if id in self._listaid:
                self._listaid.remove(id)

        return existe



    def nodo(self, id):
        
        if self.existeid(id):
            _nodo = self._listado[id]
        else:
            _nodo = {}
            _nodo['nombre'] = ''
            _nodo['texto'] = ''
            _nodo['seleccion'] =[]
        return _nodo
    
    def aleatorio(self):
        lista = self._listaid
        for id in self._listado:
            lista.append(id)
        seleccion = '--'    
        while True:
            
            id = random.choice(lista)
            if id in self._listado:
                nodo = self._listado[id] 
                break
                 
        return id, nodo
    

    def imagenes(self, id):
        _lista = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
        imagenes = {}
        if id in self._listado:
            _listado = self._listado[id]
            for posicion in _lista:
                imagenes[posicion] = _listado[posicion]

