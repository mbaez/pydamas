#!/bin/python

__author__="mbaez"
__date__ ="$19/10/2010 01:49:19$"

'''
	La clase que representa el movimiento de jugador
'''
class Move:
	def __init__(self, i=0, j=0, score=0):
		self.i=i
		self.j=j
		self.score=score
	
	def igual(self,move):
		return self.i==move.i and self.j==move.j
	def get_copia(self):
		return Move(self.i ,self.j, self.score)
	def __str__(self):
		return "Move (i="+str(self.i)+",j="+str(self.j)+", score="+str(self.score)+")"
