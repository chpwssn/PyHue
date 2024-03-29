#/usr/bin/python
from hue import HueLight
import requests,json,os

DEFAULT_CONFIG_FILE="config.json"
EXAMPLE_CONFIG_FILE="config.default.json"

class Hue:
	verbose = True
	
	def __init__(self, configFile=DEFAULT_CONFIG_FILE, autoConfig=True):
		if configFile == None or not os.path.isfile(configFile):
			#No config file should we attempt an autoconfiguration?
			if autoConfig:
				#autoconfiguration is enabled, try and read the example so we don't miss any extra config options
				if os.path.isfile(EXAMPLE_CONFIG_FILE):
					with open(EXAMPLE_CONFIG_FILE,"r") as exampleConfigFileObj:
						tmpConfig = json.loads(exampleConfigFileObj.read())
				else:
					tmpConfig = {}
				#Try and get a station address from nupnp
				nupnp = requests.get('https://www.meethue.com/api/nupnp')
				if nupnp.status_code == 200:
					tmpConfig['stationAddress'] = nupnp.json()[0]['internalipaddress']
				else:
					response = input("Could not autodetect Hue station IP address. Can you enter it? [Y/n] ")
					if response == "y" or response == "Y":
						tmpConfig['stationAddress'] = input("Please enter IP address:")
					else:
						print("Cannot configure PyHue")
						exit(2)
				print("Found Hue station at {0}".format(tmpConfig['stationAddress']))
				#ask user for username
				response = input("Do you know the username for your Hue station API? [Y/n]")
				if response == "y" or response == "Y":
					tmpConfig['user'] = input("Please enter username:")
				else:
					#user doesn't know username, prompt them to press button and get username
					response = input("Generating a username, press the button on your Hue station and press enter when ready.")
					r = requests.post("http://{0}/api".format(tmpConfig['stationAddress']), json={"devicetype":"PyHue"})
					tmpConfig['user'] = r.json()[0]['success']['username']
					print("Got username {0}".format(tmpConfig['user']))
				with open(configFile,"w") as writeFile:
					writeFile.write(json.dumps(tmpConfig))
			else:
				if self.verbose:
					print("No config file and autoConfig is disabled.")
					exit(1)
		else:
			#Config file exists, try and load it
			with open(configFile,"r") as configFileObj:
				tmpConfig = json.loads(configFileObj.read())
		self.stationAddress = tmpConfig['stationAddress']
		self.user = tmpConfig['user']
		self.config = True
			
	def getState(self):
		r = requests.get("http://{0}/api/{1}/".format(self.stationAddress,self.user))
		if r.status_code == 200:
			self.state = r.json()
		else:
			if verbose:
				print("Error communicating with hue got HTTP status code: {0}".format(r.status_code))
			self.state = None
		return self.state
			
	#onoff - boolean, sat - int, bri - int, hue - int
	def setLightState(self, light=1, on=None, sat=None, bri=None, hue=None, xy=None):
		if not self.config:
			return
		state = {}
		if not on == None:
			state['on'] = on
		if not sat == None:
			state['sat'] = sat
		if not bri == None:
			state['bri'] = bri
		if not hue == None:
			state['hue'] = hue
		if not xy == None:
			state['xy'] = [xy['x'],xy['y']]
		print(state)
		r = requests.put("http://{0}/api/{1}/lights/{2}/state".format(self.stationAddress, self.user, light), json = state)

	def getLights(self):
		r = requests.get("http://{0}/api/{1}/lights".format(self.stationAddress,self.user))
		light_dict = r.json()
		light_count = len(light_dict.keys())
		light_keys = light_dict.keys()
		for key, value in light_dict.items():
			hl = HueLight(value)
			
	def rgbtocie(self, r, g, b, scale=256):
		try:
			r = r / scale
			g = g / scale
			b = b / scale
			X = 0.4124*r + 0.3576*g + 0.1805*b
			Y = 0.2126*r + 0.7152*g + 0.0722*b
			Z = 0.0193*r + 0.1192*g + 0.9505*b
			x = X / (X + Y + Z)
			y = Y / (X + Y + Z)
			return {"x":x, "y":y}
		except Exception:
			return {"x":0.6400744994567747,"y":0.3299705106316933}