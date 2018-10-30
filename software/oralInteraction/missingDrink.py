import cv2
import lightnet
from Cliente import Cliente


class MissingDrink():

	def __init__( self , pPedidos, capture):
		# Constant values
		self.videoCapture = capture
		self.cameraPort = 0
		self.img_file_path = "data/img.jpg"
		self.boxes = 0
		self.beverage_list = [ 'bottle' , 'vase' , 'cup' , 'wine glass' ]
		self.beverage_dict = { 	'person':["persona"], \
								'bottle':["gaseosa", "cerveza"] , \
								'cell phone':["celular"], \
								'vase':["agua"] , \
								'cup':["cafe","café","tinto","te","té"] , \
								'wine glass':["copa de vino","vino"]}
		# Variables
		self.pedidos = pPedidos
		self.available_drinks = []
		self.model = lightnet.load('yolo')

	def takeBarPhoto( self ):
		# videoCapture = cv2.VideoCapture( self.cameraPort )
		# videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		# videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
		# videoCapture.set(cv2.CAP_PROP_FPS, 10)
		for i in range(0, 10):
			ret, frame = self.videoCapture.read()
		frame = frame[115:600, 320:960]
		frame = cv2.flip(frame,0)
		frame = cv2.flip(frame,1)
		if ret:
			cv2.imwrite( self.img_file_path , frame )
		# videoCapture.release()
		# cv2.destroyAllWindows()
		return True

	def analyzeImage( self ):
		image = lightnet.Image.from_bytes( open( self.img_file_path , 'rb' ).read() )
		self.boxes = self.model( image )
		print( self.boxes )

	def checkOrder( self ):
		valid_drinks = []
		self.available_drinks = []
		for identified_object in self.boxes:
			if identified_object[1] in self.beverage_list:
				valid_drinks.append( identified_object[1] )
		print(valid_drinks)
		for beverage in self.beverage_list:
			bev_tuple = ( self.beverage_dict[ beverage ] , valid_drinks.count( beverage ) )
			self.available_drinks.append( bev_tuple )
		print(self.available_drinks)
		for i_bebida in range(len(self.available_drinks)):
			# Cliente free until this point
			drink = list(self.available_drinks[i_bebida])
			for i_pedido in range(len(self.pedidos)):
				inOrder = False
				for d in drink[0]:
					if d in self.pedidos[i_pedido].darPedido():
						inOrder = True
						break
				if (self.pedidos[i_pedido].darEstadoPedido() == 'no esta listo') \
						and inOrder and (drink[1] > 0):
					self.pedidos[i_pedido].cambiarEstadoPedido('esta listo')
					drink[1] -= 1
					self.available_drinks[i_bebida] = drink
		return self.pedidos

	# def checkOrder( self ):
	# 	valid_drinks = []
	# 	for identified_object in self.boxes:
	# 		if identified_object[1] in self.beverage_list:
	# 			valid_drinks.append( identified_object[1] )
	# 	print(valid_drinks)
	# 	for beverage in self.beverage_list:
	# 		bev_tuple = ( self.beverage_dict[ beverage ] , valid_drinks.count( beverage ) )
	# 		self.available_drinks.append( bev_tuple )
	# 	print(self.available_drinks)
	# 	for bebida in self.available_drinks:
	# 		available_quantity = bebida[1]
	# 		# Cliente free until this point
	# 		for pedido in self.pedidos:
	# 			if pedido.darEstadoPedido() == 'no esta listo' and pedido.darPedido() == bebida[0] and available_quantity > 0:
	# 				pedido.cambiarEstadoPedido('esta listo')
	# 				available_quantity -= 1
	#
	# 	return self.pedidos
