#Clase que conteine listas de palabras que el robot valida en cada caso.
#Palabras claves para entender respuestas
class ListasEntendimiento:
	def __init__(self):
		self.listaNombre=["es", "soy", "llamo", "llaman"]
		self.listaPedidos=["un", "una", "dos","tres"]
		self.listaAfirmaciones = ["Sí","sí","correcto","si","Si","Afirmativo","Ciertamente","cierto","verdadero","Cierto", "afirmativo", "ciertamente"]
		self.listaNegaciones = ["No","no","incorrecto","negativo","Negativo", "incierto", "falso", "", " "]
		self.listaBartender = ["Listo","listo","termiando","Terminado","termine", "Termine", "listos", "Listos", "ya", "Ya"]
		self.listaAlternativas = ["quiero", "Quiero", "Dame", "dame", "traeme", "Traeme", "un", "una"]
		self.listaAjustePedido = ["quiero", "Quiero", "Dame", "dame", "traeme", "Traeme", "un", "una", "por", "Por", "favor", "Favor", "gracias", "Gracias", "está", "esta", "bien", "Bien", "Esta", "Está", "y","Y"]
	
	#Retona la lista palabras para identificar el nombre
	def darListaNombres(self):
		return self.listaNombre
	
	#Retona la lista palabras para identificar el pedido
	def darListaPedidos(self):
		return self.listaPedidos
	
	#Retona la lista palabras para considerar una frase afirmativa
	def darListaAfirmaciones(self):
		return self.listaAfirmaciones
	
	#Retona la lista palabras para encontrar una negación
	def darListaNegaciones(self):
		return self.listaNegaciones
	
	#Retona la lista de palbras oara obtener separar la respuesta del bartender
	def darListaBartender(self):
		return self.listaBartender
	
	#Retona la lista para comprender la alternativa del clienteFaltante
	def darListaAlternativas(self):
		return self.listaAlternativas

	def darListaAjustePedido(self):
		return self.listaAjustePedido