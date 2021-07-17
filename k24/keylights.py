""" Class to control the lights """
from platform import system
from colour import Color
import random, copy
import k24.binding_winbond as binding_winbond


class Keylights:
    """
    see: Keylights.setall() and Keylights.setkey() for practical uses
    """
    vid=0
    pid=0
    def __init__(self):
        self.adapter = binding_winbond.Usblinux()
        self.vid=binding_winbond.vid
        self.pid=binding_winbond.pid
        return


    def gencolorprofile(self, color):
        if not isinstance(color, Color):
            color = Color(color)
        colorstr = color.hex_l[1:]
        return colorstr


    def setall(self, key_color, ambient_color, brightness):
        """
        Sets the color of all keys.
        The color parameter is a colour.Color object
        or alternatively a string interpretable by the colour.Color constructor
        """
        self.adapter.setcolor(self.gencolorprofile(key_color), self.gencolorprofile(ambient_color), brightness)
