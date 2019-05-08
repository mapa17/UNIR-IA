# Estado inicial
Mono.posicion = entrada[0]
Mono.altura = Suelo
Mono.Platano = False
Platano.posicion = entrada[1]
Platano.altura = Arriba
Caja.posicion = entrada[2]
Caja.altura = Suelo

# Meta
Meta = tiene(Mono, Platano)

# Operadores
def ir(x,y):
	precondicion: esta(Mono,x) and altura(Mono,Suelo) and distinto(x,y)
	if (precondicion):
		Mono.posicion = y

	efecto: esta(Mono,y) and not esta(Mono,x)
	if (efecto):
		print("ir("+x+","+y+")")

def empujar(b,x,y):
	precondicion: esta(Mono,x) and altura(Mono,Suelo) and esta(b,x) and puedeEmpujar(b) and altura(b,Suelo) and distinto(x,y)
	if (precondicion):
		b = y
		Mono.posicion = y

	efecto: esta(b,y) and esta(Mono,y) and not esta(b,x) and not esta(Mono,x)
	if (efecto):
		print("empujar("+b+","+x+","+y+")")

def subir(x,b):
	precondicion: esta(Mono,x) and altura(Mono,Suelo) and esta(b,x) and puedeSubir(b) and altura(b,Suelo)
	if (precondicion):
		Mono.altura = b

	efecto: altura(Mono,b) and not altura(Mono,Suelo) and altura(Mono,Arriba)
	if (efecto):
		print("subir("+x+","+b+")")

def coger(x,b,h):
	precondicion: esta(Mono,x) and altura(Mono,h) and esta(b,x) and puedeCoger(b) and altura(b,h)
	if (precondicion):
		Mono.Platano = True

	efecto: tiene(Mono,b) and not esta(b,x) and not altura(b,h)
	if (efecto):
		print("coger("+x+","+b+","+h+")")


# Funciones auxiliares
def  esta(a,x):
	return a.posicion == x

def altura(a, h):
	return a.altura == h

def puedeEmpujar(b):
	return esta(Mono,b) and altura(Mono,Suelo)

def puedeSubir(b):
	return esta(Mono,b) and altura(Mono,Suelo)

def distinto(x,y):
	return x != y

def puedeCoger(b):
	return esta(Mono,b) and altura(Mono,Arriba)

def tiene(a,b):
	return Mono.Platano == True