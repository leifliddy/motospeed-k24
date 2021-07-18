"""
Parses and validates inputs for command line use
"""

import argparse
import k24.keylights as keylights

def main():
    """
        Parse arguments and start application appropriately
    """
    parse = argparse.ArgumentParser(
        description='Change light color for switches of the K24 numpad')
    parse.add_argument("-c", "--color", nargs='?', default='#red', help=
        "Set backlight color in keys. Can be input as #rrggbb in hexadecimal or as name.")
    parse.add_argument("-a", "--ambient", nargs='?', help=
        "Set color on ambient light band. Can be input as #rrggbb in hexadecimal or as name.")
    parse.add_argument("-b", "--brightness", nargs='?', default=2, help=
        "Set keyboard brightness (0-5)")

    args = parse.parse_args()

    lightctl = keylights.Keylights()

    if not args.ambient:
        args.ambient = args.color

    if args.color is not None:
        # set light for all keys
        lightctl.setall(args.color, args.ambient, args.brightness)


if __name__ == "__main__":
    main()
