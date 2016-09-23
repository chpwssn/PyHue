class HueLight:
	verbose = True
	
	def __init__(self, light_json):
		self.info = light_json
		print(light_json)