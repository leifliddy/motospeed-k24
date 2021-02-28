from pathlib import Path

ledpath=''
devicepath=''

def getCapslockState(vid, pid):
	global ledpath
	ledspath=Path('/sys/class/leds')
	if ledpath=='' or not Path(ledpath).exists():
		for x in ledspath.iterdir():
			ledpath=str(x)
			if ledpath.find('capslock')!=-1:
				f=open(ledpath+'/device/id/product')
				pid_path=f.read()
				f.close()
				f=open(ledpath+'/device/id/vendor')
				vid_path=f.read()
				f.close()
				if ("%0.4x" % vid)+'\n'==vid_path and ("%0.4x" % pid)+'\n'==pid_path:
					print(ledpath)
					break
	f=open(ledpath+'/brightness')
	state_str=f.read()
	f.close()
	return(bool(int(state_str)))

def getDPMSState():
	global devicepath
	drmpath=Path('/sys/class/drm')
	if devicepath!='' and Path(devicepath).exists():
		f=open(devicepath+'/enabled')
		en_state=f.read()
		f.close()
		f=open(devicepath+'/dpms')
		dpms_state=f.read()
		f.close()
	else:
		for x in drmpath.iterdir():
			devicepath=str(x)
			if devicepath.find('card')==-1 or devicepath.find('-')==-1:
				continue
			f=open(devicepath+'/enabled')
			en_state=f.read()
			f.close()
			f=open(devicepath+'/dpms')
			dpms_state=f.read()
			f.close()
			if en_state=='enabled\n':
				break

	if en_state=='enabled\n' and dpms_state=='On\n':
		return True
	return False