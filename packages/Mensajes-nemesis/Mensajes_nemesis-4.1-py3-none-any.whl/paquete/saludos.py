import numpy as np

# Este es un módulo con funciones que saludan
def saludar():
	print("Hola, te estoy saludando desde la función saludar() del módulo saludos")

def prueba():
	print("Esta es una prueba de la nueva versión 4.1")

def generar_array(numeros):
	return np.arange(numeros)

class Saludo():
	def __init__(self):
		print("Hola, te estoy saludando desde el __init__ de la clase Saludo")

if __name__ == "__main__":
	print(generar_array(5))