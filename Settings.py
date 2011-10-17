#!/bin/python
import pygame, time
from Game import *
from TextField import *

__author__="mbaez"
__date__ ="$29/10/2010 08:17:10$"

'''
	La clase que manipula la intefaz grafica de las configuraciones
'''
class Settings:
	def __init__(self, screen,fondo,width,height):
		self.screen=screen
		self.width, self.height=width,height
		self.fondo=fondo
		self.new_game_rect=None


	'''
	Reutilizamos codigo de la clase Damas.py
	'''
	def set_gui_fuctions(self, cargar_imagen, dibujar_imagen,print_text):
		self.cargar_imagen=cargar_imagen
		self.dibujar_imagen=dibujar_imagen
		self.print_text=print_text

	def set_ia_game(self, game):
		self.game=game

	def __init_settings__(self):
		self.dibujar_imagen(self.fondo, self.width//2,self.height//2)

		self.focus=Focus()
		y=self.height//2+50
		x=self.width//2
		dy=40
		self.print_text("Parametros de los Algoritmos",x-150, y-dy)
		level=str(self.game.minimax.MAX_LEVEL)
		self.nivel_textField=TextField(self.screen,self.focus, "Max Level:  ",level,220,y)
		peso_dama=str(self.game.tablero.peso_dama)
		self.peso_dama_textField=TextField(self.screen,self.focus,"Peso Dama:  ",peso_dama,220,y+dy)
		peso_normal=str(self.game.tablero.peso_normal)
		self.peso_normal_textField=TextField(self.screen,self.focus,"Peso Normal:",peso_normal,220,y+2*dy)
		y=100
		dy=50
		self.print_text("Algoritmos de busqueda",x-120,y+dy)
		self.minimax_button=self.cargar_imagen("img/minimax.png")
		self.minimax_button_rect=self.dibujar_imagen(self.minimax_button, x-100,y+2*dy)

		self.alpha_beta_button=self.cargar_imagen("img/alpha_beta.png")
		self.alpha_beta_button_rect=self.dibujar_imagen(self.alpha_beta_button,x+100,y+2*dy)

		self.print_text("Funciones de Evaluacion",x-120, y+3*dy)
		self.eval_suma_peso_button=self.cargar_imagen("img/suma_peso.png")
		self.eval_suma_peso_button_rect=self.dibujar_imagen(self.eval_suma_peso_button,x+100,y+4*dy)

		self.eval_suma_button=self.cargar_imagen("img/suma.png",)
		self.eval_suma_button_rect=self.dibujar_imagen(self.eval_suma_button,x-100,y+4*dy)

		self.button_clicked=self.cargar_imagen("img/button_clicked.png")

		pygame.display.flip()


	'''
		metodos que tienen que ver con el formulario a completar
	'''

	def printText(self,str,i,j,size=50, color=(255,255,255)):
		pygame.font.init()
		fuente = pygame.font.Font(None, size)
		texto = fuente.render(str, 1, color)
		self.screen.blit(texto, (i, j))
		pygame.display.flip()
	'''
		Fin de metodos de formulario
	'''
	def set_clicked(self,eval_suma_focus, minimax_focus):
		x_suma,y_suma=self.eval_suma_button_rect.center
		self.dibujar_imagen(self.eval_suma_button,x_suma,y_suma)

		x_peso,y_peso=self.eval_suma_peso_button_rect.center
		self.dibujar_imagen(self.eval_suma_peso_button,x_peso,y_peso)

		x_mini,y_mini=self.minimax_button_rect.center
		self.dibujar_imagen(self.minimax_button,x_mini,y_mini)

		x_poda,y_poda=self.alpha_beta_button_rect.center
		self.dibujar_imagen(self.alpha_beta_button,x_poda,y_poda)

		if(eval_suma_focus):
			self.dibujar_imagen(self.button_clicked,x_suma,y_suma)
		else:
			self.dibujar_imagen(self.button_clicked,x_peso,y_peso)
		if minimax_focus:
			self.dibujar_imagen(self.button_clicked,x_mini,y_mini)
		else:
			self.dibujar_imagen(self.button_clicked,x_poda,y_poda)
		pygame.display.flip()

	def start_config(self):
		clock=pygame.time.Clock()
		self.__init_settings__()
		minimax_function=Minimax()
		tablero_function=Tablero()
		minimax_focus=True
		eval_suma_focus=False
		self.set_clicked(eval_suma_focus, minimax_focus)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit = True
					pygame.quit()
				#Se hizo click
				elif event.type == 5:
					mouse_x, mouse_y = pygame.mouse.get_pos()
					self.nivel_textField.is_selected(mouse_x, mouse_y)
					self.peso_dama_textField.is_selected(mouse_x, mouse_y)
					self.peso_normal_textField.is_selected(mouse_x, mouse_y)

					if(self.minimax_button_rect.collidepoint(mouse_x, mouse_y)):
						self.game.minimax.start=minimax_function.minimax
						print "minimax"
						minimax_focus=True
					elif(self.alpha_beta_button_rect.collidepoint(mouse_x, mouse_y)):
						self.game.minimax.start=minimax_function.minimax_alpha_beta
						minimax_focus=False
					elif(self.eval_suma_peso_button_rect.collidepoint(mouse_x, mouse_y)):
						self.game.tablero.start=tablero_function.evaluar_suma_peso
						eval_suma_focus=False

					elif(self.eval_suma_button_rect.collidepoint(mouse_x, mouse_y)):
						self.game.tablero.start=tablero_function.evaluar_suma
						eval_suma_focus=True
					#al juego
					elif self.new_game_rect.collidepoint(mouse_x, mouse_y):
						self.game.minimax.MAX_LEVEL= int(self.nivel_textField.text.text)
						self.game.tablero.peso_dama=int(self.peso_dama_textField.text.text)
						self.game.tablero.peso_normal=int(self.peso_normal_textField.text.text)

						return True
					self.set_clicked(eval_suma_focus, minimax_focus)

				elif event.type== pygame.KEYDOWN:
					key=event.key
					if(self.nivel_textField.get_focus()):
						self.nivel_textField.set_key_presed(key)
					elif self.peso_dama_textField.get_focus():
						self.peso_dama_textField.set_key_presed(key)
					elif self.peso_normal_textField.get_focus():
						self.peso_normal_textField.set_key_presed(key)
			clock.tick(50)

