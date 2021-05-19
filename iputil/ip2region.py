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

    try:
        searcher = iputil.region_db
        if args.ip is not None:
            IP = args.ip
            if not searcher.isip(IP):
                print("%s is not a valid IP.\n" % IP)
                searcher.close()
                exit(-1)
            region = searcher.binarySearch(IP)
            print("[%s]\t%s\n" % (IP, region["region"]))
            searcher.close()
            exit(0)
            
        while(True):
            IP = input("ip> ")
            if not searcher.isip(IP):
                print("[%s] is not a valid IP.\n" % IP)
                continue
            region = searcher.binarySearch(IP)
            print("[%s]\t%s\n" % (IP, region["region"]))
    except KeyboardInterrupt as e:
        searcher.close()
        exit(0)
