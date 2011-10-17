#!/bin/python
import pygame, time
from Game import *
from Settings import *

__author__="mbaez"
__date__ ="$19/10/2010 01:25:19$"

'''
	La clase que manipula la intefaz grafica
'''
class Damas:
	def __init__(self):
		self.width, self.height=600, 700
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		#se cargan las imagenes de las fichas
		self.ficha_negra=self.cargar_imagen("img/ficha_negra.png")
		self.ficha_blanca=self.cargar_imagen("img/ficha_blanca.png")
		self.ficha_dama_negra=self.cargar_imagen("img/dama_negra.png")
		self.ficha_dama_blanca=self.cargar_imagen("img/dama_blanca.png")
		#Se cargan las imagenes de las celdas
		self.celda_negra=self.cargar_imagen("img/celda_negra.png")
		self.celda_blanca=self.cargar_imagen("img/celda_blanca.png")
		self.celda_selecionada= self.cargar_imagen("img/ficha_seleccionada.png")
		#se cargan las imagenes de los botones
		self.cancel_button= self.cargar_imagen("img/cancel.png")
		self.ok_button=self.cargar_imagen("img/aceptar.png")
		self.button_clicked=self.cargar_imagen("img/clicked.png")

		self.new_game_button=self.cargar_imagen("img/new_game.png")
		self.settings_button=self.cargar_imagen("img/settings.png")
		#carga la imagen de fondo
		self.fondo=self.cargar_imagen("img/fondo.png")
		self.toolbar=self.cargar_imagen("img/fondo_toolbar.png")
		pygame.display.set_caption("Damas")

		'''
		se instancia la interfaz de comunicacion con la inteligencia artificial
		'''
		self.game=Game()
		self.settings=Settings(self.screen,self.fondo,self.width,self.height)
		self.settings.set_ia_game(self.game)
		self.settings.set_gui_fuctions(self.cargar_imagen, self.dibujar_imagen,self.print_text)


	'''
	Dada la url de una imagen, carga la misma y establece el centro como x e y
	'''
	def cargar_imagen(self, url,x=0, y=0):
		picture=pygame.image.load(url)
		rect=picture.get_rect()
		rect.center=(x,y)
		return picture

	def print_text (self,text,x,y, size=30, color=(255,255,255)):
		pygame.font.init()
		fuente = pygame.font.Font(None, size)
		render = fuente.render(text, 1, color)
		self.screen.blit(render, (x, y))
		pygame.display.flip()
	'''
	Dibuja la celda del tablero
	'''
	def dibujar_imagen(self,picture ,x, y):
		rect=picture.get_rect()
		rect.center=(x,y);
		self.screen.blit(picture, rect)
		return rect
	'''
	Dibuja los botones ok y cancel
	'''
	def dibujar_botones(self):
		y=self.height-90
		x=self.width//2
		self.ok_button_rect=self.dibujar_imagen(self.ok_button, x-52,y)
		self.cancel_button_rect= self.dibujar_imagen(self.cancel_button, x+52,y)

		self.new_game_button_rect=self.dibujar_imagen(self.new_game_button, x-52,50)
		self.settings.new_game_rect=self.new_game_button_rect
		self.settings_button_rect=self.dibujar_imagen(self.settings_button, x+52,50)
		pygame.display.flip()

	'''
	Dibuja el tablero principal e inializa el tablero.
	'''
	def dibujar_tablero(self):
		self.dibujar_imagen(self.fondo, self.width//2,self.height//2)
		self.dibujar_imagen(self.toolbar, self.width//2,41)
		delta=59
		y=self.height//2 -delta*3-delta//2+3
		self.tablero_rect=[]
		indice=0
		for i in range(Tablero.MAX_DIM):
			x=self.width//2 -delta*3-delta//2
			for j in range(Tablero.MAX_DIM):
				if(self.game.tablero.casillas[i][j].duenho==Ficha.BLOQUEADA):
					rect=self.dibujar_imagen(self.celda_blanca, x, y)
				else:
					rect=self.dibujar_imagen(self.celda_negra, x, y)
					if(self.game.tablero.casillas[i][j].duenho==Ficha.USUARIO):
						self.dibujar_imagen(self.ficha_negra, x,y)

					elif (self.game.tablero.casillas[i][j].duenho==Ficha.COMPUTADORA):
						self.dibujar_imagen(self.ficha_blanca, x,y)

				self.tablero_rect.append(rect)
				x=x+delta
				indice=indice+1
			indice=indice-1
			y=y+delta-1
		pygame.display.flip()

	'''
	Traduce un indice a coordenadas i,j de la matriz
	'''
	def traducir_a_move(self, index):
		i=index//8
		j=index%8
		return Move(i,j)

	def traducir_a_index(self, move):
		return move.i*8+move.j%8
	'''
	trace route posee su propio bulce de eventos debido a que cuando se selecciona una ficha
	se debe esperar por la nueva posicion de la ficha nueva (mover fichas) y asi trazar su ruta.
	Traza el camino de las casillas que son seleccionadas hasta que se presione ok o cancel
	'''
	def trace_route(self, x,y, old_move):
		clock=pygame.time.Clock()
		route_list=[]
		route_casillas_list=[]
		#se inicializa el buffer de los movimientos
		move_buffer=old_move
		route_list.append(old_move)
		#Se pinta la casilla como seleccionada si esta no esta vacia
		if(self.game.ocupe_casilla(old_move)):
			ficha_color=self.obtener_ficha_color(self.traducir_a_index(old_move))
			self.dibujar_imagen(self.celda_selecionada,x,y)
			self.dibujar_imagen(ficha_color,x,y)
			pygame.display.flip()
		else:
			return False

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit = True
					pygame.quit()
				#Se hizo click
				elif event.type == 5:
					index=0
					mouse_x, mouse_y = pygame.mouse.get_pos()
					#Se verifica si ser realizo click en el tablero
					for r in self.tablero_rect:
						#traduce a coordenadas
						new_move=self.traducir_a_move(index)
						#verifica si se selecciono la casilla y si esta disponible
						if (r.collidepoint(mouse_x, mouse_y) and not self.game.esta_bloqueada(new_move)):
							#chequea si el movimiento acutal es permitido
							if(self.game.route_valido(move_buffer,new_move) ):
								x_new,y_new = r.center
								move_buffer=new_move
								#Anhade a la lista de move realizados el move acutal
								route_list.append(new_move)
								#Anhade a la lista de coordenadas asociadas a los move la coordenada actual
								route_casillas_list.append(r.center)
								#Marca como seleccionada la celda actual
								self.dibujar_imagen(self.celda_selecionada,x_new,y_new)
								pygame.display.flip()
						index=index+1

					#Si se selecciono el boton de cancelar
					if( self.cancel_button_rect.collidepoint(mouse_x,mouse_y)):
						#Marca el boton para indicar que este fue seleccionado
						x_click,y_click=self.cancel_button_rect.center
						self.dibujar_imagen(self.button_clicked,x_click,y_click)
						pygame.display.flip()
						#Actualiza la ficha inicial dado que esta ya no esta seleccionada
						self.dibujar_imagen(self.celda_negra, x,y)
						ficha_color=self.obtener_ficha_color(self.traducir_a_index(old_move))
						self.dibujar_imagen(ficha_color, x,y)
						#Recorre la lista de coordenadas asociadas a los move y acutaliza su estado
						for punto in route_casillas_list:
							__x,__y=punto
							#Pone el tablero a su estado anterio
							self.dibujar_imagen(self.celda_negra,__x,__y)
						#Se pone el boton en su estado normal
						clock.tick(5)
						self.dibujar_imagen(self.cancel_button,x_click,y_click)
						pygame.display.flip()
						return False

					elif( self.ok_button_rect.collidepoint(mouse_x,mouse_y)):
						__x,__y=x,y
						#Marca el boton para indicar que este fue seleccionado
						x_click,y_click=self.ok_button_rect.center
						self.dibujar_imagen(self.button_clicked,x_click,y_click)

						#si se selecciona una ficha y luego se da ok, para que acutalice a su estado normal
						if(len(route_list)-1==0):
							ficha_color=self.obtener_ficha_color(self.traducir_a_index(old_move))
							self.dibujar_celda_ficha(ficha_color,__x,__y)
							self.dibujar_imagen(self.ok_button,x_click,y_click)
							pygame.display.flip()
							return False

						#Recorre la lista de move y verifica que el camino sea correcto
						for i in range(len(route_list)-1):
							#Trata de realizar el movimiento si este no esta permitido, no lo realizara
							mover_index=self.game.realizar_movimiento(route_list[i],route_list[i+1])
							if not (mover_index==False):
									#obtiene las coordenadas actuales
									x_new,y_new = route_casillas_list[i]
									#actualiza el estado de la celda anterior
									self.dibujar_imagen(self.celda_negra,__x,__y)
									#actualiza el estado de la celda actual
									ficha_color=self.obtener_ficha_color(self.traducir_a_index(route_list[i+1]))
									self.dibujar_celda_ficha(ficha_color,x_new,y_new)
									pygame.display.flip()
									#Ahora __x e __y pasan a ser la posicion actual
									__x,__y=route_casillas_list[i]
									#Espera un momento para dar la impresion que la ficha se mueve lentamente
									clock.tick(2)
									#Elimina la ficha que se comio en la jugada
									if not (mover_index==True) :
										pto_x, pto_y= self.tablero_rect[mover_index].center
										self.dibujar_imagen(self.celda_negra,pto_x,pto_y)
										pygame.display.flip()
										clock.tick(2)
						#Se pone el boton en su estado normal
						self.dibujar_imagen(self.ok_button,x_click,y_click)
						return True
			clock.tick(50)

	#dibuja la casilla y la ficha en la posicion x e y
	def dibujar_celda_ficha(self,ficha_color,x,y):
		self.dibujar_imagen(self.celda_negra, x,y)
		self.dibujar_imagen(ficha_color, x,y)

	def dibujar_celda(self, move):
		index=self.traducir_a_index(move)
		x,y =self.tablero_rect[index].center
		self.dibujar_imagen(self.celda_negra, x,y)
		pygame.display.flip()
	#Se encarga de mover las fichas y pintar sus respectivas casillas
	def mover_fichas(self, old_index, new_index, ficha_color):
		__x,__y= self.tablero_rect[old_index].center
		self.dibujar_imagen(self.celda_negra,__x,__y)
		#actualiza el estado de la celda actual
		x_new, y_new=self.tablero_rect[new_index].center
		self.dibujar_celda_ficha(ficha_color,x_new,y_new)
		pygame.display.flip()

	def obtener_ficha_color(self,index):
		move=self.traducir_a_move(index)
		if self.game.es_dama_usuario(move):
			return self.ficha_dama_negra
		elif self.game.es_dama_computadora(move):
			return self.ficha_dama_blanca
		elif self.game.es_ficha_usuario(move):
			return self.ficha_negra
		#self.game.es_ficha_computadora(move):
		return self.ficha_blanca

