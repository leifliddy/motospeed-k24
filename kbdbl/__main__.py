"""
Parses and validates inputs for command line use
"""

import random
import argparse
import kbdbl.keylights as keylights
import kbdbl.systemstat as systemstat
import json, subprocess, re, time
from pathlib import Path

def main():
    """
        Parse arguments and start application appropriately
    """
    parse = argparse.ArgumentParser(
        description='Change light color for switches of the Drevo Calibur keyboard')
    parse.add_argument("-c", "--color", nargs='?', help=
        "Color to set on LEDs. Can be input as #rrggbb in hexadecimal or as name.")
    parse.add_argument("-k", "--key", nargs='?', help=
        "Keyname of the Key to be set. " +
        "Options can be seen in output of -v. " +
        "If not given whole keyboard is set to given color.")
    parse.add_argument("-r", "--random", action="store_true", help=
        "Set random color for given key or full keyboard")
    parse.add_argument("-R", "--allrandom", action="store_true", help=
        "Set each key to a random color. This overwrites all other options.")
    parse.add_argument("-p", "--profile", nargs='?', help=
        "JSON color profile to use")
    parse.add_argument("-b", "--brightness", nargs='?', help=
        "Set keyboard brightness (0-6)")
    parse.add_argument("-d", "--daemon", action="store_true", help=
        "Daemon mode")

    args = parse.parse_args()

    lightctl = keylights.Keylights()
    configfolder=str(Path.home())+'/.config/kbdbl/'

    if not args.allrandom and args.color is None and not args.random and args.profile is None and args.brightness is None and not args.daemon:
        parse.print_usage()

    if args.brightness is not None:
        lightctl.setbrightness(int(args.brightness))

    if args.allrandom:
        lightctl.setrandom()

    if args.profile is not None:
        with open(configfolder+args.profile) as f:
            profile_json = json.load(f)
        lightctl.setprofile(profile_json)

    if args.random:
        lightctl.setallrandom()

    if args.color is not None:
        if args.key is not None:
            # Set light for specific key
            lightctl.setkey(args.key, args.color)
        else:
            # Set light for all keys
            lightctl.setall(args.color)

    if args.daemon:
        config={
        "defaultprofile": "defaultprofile.json",
        "brightness": 100,
        "capslight": False,
        "capslight_oncolor": "ff0000",
        "capslight_offcolor": "ffffff",
        "followdpms": False,
        "offbrightness": 0
        } #Default configuration
        capslock_state=False
        monitor_state=False

        if Path(configfolder).is_dir() is False: #If basic configuration not created
            print('configuring')
            Path(configfolder).mkdir()
            with open(configfolder+'config.json', 'w') as f:
                json.dump(config, f, indent=4) #Save default config
            with open(configfolder+config['defaultprofile'], 'w') as f:  
                json.dump(lightctl.gencolorprofile('white'), f, indent=4) #Save default profile
        else:
            with open(configfolder+'config.json') as f:
                config = json.load(f) #Load config if exist


        with open(configfolder+config['defaultprofile']) as f:
            profile_json = json.load(f)
        lightctl.setprofile(profile_json) #Load profile on start

        while  True:
            capslock_state_old=capslock_state
            monitor_state_old=monitor_state
            capslock_state=systemstat.getCapslockState()
            monitor_state=systemstat.getDPMSState()
            if capslock_state and not capslock_state_old and config['capslight']:
                lightctl.setkey('CAPS', '#'+config['capslight_oncolor'])
            if not capslock_state and capslock_state_old and config['capslight']:
                lightctl.setkey('CAPS', '#'+config['capslight_offcolor'])

            if not monitor_state and monitor_state_old and config['followdpms']:
                lightctl.setbrightness(config['offbrightness'])
            if monitor_state and not monitor_state_old and config['followdpms']:
                lightctl.setbrightness(config['brightness'])
            time.sleep(0.1)


if __name__ == "__main__":
    main()
