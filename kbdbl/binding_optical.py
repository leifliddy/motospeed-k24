""" Linux related implementation of USB code """
import usb.core
import usb.util
from operator import itemgetter

def isPresented():
    dev = usb.core.find(
        idVendor=0x2ea8,  # Noname
        idProduct=0x2125  # Gaming Keyboard
    )
    if dev is not None:
        return(True)


class Usblinux():
    """ Class that implements Linux specific USB handling """
    rgbinterface = 1
    keyboard={"ESC" : 0x80, "F1" : 0x82, "F2" : 0x83, "F3" : 0x84, "F4" : 0x85, "F5" : 0x86, "F6" : 0x87, "F7" : 0x88, "F8" : 0x89, "F9" : 0x8a, "F10" : 0x8b, "F11" : 0x8c, "F12" : 0x8d, "`" : 0x95, "1" : 0x96, "2" : 0x97, "3" : 0x98, "4" : 0x99, "5" : 0x9a, "6" : 0x9b, "7" : 0x9c, "8" : 0x9d, "9" : 0x9e, "0" : 0x9f, "-" : 0xa0, "=" : 0xa1, "BACKSPACE" : 0xa2, "TAB" : 0xaa, "Q" : 0xab, "W" : 0xac, "E" : 0xad, "R" : 0xae, "T" : 0xaf, "Y" : 0xb0, "U" : 0xb1, "I" : 0xb2, "O" : 0xb3, "P" : 0xb4, "[" : 0xb5, "]" : 0xb6, "BACKSLASH" : 0xb7, "CAPS" : 0xbf, "A" : 0xc0, "S" : 0xc1, "D" : 0xc2, "F" : 0xc3, "G" : 0xc4, "H" : 0xc5, "J" : 0xc6, "K" : 0xc7, "L" : 0xc8, ";" : 0xc9, "'" : 0xca, "ENTER" : 0xcc, "SHIFT_L" : 0xd4, "Z" : 0xd6, "X" : 0xd7, "C" : 0xd8, "V" : 0xd9, "B" : 0xda, "N" : 0xdb, "M" : 0xdc, "," : 0xdd, "." : 0xde, "/" : 0xdf, "SHIFT_R" : 0xe1, "CTRL_L" : 0xe9, "WIN" : 0xea, "ALT_L" : 0xeb, "SPACEBAR" : 0xee, "ALT_R" : 0xf2, "FN" : 0xf3, "MENU" : 0xf5, "CTRL_R" : 0xf6, "INS" : 0xa3, "HM" : 0xa4, "PU" : 0xa5, "DEL" : 0xb8, "END" : 0xb9, "PD" : 0xba, "UP" : 0xe3, "LEFT" : 0xf7, "DOWN" : 0xf8, "RIGHT" : 0xf9, "PB" : 0x90, "SL" : 0x8f, "PS" : 0x8e, "NUMLOCK" : 0xa6, "KPSLASH" : 0xa7, "KPASTERISK" : 0xa8, "KPMINUS" : 0xa9, "KPPLUS" : 0xbe, "KP1" : 0xe5, "KP2" : 0xe6, "KP3" : 0xe7, "KP4" : 0xd0, "KP5" : 0xd1, "KP6" : 0xd2, "KP7" : 0xbb, "KP8" : 0xbc, "KP9" : 0xbd, "KP0" : 0xfa, "KPDOT" : 0xfc, "KPENTER" : 0xe8}

    def connect(self):
        dev = usb.core.find(
            idVendor=0x2ea8,  # Noname
            idProduct=0x2125  # Gaming Keyboard
        )
        if dev is None:
            # Device not present, or user is not allowed to access device.
            raise ValueError(
                "Keyboard not present or insufficient permissions")

        self.reattach = False
        if dev.is_kernel_driver_active(self.rgbinterface):
            self.reattach = True
            dev.detach_kernel_driver(self.rgbinterface)
        conf = dev.get_active_configuration()
        interface = conf[(self.rgbinterface, 0)]
        self.dev = dev

        writergbendpoint = usb.util.find_descriptor(
            interface,
            bEndpointAddress=0x03
        )
        if writergbendpoint is None:
            raise ValueError("Endpoint for writing not found")
        self.writergbendpoint = writergbendpoint
        self.write = writergbendpoint.write
        
        readrgbendpoint = usb.util.find_descriptor(
            interface,
            bEndpointAddress=0x03
        )
        if readrgbendpoint is None:
            raise ValueError("Endpoint for reading not found")
        self.readrgbendpoint = readrgbendpoint
        self.read = readrgbendpoint.read
    
    def disconnect(self):
        # This is needed to release interface, otherwise attach_kernel_driver fails
        # due to "Resource busy"
        usb.util.dispose_resources(self.dev)

        # In theory you don't even need to reattach the kernel.
        # The kernel does not use this part of the device
        if self.reattach:
            self.dev.attach_kernel_driver(self.rgbinterface)

    def __init__(self):
        self.connect()
        a=sorted(self.keyboard.items(), key=itemgetter(1))
        self.keyboard={}
        for i in a:
            self.keyboard[i[0]]=i[1]
    

    def __del__(self):
        self.disconnect()

    def sendbrightness(self, brightness):
        self.disconnect()
        self.connect()
        #4 is max brightness
        self.write(bytearray.fromhex('04ae0100001b020'+str(round(brightness*0.04))+'ff')) #Brightness, 00 - not powered, 06 - max brightness


    def sendhex(self, jsoncolors):
        """
        Send a message with key colors

        Keyword arguments:
        jsoncolors -- Structure with the all colors, that needs to be set
        """
        header = '04ae0100001b0204ff'

        #self.write(bytearray.fromhex('04ae0100001b0204ff8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')) #Direct send example
        
        count=0
        payload=''
        self.disconnect()
        self.connect()

        for keyname, color in jsoncolors.items():
            payload+="%0.2x" % self.keyboard[keyname] #Just convert HEX value to hex string
            payload+=color
            count+=1
            if count==12:
                self.write(bytearray.fromhex(header+payload+'ff000000000000'))
                self.disconnect()
                self.connect()
                count=0
                payload=''
        if count!=0: #If amount of items is not multiple of five
            payload+="ff"+'0'*(110-len(payload)) #TODO: REPLACE FILERS #128 - header size = 110
            self.write(bytearray.fromhex(header+payload))