from hue import HueLight
from hue import Hue

hue = Hue()
hue.getState()
#hue.setLightState(light=1, on=True, bri=254, sat=254, hue=10000)
hue.getLights()
hue.rgbtocie(255,0,0)
hue.rgbtocie(0,255,0)
hue.rgbtocie(0,0,255)
hue.setLightState(light=1, on=True, xy=hue.rgbtocie(0,0,255))
