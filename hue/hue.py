#/usr/bin/python
import requests,json,os

DEFAULT_CONFIG_FILE="config.json"

class Hue:
	verbose = True
	
	def __init__(self, configFile=DEFAULT_CONFIG_FILE):
		if not os.path.isfile(configFile):
			print("No config file present, can't continue")
			exit(1)
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
	def setLightState(self, light=1, on=None, sat=None, bri=None, hue=None):
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
		print(state)
		r = requests.put("http://{0}/api/{1}/lights/{2}/state".format(self.stationAddress, self.user, light), json = state)
		