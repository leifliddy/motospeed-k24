
# fdclct

Free Drevo Calibur Lighting Control Tool

**Now remastered for absolutely different keyboard!**

## Usage

### Linux (possibly also unixes)

**The simple way:**

In the folder containing the drevo folder, use the shell to light the C key in red:

```bash
sudo python3 -m drevo -c red -k C
```

**The better way:**

Use a udev rule so you may access the USB device with your user privileges and drop the sudo. An example can be found [here](utils/).
I highly discourage you from running anybody's shitty python code with root privileges.

### Windows

```cmd
python3 -m drevo --help
```

### To use it as python module

Include the drevo folder in your module path and simply import it in your python file.

```python
import drevo
```

### General

If you want to input colors as hexadecimal values input it like this: ```-c #deadbe```, otherwise many color names are accepted.

## What this should one day become

This tool is to set the color of the RGB LEDs in the Drevo Calibur keyboard. By default this keyboard can be set to 8 different colors per key, but the Windows software by Drevo ([you can get from here](https://drevo.net/product/keyboard/calibur)) supports color selection per key with 24 bit color. Sadly it is closed source and Windows exclusive. So this project aims to reverse engineer the USB communication and implement a free version of the same tool to enable platform independent keyboard RGB glory.

## Requirements

### Software

This package is written for Python 3.

Packages:

* [PyUSB 1.0+](https://github.com/pyusb/pyusb) (under Ubuntu also available via ```sudo apt install python3-usb```)
* [colour 0.1.5](https://github.com/vaab/colour)

If under Windows, you will need the [libusb windows binaries](https://github.com/libusb/libusb/releases). This does not fully work yet, but will soon.

### Hardware

My keyboard is ZET  Blade, but should work with keyboard on the same chip. VID: 0416, PID: a0f8, Winbond Electronics Corp. Gaming Keyboard. 

## Restrictions

Due to the nature of the protocol the Calibur uses to set the leds it is not possible to hack fluid animations. This is due to the fact that for every single change in the configuration of the lighting a new colormap for every key is transfered to the keyboard. This process can take over half a second.


## Adding support for another keyboard (reverse-engineering workflow)
1. Set up virtual machine with Windows and install vendor's program into it. 
2. Forward your keyboard into the VM
3. Hook up wireshark in Linux and sniff keyboard's protocol
4. Recreate it's behaviour
5. Fork repo and post your code
6. ????
7. PROFIT
