#!/usr/bin/python


__author__="mbaez"
__date__ ="$29/10/2010 11:57:19 PM$"
import pygame,time
from pygame import Rect
from String import *
#global TEXT_ID
class TextField:
	TEXT_ID=1
	def __init__(self,screen,focus,label,text,x,y,ancho=200,alto=20):
		self.screen=screen
		self.alto=alto
		self.ancho=ancho
		self.label=label
		self.text=String(text)
		self.rect=self.__dibujar__(x, y)
		self.print_text(30,(0,0,0))
		self.print_text(30,(255,255,255),len(self.label))
		TextField.TEXT_ID=TextField.TEXT_ID+1
		self.id =TextField.TEXT_ID
		self.focus=focus
		
	def is_selected(self,x,y):
		if(self.rect.collidepoint(x,y)):
			self.focus.set_id(self.id)
	def set_label(self, label):
		self.label=label
	def get_focus(self):
		return self.focus.id==self.id
	
	def __dibujar__(self, ptox,ptoy):
		self.x, self.y= ptox, ptoy
		puntos = [(ptox,ptoy),(ptox+self.ancho,ptoy),(ptox+self.ancho,ptoy+self.alto),(ptox,ptoy+self.alto)]
		r=Rect(pygame.draw.polygon(self.screen, (255,255,255), puntos))
		pygame.display.flip()
		return r

	def print_text (self,size=50, color=(255,255,255), label=0):
		pygame.font.init()
		fuente = pygame.font.Font(None, size)
		if(label==0):
			render = fuente.render(self.text.text, 1, color)
			x=0
		else:
			render = fuente.render(self.label, 1, color)
			x=label*10+(label//5)*10
		self.screen.blit(render, (self.x-x, self.y))
		pygame.display.flip()
		
	def set_key_presed(self,key):
		if (key>=pygame.K_0 and key<=pygame.K_9)or(key>=pygame.K_a and key<=pygame.K_z)or key==pygame.K_PERIOD:
			self.text.add(pygame.key.name(key))
		elif key==pygame.K_SPACE:
			self.text.add(" ")
		elif key==pygame.K_BACKSPACE:
			if self.text.pop()==True:
				self.__dibujar__(self.x,self.y)
		self.print_text(30,(0,0,0))

class Focus:
	def __init__(self, id=0):
		self.id=id
	def set_id(self, id):
		print "id", id
		self.id=id
		

print "len", len("hola")
