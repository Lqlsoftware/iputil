#!/usr/bin/env python3
import sys
import argparse
import iputil

sys.setrecursionlimit(10000)


def get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="IP to Region")
    parser.add_argument("-ip", "--ip", dest='ip',
                        help="Search specify IP")
    return parser.parse_args(args)


def main():
    args = get_arguments()

    if args.ip is not None:
        if not iputil.valid_ip(args.ip):
            print("%s is not a valid IP.\n" % args.ip)
            exit(-1)
        region = iputil.get_region(args.ip)
        print("[%s]\t%s\n" % (args.ip, region))
        exit(0)

    try:
        while(True):
            IP = input("ip> ")
            if not iputil.valid_ip(IP):
                print("[%s] is not a valid IP.\n" % IP)
                continue
            region = iputil.get_region(IP)
            print("[%s]\t%s\n" % (IP, region))
    except KeyboardInterrupt as e:
        exit(0)
