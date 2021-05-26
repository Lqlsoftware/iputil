"""
" ip2region python seacher client module
"
" Author: koma<komazhang@foxmail.com>
" Date : 2015-11-06
"""
import struct
import io
import socket
import sys
import os
import iputil


class Ip2Region(object):
    dbfile = None
    data_file = ""

    def __init__(self):
        self.__INDEX_BLOCK_LENGTH = 12
        self.__indexSPtr = 0
        self.__indexLPtr = 0
        self.__indexCount = 0

        # Open DB File & load into memory
        if Ip2Region.dbfile is None:
            self.setSource(os.path.join(
                os.path.dirname(iputil.__file__),
                "data/ip2region.db"
            ))

    def setSource(self, data_file):
        try:
            Ip2Region.data_file = data_file
            with io.open(Ip2Region.data_file, "rb") as f:
                Ip2Region.dbfile = f.read()

            # initialize superBlock
            superBlock = Ip2Region.dbfile[0:8]
            self.__indexSPtr = self.getLong(superBlock, 0)
            self.__indexLPtr = self.getLong(superBlock, 4)
            self.__indexCount = int(
                (self.__indexLPtr - self.__indexSPtr) / self.__INDEX_BLOCK_LENGTH) + 1
        except IOError as e:
            print("[Error]: %s" % e)
            sys.exit()

    def binarySearch(self, ip):
        """
        " binary search method
        " param: ip
        """

        if not ip.isdigit():
            ip = self.ip2long(ip)

        l, h, dataPtr = (0, self.__indexCount, 0)
        while l <= h:
            m = int((l + h) >> 1)
            p = self.__indexSPtr + m * self.__INDEX_BLOCK_LENGTH

            if ip < self.getLong(Ip2Region.dbfile, p):
                h = m - 1
            elif ip > self.getLong(Ip2Region.dbfile, p + 4):
                l = m + 1
            else:
                dataPtr = self.getLong(Ip2Region.dbfile, p + 8)
                break

        if dataPtr == 0:
            raise Exception("Data pointer not found")

        # Extract data
        dataLen = ((dataPtr >> 24) & 0xFF) - 4
        dataPtr = (dataPtr & 0x00FFFFFF) + 4
        retData = Ip2Region.dbfile[dataPtr:dataPtr + dataLen].decode('utf-8')

        return retData

    def ip2long(self, ip):
        _ip = socket.inet_aton(ip)
        return struct.unpack("!L", _ip)[0]

    def getLong(self, b, offset):
        if len(b[offset:offset + 4]) == 4:
            return struct.unpack('I', b[offset:offset + 4])[0]
        return 0
