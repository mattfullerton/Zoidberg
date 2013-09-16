class CallABikeStation:
	def __init__(self, longitude, latitude, isOutside):
		self.longitude = longitude
		self.latitude  = latitude
		self.isOutside = isOutside
		
	def out(self):
		return str(self.latitude) + "," + str(self.longitude) + "," + str(self.isOutside)