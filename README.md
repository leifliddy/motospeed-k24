
# kbdbl

Keyboard backlight control for Winbond Gaming Keyboard chip-based keyboards. 

## Usage

### Linux (possibly also unixes)

**The simple way:**

In the folder containing the drevo folder, use the shell to light the C key in red:

```bash
sudo python3 -m kbdbl -c red -k C
```

**The better way:**

PKGBUILD for Arch Linux is avalible. It contains the systemd service, udev rule and ready for everyday usage.
 Just after installation
```bash
sudo systemctl enabled winbond-kbdbl@_username_
```
and you are ready to go.

### Windows

DPMS and Capslock features will not work at all. Other features should work (but not tested), you can try it at your own risk! I will not support Windows compatibility by myself.
```cmd
python3 -m kbdbl --help
```


### Features

* Absoulutely custom backlight color profile (via config file)
* Changing keyboard brightness
* Following monitor's state by DPMS. Keyboard can disable backlight or reduce brightness if monitor is disabled.
* Indicating CapsLock state by key color

### Settings

All backlight-related settings is located in .config/kbdbl in your home folder

config.json is responsible for main settings:

* defaultprofile: Default profile's file name
* brightness: Keyboard brightness
* capslight: Indicate CapsLock by key color
* capslight_oncolor: CapsLock enabled key color
* capslight_offcolor: CapsLock disabled color
* followdpms: Disable (or reduce) backlight if monitor is disabled

defaultprofile.json file contains array with color in hex format for each key (default is all white)

## Requirements

### Software

This package is written for Python 3.

Packages:

* [PyUSB 1.0+](https://github.com/pyusb/pyusb) (under Ubuntu also available via ```sudo apt install python3-usb```)
* [colour 0.1.5](https://github.com/vaab/colour)

If under Windows, you will need the [libusb windows binaries](https://github.com/libusb/libusb/releases). This does not fully work yet, but will soon.

### Hardware

My keyboard is ZET  Blade, but should work with any keyboard on the same chip. VID: 0416, PID: a0f8, Winbond Electronics Corp. Gaming Keyboard. 

## Restrictions

Default fluid animations not avaliable, only custom profile.


## Adding support for another keyboard (reverse-engineering workflow)
1. Set up virtual machine with Windows and install vendor's program into it. 
2. Forward your keyboard into the VM
3. Hook up wireshark in Linux and sniff keyboard's protocol
4. Recreate it's behaviour
5. Fork repo and post your code
6. ????
7. PROFIT
