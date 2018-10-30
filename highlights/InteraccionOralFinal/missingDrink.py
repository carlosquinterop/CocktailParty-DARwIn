import cv2
import lightnet
from Cliente import Cliente


class MissingDrink():

	def __init__( self , pPedidos ):
		# Constant values
		self.cameraPort = 0
		self.img_file_path = "data/img.jpg"
		self.boxes = 0
		self.beverage_list = [ 'bottle' , 'vase' , 'cup' , 'wine glass' ]
		self.beverage_dict = { 'person':"persona" , 'bottle':"una gaseosa" , 'cell phone':"celular" , 'vase':"un vaso" , 'cup':"un cafe" , 'wine glass':"un copa de vino"}
		# Variables
		self.pedidos = pPedidos
		self.available_drinks = []
		self.model = lightnet.load('yolo')

	def takeBarPhoto( self ):
		videoCapture = cv2.VideoCapture( self.cameraPort )
		ret, frame = videoCapture.read()
		if ret:
			cv2.imwrite( self.img_file_path , frame )
		videoCapture.release()
		cv2.destroyAllWindows()
		return True
		
	def analyzeImage( self ):
		image = lightnet.Image.from_bytes( open( self.img_file_path , 'rb' ).read() )
		self.boxes = self.model( image )
		print( self.boxes )

	def checkOrder( self ):
		valid_drinks = []
		for identified_object in self.boxes:
			if identified_object[1] in self.beverage_list:
				valid_drinks.append( identified_object[1] )
		print(valid_drinks)
		for beverage in self.beverage_list:
			bev_tuple = ( self.beverage_dict[ beverage ] , valid_drinks.count( beverage ) )
			self.available_drinks.append( bev_tuple )
		print(self.available_drinks)
		for bebida in self.available_drinks:
			available_quantity = bebida[1]
			# Cliente free until this point
			for pedido in self.pedidos:
				if pedido.darEstadoPedido() == 'no esta listo' and pedido.darPedido() == bebida[0] and available_quantity > 0:
					pedido.cambiarEstadoPedido('esta listo')
					available_quantity -= 1
		
		return self.pedidos