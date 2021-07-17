
# motospeed-k24

Keyboard backlight control for the Motospeed K24 numeric keypad. 

## Usage

### Linux

Dependant Packages:

* [PyUSB 1.0+](https://github.com/pyusb/pyusb)
* [colour 0.1.5+](https://github.com/vaab/colour)


Install on Fedora with:
* ```dnf install python3-colour python3-pyusb```


run the following to turn all keys purple, turn the ambient light-band red, and set the brightness to 3 (scale 0-5)

```
git clone git clone https://github.com/leifliddy/motospeed-k24.git
cd motospeed-k24/
python3 -m k24 -c purple -a red -b 3 
```

You could also just run: 
```
python3 -m kbdbl -c purple
```

In this case, the -a (ambient light) value would be set to purple (to match the -c value) and the -b value would be set to 2 (which is the default value if it's not specified)


Packages:

* [PyUSB 1.0+](https://github.com/pyusb/pyusb)
* [colour 0.1.5+](https://github.com/vaab/colour)


Install on Fedora with:
* ```dnf install python3-colour python3-pyusb```


### Hardwarehttps://github.com/brainrom/winbond-kbdbl

The Motospeed K24 Mechanical numeric keyPad. 
VID: 0416, PID: a0f8, Winbond Electronics Corp. Gaming Keyboard.

# Restrictions
This was a very quick and dirty rewrite (and simplifcation) of the https://github.com/brainrom/winbond-kbdbl project
to support the Motospeed K24 numeric keypad.

You can only set the keys to a single color and adjust the brightness. That's pretty much it. 
I simply don't have the desire or need to enable effects or to enable profiles to set individual keys to different colors. 
But honestly, it wouldn't be that difficult to use wireshark to capture the HID Data and analyze + decode it (which is how I made this driver)


## Adding support for another keyboard (reverse-engineering workflow)
1. Set up virtual machine with Windows and install vendor's program into it. 
2. Forward your keyboard into the VM
3. Hook up wireshark in Linux and sniff keyboard's protocol
4. Recreate it's behaviour
5. Fork repo and post your code
6. ????
7. PROFIT
