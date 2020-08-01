"""
Parses and validates inputs for command line use
"""

import random
import argparse
import time
import drevo.keylights as keylights
from drevo import keyboard
import json, subprocess, re, time


def main():
    """
        Parse arguments and start application appropriately
    """
    # TODO: Add parameter for a json object mapping key -> color
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
    parse.add_argument("--capslight", action="store_true", help=
        "Indicate capslock status by key color")
    parse.add_argument("--followdpms", action="store_true", help=
        "Follow monitor's DPMS status and disable keyboard light if monitor disabled")


    args = parse.parse_args()

    lightctl = keylights.Keylights()
    
    if not args.allrandom and args.color is None and not args.random and args.profile is None and args.brightness is None and not args.daemon:
        parse.print_usage()

    if args.brightness is not None:
        lightctl.setbrightness(int(args.brightness))

    if args.allrandom:
        lightctl.setrandom()

    if args.profile is not None:
        with open(args.profile) as f:
            profile_json = json.load(f)
        lightctl.setprofile(profile_json)

    if args.random:
        args.color = "#" + "".join(random.sample("0123456789abcdef", 6))

    if args.color is not None:
        if args.key is not None:
            # Set light for specific key
            lightctl.setkey(args.key, args.color)
        else:
            # Set light for all keys
            lightctl.setall(args.color)

    if args.daemon:
        monitorpattern='(?<=Monitor is ).*'
        kbdlenpattern='(?<=LED mask:  )\\d*'
        while  True:
            xsetresult=subprocess.check_output('xset q', shell=True).decode("utf-8")
            capslock_status=int(re.search(kbdlenpattern, xsetresult).group())
            monitor_status=re.search(monitorpattern, xsetresult).group()
            if (capslock_status==3 or capslock_status==1) and args.capslight:
                lightctl.setkey('CAPS', 'red')
            if (capslock_status==2 or capslock_status==0) and args.capslight:
                lightctl.setkey('CAPS', 'white')

            if (monitor_status!='On') and args.followdpms:
                lightctl.setbrightness(0)
            if (monitor_status=='On') and args.followdpms:
                lightctl.setbrightness(5)
            time.sleep(1)
if __name__ == "__main__":
    main()
