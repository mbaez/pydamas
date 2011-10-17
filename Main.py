#!/bin/python
import pygame, time
from Damas import *

__author__="mbaez"
__date__ ="$19/10/2010 01:30:19$"

if __name__=="__main__" :
	damas=Damas()
	#print damas.game.tablero
	damas.dibujar_tablero()
	#damas.settings.start_config()
	damas.dibujar_botones()
	quit=False
	clock=pygame.time.Clock()
	init_game=True
	while not quit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				quit = True
				pygame.quit()
			elif event.type == 5:
				index=0 
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if damas.settings_button_rect.collidepoint(mouse_x,mouse_y):
					init_game=damas.settings.start_config()
					#damas=Damas()
					damas.dibujar_tablero()
					damas.dibujar_botones()
					#init_game=False
					
				elif damas.new_game_button_rect.collidepoint(mouse_x,mouse_y):
						damas=Damas()
						damas.dibujar_tablero()
						damas.dibujar_botones()
						init_game=True
				elif init_game:
					for r in damas.tablero_rect:
						i=index//8
						j= index%8
						old_move=Move(i,j)
						if not (damas.game.esta_bloqueada(old_move)) and r.collidepoint(mouse_x, mouse_y):
							x,y = r.center
							if(damas.trace_route(x,y,old_move)):
								#pygame.display.flip()
								index,comer_move=damas.game.juega_computadora()
								for i in range(len(index)-1):
									old_index, new_index=damas.game.traducir_a_index(index[i]),damas.game.traducir_a_index(index[i+1])
									if not (old_index==-1 or new_index==-1):
										ficha_color=damas.obtener_ficha_color(new_index)
										damas.mover_fichas(old_index, new_index, ficha_color)
										for comer in comer_move:
											clock.tick(1)
											damas.dibujar_celda(comer)
											pygame.display.flip()
									else :
										damas.print_text("Fin del Juego "+damas.game.quien_gano(),damas.width//2-100, damas.height-100)
										
								#print damas.game.tablero
							break
						index=index+1
		clock.tick(50)
