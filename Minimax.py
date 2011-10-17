#!/bin/python

__author__="mbaez"
__date__ ="$19/10/2010 01:40:19$"

from Tablero import *
from Ficha import *
from Move import *

'''
Falta copiar lo que tengo en papel
'''
class Minimax:
	MAX_LEVEL=3
	def __init__(self, minimax_function=0, max_level=3):
		self.nodos=0
		self.start=minimax_function
		Minimax.MAX_LEVEL=max_level
		
	def minimax(self, tablero):
		print "minimax"
		return self.max_value(tablero,1)
	
	def minimax_alpha_beta(self, tablero):
		self.BETA = (1L<<700)-1L
		self.ALPHA = -self.BETA
		print "alphabeta"
		return self.max_value_alphabeta(tablero,1)
	
	def min_value(self, tablero, level):
		mejor_move=Move(-1,-1,1000)
		old_move=Move(-1,-1)
		tablero_copy=tablero.get_copia()
		old_move_anterior_buffer=Move(-1,-1)
		if(not tablero.fin_del_juego()and level<=Minimax.MAX_LEVEL):
			for i in range(Tablero.MAX_DIM):
				for j in range(Tablero.MAX_DIM):
					old_move_buffer=Move(i,j)
					if tablero_copy.es_duenho(old_move_buffer):
						move_validos=tablero_copy.get_lista_move_validos(old_move_buffer, old_move_anterior_buffer)
						#self.nodos=self.nodos+1
						for move_valido in move_validos:
							#si es que puede come todas las fichas posibles
							lista=tablero_copy.comer_fichas(old_move_buffer,1,Ficha.USUARIO)
							if(len(lista)-1==0):
								#prueb una posicion
								tablero_copy.mover_ficha(old_move_buffer, move_valido)
							#expande al otro nodo
							old,move_result=self.max_value(tablero_copy, level+1)
							#Obtiene el puntaje obtenido 
							#move_valido.score=tablero_copy.evaluar_suma_peso() #+ move_result.score
							move_valido.score=move_result.score
							'''
							Selecciona mayor valor del move para la computadora
							Significa que en el peor de los casos el valor sera el del mejor_move.score
							Atender el signo, todavia me confunde
							'''
							if move_valido.score <= mejor_move.score:
								mejor_move=move_valido
								#mejor_move.score=move_result.score
								old_move=old_move_buffer
							#pone la ficha en su posicion inicial
							tablero_copy=tablero.get_copia()
						old_move_anterior_buffer=Move(i,j)
		else:
			#mejor_move.score=tablero.evaluar_suma_peso()
			mejor_move.score=tablero.evaluar()
		return old_move,mejor_move
		
	def max_value(self, tablero, level):
		range_list=[7,6,5,4,3,2,1,0]
		mejor_move=Move(-1,-1,-1000)
		old_move=Move(-1,-1)
		old_move_anterior_buffer=Move(-1,-1)
		tablero_copy=tablero.get_copia()
		if(not tablero.fin_del_juego() and level<=Minimax.MAX_LEVEL):
			for i in range_list:
				for j in range_list:
					old_move_buffer=Move(i,j)
					#Genera los movimientos validos para la computadora
					if (tablero_copy.es_duenho(old_move_buffer, Ficha.COMPUTADORA)):
						move_validos=tablero_copy.get_lista_move_validos(old_move_buffer,old_move_anterior_buffer,-1,Ficha.COMPUTADORA)
						for move_valido in move_validos:
							#self.nodos=self.nodos+1
							#si es que puede come todas las fichas posibles
							lista=tablero_copy.comer_fichas(old_move_buffer)
							if(len(lista)-1==0):
								#prueba una posicion
								tablero_copy.mover_ficha(old_move_buffer, move_valido)
							#expande el siguiente nodo
							old, move_result=self.min_value(tablero_copy, level+1)
							#evalua el movimiento actual
							#move_valido.score=tablero_copy.evaluar_suma_peso(-1) +move_result.score
							#se le suma el puntaje obtenido al realizar dicho movimiento
							move_valido.score=move_result.score
							'''
							Selecciona el move de menor riesgo para la computadora
							Atender el signo, todavia me confunde
							'''
							if move_valido.score >= mejor_move.score:
								mejor_move=move_valido
								old_move=old_move_buffer
							#pone el tablero en su posicion inicial
							tablero_copy=tablero.get_copia()
					old_move_anterior_buffer=Move(i,j)
		else:
			#mejor_move.score=tablero.evaluar_suma_peso(-1)
			mejor_move.score=tablero.evaluar(-1)
			
		return old_move,mejor_move
		

	def min_value_alphabeta(self, tablero, level):
		mejor_move=Move(-1,-1,1000)
		old_move=Move(-1,-1)
		old_move_anterior_buffer=Move(-1,-1)
		tablero_copy=tablero.get_copia()
		old_move_anterior_buffer=Move(-1,-1)
		if(not tablero.fin_del_juego()and level<=Minimax.MAX_LEVEL):
			for i in range(Tablero.MAX_DIM):
				for j in range(Tablero.MAX_DIM):
					old_move_buffer=Move(i,j)
					if tablero_copy.es_duenho(old_move_buffer):
						move_validos=tablero_copy.get_lista_move_validos(old_move_buffer,old_move_anterior_buffer)
						for move_valido in move_validos:
							#si es que puede come todas las fichas posibles
							lista=tablero_copy.comer_fichas(old_move_buffer,2,Ficha.USUARIO)
							#self.nodos=self.nodos+1
							if(len(lista)-1==0):
								#prueb una posicion
								tablero_copy.mover_ficha(old_move_buffer, move_valido)
							#expande al otro nodo
							old,move_result=self.max_value_alphabeta(tablero_copy, level+1)
							#Obtiene el puntaje obtenido 
							#move_valido.score=tablero_copy.evaluar_suma_peso() #+ move_result.score
							move_valido.score=move_result
							'''
							Selecciona mayor valor del move para la computadora
							Significa que en el peor de los casos el valor sera el del mejor_move.score
							Atender el signo, todavia me confunde
							'''
							if move_valido.score <= mejor_move.score:
								mejor_move=move_valido
								#mejor_move.score=move_result.score
								old_move=old_move_buffer
							
							if mejor_move.score < self.BETA:
								self.BETA = mejor_move.score
							
							if self.BETA <= self.ALPHA: return old_move,mejor_move
							
							#pone la ficha en su posicion inicial
							tablero_copy=tablero.get_copia()
						old_move_anterior_buffer=Move(i,j)
		else:
			#mejor_move.score=tablero.evaluar_suma_peso()
			mejor_move.score=tablero.evaluar()
		return old_move,mejor_move
		
	def max_value_alphabeta(self, tablero, level):
		range_list=[7,6,5,4,3,2,1,0]
		mejor_move=Move(-1,-1,-1000)
		old_move=Move(-1,-1)
		old_move_anterior_buffer=Move(-1,-1)
		tablero_copy=tablero.get_copia()
		if(not tablero.fin_del_juego() and level<=Minimax.MAX_LEVEL):
			for i in range_list:
				for j in range_list:
					old_move_buffer=Move(i,j)
					#Genera los movimientos validos para la computadora
					if (tablero_copy.es_duenho(old_move_buffer, Ficha.COMPUTADORA)):
						#move_validos=tablero_copy.get_lista_move_validos(old_move_buffer,-1,Ficha.COMPUTADORA)
						move_validos=tablero_copy.get_lista_move_validos(old_move_buffer,old_move_anterior_buffer,-1,Ficha.COMPUTADORA)
						for move_valido in move_validos:
							#si es que puede come todas las fichas posibles
							lista=tablero_copy.comer_fichas(old_move_buffer)
							#self.nodos=self.nodos+1
							if(len(lista)-1==0):
								#prueba una posicion
								tablero_copy.mover_ficha(old_move_buffer, move_valido)
							#expande el siguiente nodo
							old, move_result=self.min_value_alphabeta(tablero_copy, level+1)
							#evalua el movimiento actual
							#move_valido.score=tablero_copy.evaluar_suma_peso(-1) +move_result.score
							move_valido.score= move_result.score
							'''
							Selecciona el move de menor riesgo para la computadora
							Atender el signo, todavia me confunde
							'''
							if move_valido.score >= mejor_move.score:
								mejor_move=move_valido
								old_move=old_move_buffer
							#pone el tablero en su posicion inicial
							tablero_copy=tablero.get_copia()
					old_move_anterior_buffer=Move(i,j)
		else:
			#mejor_move.score=tablero.evaluar_suma_peso(-1)
			mejor_move.score=tablero.evaluar(-1)
			
		return old_move,mejor_move
		
