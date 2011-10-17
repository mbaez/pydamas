from Ficha import *
from Move import *

__author__="mbaez"
__date__ ="$19/10/2010 01:42:19$"

'''
	La clase que representa el tablero.
'''
class Tablero:
	MAX_DIM=8

	def __init__(self, evaluar_function=None):
		self.evaluar=evaluar_function
		self.casillas=[]
		self.__init_tablero__();
		self.peso_dama=3
		self.peso_normal=1


	def __init_tablero__(self):
		indice=0
		for i in range(Tablero.MAX_DIM):
			self.casillas.append([])
			for j in range (Tablero.MAX_DIM):
				if indice%2==0:
					#Las casillas blancas se bloquean para que no se agregen fichas sobre estas.
					self.casillas[i].append(Ficha(Ficha.NORMAL, Ficha.PESO_NORMAL,Ficha.BLOQUEADA));
				else:
					self.casillas[i].append(Ficha());
				indice=indice+1
			indice=indice-1

	def get_copia(self):
		copy=Tablero(self.evaluar)
		for i in range(Tablero.MAX_DIM):
			for j in range(Tablero.MAX_DIM):
				copy.casillas[i][j]=self.casillas[i][j].get_copia()
		return copy

	def crear_dama(self, move, duenho=Ficha.USUARIO):
		self.casillas[move.i][move.j]=Ficha(Ficha.DAMA,Ficha.PESO_DAMA,duenho)
	'''
	Carga las 24 fichas de los jugadores, 12 por cada una
	'''
	def cargar_fichas(self):
		#Carga las 12 fichas para los jugadores.
		#'''
		for i in range(3):
			for casilla in self.casillas[i]:
				if not (casilla.duenho == Ficha.BLOQUEADA) :
					casilla.duenho=Ficha.USUARIO
			for casilla in self.casillas[Tablero.MAX_DIM-i-1]:
				if not (casilla.duenho == Ficha.BLOQUEADA) :
					casilla.duenho=Ficha.COMPUTADORA

		'''
		self.casillas[6][5].duenho=Ficha.COMPUTADORA
		self.crear_dama(Move(6,5), Ficha.COMPUTADORA)
		self.casillas[5][6].duenho=Ficha.USUARIO
		#self.crear_dama(Move(6,1))
		self.casillas[3][6].duenho=Ficha.USUARIO
		self.casillas[6][1].duenho=Ficha.USUARIO
		'''
	'''
	Se deben definir e identificar muy bien la zona del usuario y de la computadora
	El usuario humano se encuentra en las primeras 12 casillas habilitadas(U) y la computadora
	el las ultimas 12(C).
	__________________________
	|[#][U][#][U][#][U][#][U]|
	|[U][#][U][#][U][#][U][#]|
	|[#][U][#][U][#][U][#][U]|
	|[ ][#][ ][#][ ][#][ ][#]|
	|[#][ ][#][ ][#][ ][#][ ]|
	|[C][#][C][#][C][#][C][#]|
	|[#][C][#][C][#][C][#][C]|
	|[C][#][C][#][C][#][C][#]|
	``````````````````````````
	Este metodo sencillo retorna true si la jugada correspondiente es dama de acuerdo al duenho del
	movimiento(usuario, computadora).
	'''

	def es_dama(self, move, duenho=Ficha.USUARIO):
		i,j=move.i, move.j
		if self.casillas[i][j].duenho == duenho and duenho==Ficha.USUARIO and (i==7 or self.casillas[i][j].tipo==Ficha.DAMA):
			return True

		elif self.casillas[i][j].duenho == duenho and duenho==Ficha.COMPUTADORA and (i==0 or self.casillas[i][j].tipo==Ficha.DAMA):
			return True
		return False

	def es_vacio(self, i,j):
		return (i <8 and i>=0)  and (j<8 and j>=0) and self.casillas[i][j].duenho==Ficha.VACIA

	def es_valido_move_normal(self, old_move, new_move, signo=1 ,duenho=Ficha.USUARIO):
		i_old, j_old= old_move.i, old_move.j
		i_new, j_new= new_move.i, new_move.j

		if (j_old+1==j_new or j_old-1==j_new) and i_old+1*signo==i_new and self.es_vacio(i_new, j_new) and not self.es_vacio(i_old, j_old):
			return True
		#Movimiento el el que trata de comer una ficha
		if (j_old+2==j_new or j_old-2==j_new) and i_old+2*signo==i_new and self.es_vacio(i_new, j_new) and self.controlar_casilla_anterior(old_move,new_move,signo,duenho) :
			return True
		return False

	def es_valido_move(self, old_move, new_move, signo=1 ,duenho=Ficha.USUARIO):
		'''
		Controla si el movimiento actual sea un movimiento normal
		si es un movimiento que implica comer una ficha
		o si el movimiento implica quedarse en la misma casilla.
		'''
		#si sobrepasa el maximo/minimo valor del indice retorna false
		if(self.sobrepasa_limites(new_move) or self.es_duenho(new_move,Ficha.BLOQUEADA) or old_move.igual(new_move)):
			return False

		elif self.es_dama(old_move,duenho):
			#tablero_copy=self.get_copia()
			return self.es_valido_move_dama2(old_move,new_move,signo,duenho)

		return self.es_valido_move_normal(old_move, new_move, signo, duenho)

	def es_duenho(self, move, duenho=Ficha.USUARIO):
		return self.casillas[move.i][move.j].duenho==duenho

	def get_pos_ficha_anterior(self, old_move, new_move, inc=1):
		delta_i=new_move.i-old_move.i
		delta_j=new_move.j-old_move.j
		if(delta_i==0 or delta_j==0) or self.sobrepasa_limites(old_move) or self.sobrepasa_limites(new_move):
			return None
		signo_i=(delta_i/abs(delta_i))*-1
		signo_j=(delta_j/abs(delta_j))*-1
		dj,di=abs(inc),abs(inc)
		i, j=new_move.i,new_move.j
		resul=Move(i+di*signo_i,j+di*signo_j)
		if(self.sobrepasa_limites(resul)):
			return None
		return  resul

	def sobrepasa_limites(self,move):
		if (move.i>=0 and move.i<8 and move.j>=0 and move.j<8):
			return False
		return True

	'''
	debe controlar el movimiento que puede realizar la dama
	'''
	def es_valido_move_dama2(self,old_move,new_move,inc=1,duenho=Ficha.USUARIO):
		delta_i=new_move.i-old_move.i
		delta_j=new_move.j-old_move.j
		i, j=old_move.i,old_move.j
		if not (abs(delta_i)==abs(delta_j)) or delta_i==0 or delta_j==0:
			return False

		signo_j=delta_j/abs(delta_j)
		signo_i= delta_i/abs(delta_i)
		move_buffer=Move(i,j)
		for di in range(1, abs(delta_i)+1):
			#se obtiene el siguiente movimiento
			actual_move=Move(i+di*signo_i,j+di*signo_j)
			#se verifica que este no este fuera del rango 0-8 y que no este ocupado por alguna ficha
			if not self.sobrepasa_limites(actual_move) and not (self.es_vacio(actual_move.i,actual_move.j)) and self.es_duenho(actual_move,duenho):
				return False
			#se verifica que no se sobrepase el rango 0-8 y que no este vacio para verificar si se puede comer alguna ficha
			elif not self.sobrepasa_limites(actual_move) and not self.es_duenho(actual_move,duenho) and not (self.es_vacio(actual_move.i,actual_move.j)):
				di=di+1
				#Se obtiene el siguiente movimiento y se verifica
				actual_move=Move(i+(di)*signo_i,j+(di)*signo_j)
				if(self.sobrepasa_limites(actual_move) or not (actual_move.igual(new_move))):
					return False
				#Se mueve la ficha a la posicion anterior a la casilla ocupada
				comer_move=self.comer_ficha(old_move, actual_move,signo_i, duenho)
				if(comer_move==None):
					return False
				return True

			move_buffer=actual_move
		return True

	'''
	Controla los movimientos en los que implica comer una ficha, busca la posicion de la ficha que se comio en la jugada
	'''
	def comer_ficha(self, old_move, new_move,signo=1,duenho=Ficha.USUARIO):
		i_old, j_old= old_move.i, old_move.j
		i_new, j_new= new_move.i, new_move.j
		#verifica si puede hacer el salto
		move=None
		delta=2
		if(old_move.igual(new_move)):
			return None
		delta=abs(new_move.i-old_move.i)-2
		if(self.es_dama(old_move,duenho) and not delta==0):
			signo=self.get_signo(old_move,new_move)
			move=self.get_pos_ficha_anterior(old_move,new_move,2)
			if(move==None):
				return None
			self.mover_ficha(move,old_move)
			i_old, j_old= move.i, move.j

		if (self.es_vacio(i_new, j_new) and self.controlar_casilla_anterior(Move(i_old, j_old),new_move,signo,duenho) and not self.es_vacio(i_old, j_old)):
			#Busca cual fue la casilla anterior
			if(not move==None):
				self.mover_ficha(old_move,move)

			if(j_old+2==j_new  and i_old+2*signo==i_new):
				return Move(i_old+1*signo,j_old+1)
			elif (j_old-2==j_new and i_old+2*signo==i_new):
				return Move(i_old+1*signo,j_old-1)
			else :
				return None
		if(not move==None):
			self.mover_ficha(old_move,move)
		return None

	'''
	Verifica que si la casilla anterior al un nuevo movimiento esta vacia
	'''
	def controlar_casilla_anterior(self,old_move,new_move, signo=1,duenho=Ficha.USUARIO):
		move_ant=self.get_pos_ficha_anterior(old_move,new_move,signo)
		if(not move_ant==None and not self.es_duenho(move_ant,duenho) and not self.es_vacio(move_ant.i,move_ant.j) and self.es_vacio(new_move.i, new_move.j)):
			return True
		return False

	'''
	Calcula el valor de una jugada teniendo en cuenta el peso y la cantidad de fichas
	'''
	def evaluar_suma_peso(self, signo=1):

		n_propias, d_propias, n_contrario, d_contrario=self.contar_fichas();
		return signo*(n_propias-n_contrario)*self.peso_normal + signo*(d_propias-d_contrario)*self.peso_dama

	'''
	Calcula el valor de una jugada teniendo en cuenta la cantidad de fichas
	'''
	def evaluar_suma(self, signo=1):
		n_propias, d_propias, n_contrario, d_contrario=self.contar_fichas();
		return signo*(n_propias-n_contrario) + signo*(d_propias-d_contrario)

	'''
		retorna la suma de todas las fichas normales y damas por el duenho del usuario
			fichas_propias_normal
			fichas_propias_damas
			fichas_contrario_normal
			fichas_contrario_damas
	'''
	def contar_fichas(self):
		sum_fichas_propias_normal=0
		sum_fichas_contrario_normal=0
		sum_fichas_propias_damas=0
		sum_fichas_contrario_damas=0
		for i in range(self.MAX_DIM):
			for j in range(self.MAX_DIM):
				ficha=self.casillas[i][j]
				if(ficha.duenho==Ficha.USUARIO):
					if ficha.tipo==Ficha.DAMA :
						sum_fichas_propias_damas=sum_fichas_propias_damas+1
					else:
						sum_fichas_propias_normal=sum_fichas_propias_normal+1

				elif (ficha.duenho==Ficha.COMPUTADORA):
					if ficha.tipo==Ficha.DAMA :
						sum_fichas_contrario_damas=sum_fichas_contrario_damas+1
					else:
						sum_fichas_contrario_normal=sum_fichas_contrario_normal+1

		return sum_fichas_propias_normal,sum_fichas_propias_damas,sum_fichas_contrario_normal,sum_fichas_contrario_damas

	'''
	Realiza un swap entre las fichas
	'''
	def mover_ficha(self,old_move,new_move):
		if(self.sobrepasa_limites(new_move) or self.sobrepasa_limites(old_move)):
			return None
		ficha=self.casillas[new_move.i][new_move.j]
		self.casillas[new_move.i][new_move.j]=self.casillas[old_move.i][old_move.j]
		self.casillas[old_move.i][old_move.j]=ficha

	'''
	Anhade a la lista de movimientos validos el new_move si este esta permitido
	'''
	def anhadir_move_valido(self,move, anterior,new_move,inc=1,duenho=Ficha.USUARIO):
		if(self.es_valido_move(move,new_move,inc,duenho) and not anterior.igual(new_move)):
			self.validos.append(new_move.get_copia())

	def eliminar_ficha(self, move):
		self.casillas[move.i][move.j]=Ficha()
	'''
	Genera una lista de todos los movimientos valido para una ficha que se encuentra
	en la posion move
	'''
	def get_lista_move_validos(self,move,anterior,inc=1,duenho=Ficha.USUARIO, limit_start=1):
		self.validos=[]
		#si el inc es negativo se tiene que decermentar, para la busqueda hacia abajo
		inc_increment=inc
		dj=1
		inc_increment= inc/abs(inc)
		if limit_start==0:
			dj=abs(inc)
		#si es dama el abs(inc_limite) es mayor a 2 porque tiene que analizar las diagonales
		inc_limit=abs(inc)+limit_start
		i, j=move.i,move.j
		while (abs(inc)<=abs(inc_limit) and dj<=8):
			#se verican las posisiones hacia adelante
			new_move=Move(i+inc,j+dj)
			#print new_move
			self.anhadir_move_valido(move,anterior,new_move,inc_increment,duenho)
			new_move=Move(i+inc,j-dj)
			#print new_move
			self.anhadir_move_valido(move,anterior,new_move,inc_increment,duenho)
			if(self.casillas[move.i][move.j].tipo==Ficha.DAMA):
				#como es dama se incrementa el limite
				inc_limit=11
				#se verifican las posiciones de atras
				new_move=Move(i-inc,j-dj)
				#print new_move
				self.anhadir_move_valido(move,anterior,new_move,-inc_increment,duenho)
				new_move=Move(i-inc,j+dj)
				#print new_move
				self.anhadir_move_valido(move,anterior,new_move,-inc_increment,duenho)
			#se incrementa el inc
			inc=inc+inc_increment
			#se increnta el delta de j
			dj=dj+1
		return self.validos

	'''
	Verifica si es el fin del juego, de momento se considerea que el juego termina cuando
	uno de los jugadores se queda sin fichas.
	'''
	def fin_del_juego(self):
		n_propias, d_propias, n_contrario, d_contrario=self.contar_fichas();
		if((n_propias+d_propias)==0 or (n_contrario+ d_contrario)==0):
			print "fin del juego :("
			return True
		return False

	'''
	Come todas las fichas que puede teniedo en cuenta la cantidad
	'''
	def comer_fichas(self, move, inc=-1, duenho=Ficha.COMPUTADORA):
		limit_start=1
		if(self.es_dama(move, duenho)):
			limit_start=0
		tablero_copia=self.get_copia()
		lista, max=tablero_copia.__puedo_comer__(move,Move(-1,-1),0,inc,duenho,limit_start)
		lista_comidos=[]
		signo=inc

		for move_valido in lista:
			if self.es_dama(move, duenho):
				signo=self.get_signo(move,move_valido)

			comer_move=self.get_pos_ficha_anterior(move,move_valido,signo)
			if(not comer_move==None):
				self.mover_ficha(move, move_valido)
				self.eliminar_ficha(comer_move)
				lista_comidos.append(comer_move)
			move=move_valido

		return lista, lista_comidos

	def  get_signo(self, old_move, new_move):
		delta_i=new_move.i-old_move.i
		if(delta_i==0):
			return 1
		return (delta_i/abs(delta_i))

	def __puedo_comer__(self, move,anterior,contador, inc=-1, duenho=Ficha.COMPUTADORA, limit_start=1):
		lista_validos=[]
		if(not self.fin_del_juego() and contador < 5):
			#print "hola"
			lista_validos=self.get_lista_move_validos(move, Move(-1,-1), inc,duenho,limit_start)
		mejor=contador
		lista_move=[]
		lista_move.append(move)
		signo=inc
		buffer=move
		for valido in lista_validos:
			if self.es_dama(move, duenho):
				signo=self.get_signo(move,valido)

			comer_move=self.comer_ficha(move, valido, signo, Ficha.COMPUTADORA)
			bkp=self.casillas[move.i][move.j].duenho
			self.casillas[buffer.i][buffer.j].duenho=Ficha.BLOQUEADA
			print self
			if(not comer_move==None):
				self.mover_ficha(valido, move)
				lista,result=self.__puedo_comer__(valido, move, contador+1, inc,duenho)
				if(result>mejor):
					mejor=result
					for l in lista:
						lista_move.append(l)
				self.casillas[buffer.i][buffer.j].duenho=bkp
				self.mover_ficha(valido, move)
			buffer=valido
		return lista_move, mejor

	'''
	Metodo llamado para crear una cadena de texto que represente a nuestro objeto.
	Se utiliza cuando usamos print para mostrar nuestro objeto o cuando usamos la
	funcion str(obj) para crear una cadena a partir de nuestro objeto.
	'''
	def __str__(self):
		str=""
		for i in range(Tablero.MAX_DIM):
			for casilla in self.casillas[i]:
				str=str+"|"+casilla.__str__()
			str=str+"\n"
		return str


if __name__=="__main__":
	print "testing "
	table=Tablero()
	table.cargar_fichas()
	print table
	aux=table.comer_fichas(Move(6,5),-1)
	for i in aux:
		if len(i)>0:
			print "-> ",i[0]
	print table
