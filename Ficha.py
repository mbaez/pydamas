#!/bin/python

__author__="mbaez"
__date__ ="$19/10/2010 01:28:19$"

class Ficha:
	#Tipo de Ficha
	DAMA  =' DAMA '
	NORMAL='NORMAL'
	#Valor de la ficha segun su tipo
	PESO_DAMA=3
	PESO_NORMAL=1
	#Posibles valores de cada celda
	VACIA='    '
	USUARIO='USER'
	COMPUTADORA=' PC '
	#Para bloquear las casillas en las que no se pueden colocar fichas
	BLOQUEADA='####'
	
	def __init__(self,tipo=NORMAL, peso=PESO_NORMAL,duenho=VACIA):
		self.tipo= tipo
		self.peso= peso
		self.duenho=duenho
	'''
	Metodo llamado para crear una cadena de texto que represente a nuestro objeto. 
	Se utiliza cuando usamos print para mostrar nuestro objeto o cuando usamos la 
	funcion str(obj) para crear una cadena a partir de nuestro objeto.
	'''
	def get_copia(self):
		return Ficha(self.tipo,self.peso, self.duenho)
	def __str__(self):
		return str(self.duenho)#+":"+str(self.tipo)
