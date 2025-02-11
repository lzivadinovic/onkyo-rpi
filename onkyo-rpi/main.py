import argparse
import sys
import time
import pigpio
from command import OnkyoCommand

a9150Commands = {
    "vu" : [2],
    "vd" : [3],
    "pwr" : [4],
    "mute" : [5],
    "srcu" : [213],
    "srcd" : [214],
    "d1" : [32],
    "d2" : [224],
    "d3" : [224,213],
    "d4" : [224, 213, 213],
    "l1" : [224, 213, 213, 213],
    "l2" : [224, 213, 213, 213, 213],
    "l3" : [224, 213, 213, 213, 213, 213],
    "l4" : [224, 213, 213, 213, 213, 213, 213],
    "phono" : [224, 213, 213, 213, 213, 213, 213, 213],
    # we do it like this because every time we go over main some relays pop
    "main" : [32, 214],  # Switch to D1 and go src down
}

def parse_args():
    parser = argparse.ArgumentParser(
        description='A tool to control onkyo devices over Remote Interactive (RI) interface.')

    parser.add_argument('--gpio', type=int, nargs='?', default=25,
                        help="GPIO port of your pi you want to use - default: 25")
    parser.add_argument('--count', type=int, nargs='?', default=1,
                        help="How many times you want to send specif command (useful for volume) - default: 1")
    # Send command or message
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--command', type=lambda x: x.lower(), nargs='?',
                        help="Exec specific command for A-9150")

    group.add_argument('--message', type=lambda x: [int(x, 0)], nargs='?',
                        help='message (0x000-0xFFF or 0-4095) to send to your onkyo device')

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    if args.message:
        cmdlist = args.message
    else:
        cmdlist = a9150Commands[args.command]

    count = int(args.count)
    gpiopin = int(args.gpio)

    # print('send message {:012b} ({:04d}) via GPIO {:d}, {:d} times'
    #       .format(message, message, args.gpio, count))

    pi = pigpio.pi()
    command = OnkyoCommand(pi, gpio=gpiopin)
    for cmd in cmdlist:
        command.send(cmd, count)
    time.sleep(1)

    pi.stop()