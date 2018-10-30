class Cliente:

	def __init__(self, n, p, e):
		self.nombre = n
		self.pedido = p
		self.estadoPedido = e
		self.age = 0
		self.gender = ""
		self.smile = 0
		self.beard = 0
		self.glasses = ""
		self.bald = 0
		self.hairColor = ""
		self.eyeMakeUp = False
		self.lipMakeUp = False
		self.headWear = 0
		self.mustache = 0

	def darNombre(self):
		return self.nombre
	
	def darPedido(self):
		return self.pedido
	
	def darEstadoPedido(self):
		return self.estadoPedido
	
	def cambiarNombre(self, pNombre):
		self.nombre = pNombre
	
	def cambiarPedido(self, pPedido):
		self.pedido = pPedido
	
	def cambiarEstadoPedido(self, pEstadoPedido):
		self.estadoPedido = pEstadoPedido

	def assignAttributes(self, dictionary):
		self.age = dictionary['age']
		self.gender = dictionary['gender']
		self.smile = dictionary['smile']
		self.beard = dictionary['beard']
		self.glasses = dictionary['glasses']
		self.bald = dictionary['bald']
		self.hairColor = dictionary['hairColor']
		self.eyeMakeUp = dictionary['eyeMakeUp']
		self.lipMakeUp = dictionary['lipMakeUp']
		self.headWear = dictionary['headWear']
		self.mustache = dictionary['mustache']

	def giveAge(self):
		return self.age

	def giveGender(self):
		return self.gender

	def giveSmile(self):
		return self.smile

	def giveBeard(self):
		return self.beard

	def giveGlasses(self):
		return self.glasses

	def giveBald(self):
		return self.bald

	def giveHairColor(self):
		return self.hairColor

	def giveEyeMakeUp(self):
		return self.eyeMakeUp

	def giveLipMakeUp(self):
		return self.lipMakeUp

	def giveHeadWear(self):
		return self.headWear
	
	def giveMustache(self):
		return self.mustache