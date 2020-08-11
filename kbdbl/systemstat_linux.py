from pathlib import Path

def getCapslockState():
	f=open("/sys/class/leds/input16::capslock/brightness")
	state_str=f.read()
	f.close()
	state=bool(int(state_str))
	return state

def getDPMSState():
	drmpath=Path('/sys/class/drm')
	for x in drmpath.iterdir():
		devicepath=str(x)
		f=open(devicepath+'/enabled')
		en_state=f.read()
		f.close()
		f=open(devicepath+'/dpms')
		dpms_state=f.read()
		f.close()
		if en_state=='enabled\n' and dpms_state=='On\n':
			return True
	return False