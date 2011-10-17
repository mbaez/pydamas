#!/bin/python
from Tablero import *
from Minimax import *

__author__="mbaez"
__date__ ="$19/10/2010 23:28:01$"

'''
Game actua como una interfaz entre lo que seria la interfaz grafica
y la inteligencia artificial
'''

class Game:
	def __init__(self):
		evaluacion=Tablero()
		algoritmo=Minimax()
		self.tablero=Tablero(evaluacion.evaluar_suma_peso)
		self.tablero.cargar_fichas()
		self.minimax=Minimax(algoritmo.minimax);
	def quien_gano(self):
		value=self.tablero.evaluar_suma(1)
		if(value < 0):
			return "Perdiste!!!"
		return "Ganaste!!!"
	
	def juega_computadora(self):
		old_move_computadora,new_move_computadora=self.minimax.start(self.tablero)
		print "score : ", new_move_computadora
		lista, comer_move=self.tablero.comer_fichas(old_move_computadora)
		if(len(lista)-1==0):
			self.tablero.mover_ficha(old_move_computadora,new_move_computadora)
			lista.append(old_move_computadora)
			lista.append(new_move_computadora)
			comer_move=[]
		if(self.tablero.es_dama(new_move_computadora,Ficha.COMPUTADORA)):
			self.tablero.crear_dama(new_move_computadora, Ficha.COMPUTADORA)
		return lista,comer_move
		'''

		'''
	def traducir_a_index(self, move):
		return move.i*8+move.j%8
		
	def juega_usuario(self,x,y):
		
		'''
		debe verificar si:
		se comio una ficha y actualizar el tablero
		'''
	def realizar_movimiento(self, old_move, new_move):
		if(self.tablero.es_valido_move(old_move,new_move)):
			if(self.es_dama_usuario(old_move)):
				#prueba una posicion
				self.tablero.mover_ficha(old_move, new_move)
				comer_move=self.tablero.get_pos_ficha_anterior(old_move,new_move)
				if(not self.tablero.es_duenho(comer_move, Ficha.COMPUTADORA)):
					comer_move=None
			else:
				comer_move=self.tablero.comer_ficha(old_move, new_move)
				self.tablero.mover_ficha(old_move, new_move)
				if(self.es_dama_usuario(new_move)):
					self.tablero.crear_dama(new_move)
			if not (comer_move==None):
				print self.tablero
				self.tablero.eliminar_ficha(comer_move)
				return comer_move.i*Tablero.MAX_DIM+comer_move.j%Tablero.MAX_DIM
			return True
		return False
		
	def route_valido(self, old_move, new_move):
		copia=self.tablero.get_copia()
		if(copia.es_valido_move(old_move,new_move)):
			return True
		return False
	
	def esta_bloqueada(self, move):
		if(self.tablero.casillas[move.i][move.j].duenho==Ficha.BLOQUEADA):
			return True;
		return False
	'''
	verifica si una casilla esta ocupada por el duenho
	'''
	def ocupe_casilla(self, move, duenho=Ficha.USUARIO):
		if(self.tablero.es_vacio(move.i, move.j) or not self.tablero.casillas[move.i][move.j].duenho==duenho):
			return False
		return True
	
	def eliminar_ficha(self, move):
		self.tablero.casillas[move.i][move.j]=Ficha()
	
	def es_dama_usuario(self,move):
		return self.tablero.es_dama(move, Ficha.USUARIO)
	def es_dama_computadora(self, move):
		return self.tablero.es_dama(move, Ficha.COMPUTADORA)
	def es_ficha_usuario(self,move):
		return self.tablero.casillas[move.i][move.j].duenho==Ficha.USUARIO
	def es_ficha_computadora(self, move):
		return self.tablero.casillas[move.i][move.j].duenho==Ficha.COMPUTADORA
	
