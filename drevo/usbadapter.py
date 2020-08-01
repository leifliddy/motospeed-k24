""" General platform independent USB related hassle """
from abc import ABC
from drevo import keyboard


class Usbadapter(ABC):
    # This is 1 because we're (at the moment) only interested in
    # the interface with id 1. This manages the color-messages.
    rgbinterface = 1
    # Interface 0 yields keypress-interrupts


    
    def write(self, string):
        """ Write is implemented platform specific """
        pass

    def read(self, size):
        """ Read is implemented platform specific """
        pass

    def sendbrightness(self, brightness):
        self.write(bytearray.fromhex('06be150001020d000'+str(brightness)+'000000ff00000000000000000000000000000000000000')) #Brightness, 00 - not powered, 07 - blinking


    def sendhex(self, jsoncolors):
        """
        Send a message with exactly 216 bytes as color message

        Keyword arguments:
        jsoncolors -- Message with the all colors, that needs to be set
        """
        
        header = '06be190001020d'

        #Just send "06be190001020d", then scancodes list (max 5), then colors, separated by 00

        #self.write(bytearray.fromhex('06be140001000dff00000000000ff00000000000ff0000000000000000000000')) #I dunno what is this yet

        count=0
        scancodes=''
        colorstr=''
        for keyname, color in jsoncolors.items():
            scancodes+="%0.2x" % keyboard[keyname] #Just convert HEX value to hex string
            colorstr+=color+'00'
            count+=1
            if count==5:
                self.write(bytearray.fromhex(header+scancodes+colorstr))
                count=0
                scancodes=''
                colorstr=''
        if count!=0: #If amount of items is not multiple of five
            scancodes+='90'*(5-count) #Use 8b, 88, 90, 93 as filers
            colorstr+='00000000'*(5-count)
            self.write(bytearray.fromhex(header+scancodes+colorstr))
        