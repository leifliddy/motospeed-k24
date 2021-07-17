""" Linux related implementation of USB code """
import usb.core
import usb.util

vid=0x0416
pid=0xa0f8

def isPresented():
    dev = usb.core.find(
        idVendor=vid,  # Winbond
        idProduct=pid  # Gaming Keyboard
    )
    if dev is not None:
        return(True)


class Usblinux():
    """ Class that implements Linux specific USB handling """
    rgbinterface = 1
    #keyboard={"ESC" : 0x29, "F1" : 0x3a, "F2" : 0x3b, "F3" : 0x3c, "F4" : 0x3d, "F5" : 0x3e, "F6" : 0x3f, "F7" : 0x40, "F8" : 0x41, "F9" : 0x42, "F10" : 0x43, "F11" : 0x44, "F12" : 0x45, "`" : 0x35, "1" : 0x1e, "2" : 0x1f, "3" : 0x20, "4" : 0x21, "5" : 0x22, "6" : 0x23, "7" : 0x24, "8" : 0x25, "9" : 0x26, "0" : 0x27, "-" : 0x2d, "=" : 0x2e, "BACKSPACE" : 0x2a, "TAB" : 0x2b, "Q" : 0x14, "W" : 0x1a, "E" : 0x08, "R" : 0x15, "T" : 0x17, "Y" : 0x1c, "U" : 0x18, "I" : 0x0c, "O" : 0x12, "P" : 0x13, "[" : 0x2f, "]" : 0x30, "BACKSLASH" : 0x31, "CAPS" : 0x39, "A" : 0x04, "S" : 0x16, "D" : 0x07, "F" : 0x09, "G" : 0x0a, "H" : 0x0b, "J" : 0x0d, "K" : 0x0e, "L" : 0x0f, ";" : 0x33, "'" : 0x34, "ENTER" : 0x28, "SHIFT_L" : 0xe1, "Z" : 0x1d, "X" : 0x1b, "C" : 0x06, "V" : 0x19, "B" : 0x05, "N" : 0x11, "M" : 0x10, "," : 0x36, "." : 0x37, "/" : 0x38, "SHIFT_R" : 0xe5, "CTRL_L" : 0xe0, "WIN" : 0xe3, "ALT_L" : 0xe2, "SPACEBAR" : 0x2c, "ALT_R" : 0xe6, "FN" : 0xed, "MENU" : 0x65, "CTRL_R" : 0xe4, "INS" : 0x49, "HM" : 0x4a, "PU" : 0x4b, "DEL" : 0x4c, "END" : 0x4d, "PD" : 0x4e, "UP" : 0x52, "LEFT" : 0x50, "DOWN" : 0x51, "RIGHT" : 0x4f, "PB" : 0x48, "SL" : 0x47, "PS" : 0x46, "NUMLOCK" : 0x53, "KPSLASH" : 0x54, "KPASTERISK" : 0x55, "KPMINUS" : 0x56, "KPPLUS" : 0x57, "KP1" : 0x59, "KP2" : 0x5a, "KP3" : 0x5b, "KP4" : 0x5c, "KP5" : 0x5d, "KP6" : 0x5e, "KP7" : 0x5f, "KP8" : 0x60, "KP9" : 0x61, "KP0" : 0x62, "KPDOT" : 0x63, "KPENTER" : 0x58}

    def __init__(self):
        dev = usb.core.find(
            idVendor=vid,  # Winbond
            idProduct=pid  # Gaming Keyboard
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
        
    """
    def __del__(self):
        # This is needed to release interface, otherwise attach_kernel_driver fails
        # due to "Resource busy"
        usb.util.dispose_resources(self.dev)

        # In theory you don't even need to reattach the kernel.
        # The kernel does not use this part of the device
        if self.reattach:
            self.dev.attach_kernel_driver(self.rgbinterface)
    """

    def setcolor(self, key_color, ambient_color, brightness):
        # Brightness: 0 is powered off, 5 is max brightness
        # set keylight + brightness
        self.write(bytearray.fromhex('06be150001010b000' + str(brightness) + '000000' + key_color + '0000000000000000000000000000000000'))
        
        # set ambient_light
        self.write(bytearray.fromhex('06be15000201020002000000' + ambient_color + '00' + ambient_color + '00000000000000000000000000'))
