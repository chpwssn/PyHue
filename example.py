from hue import Hue

hue = Hue()
hue.getState()
hue.setLightState(light=1, on=True, bri=254, sat=254, hue=10000)