# Copyright 2022 The Ip2Region Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
#  Created by luckydog on 2022/6/29.
#  Copyright © 2022 luckydog. All rights reserved.
#
#  For more infomations & copyrights, please visit
#    https://github.com/lionsoul2014/ip2region

import socket
import struct
import io
import os
import sys
import iputil

HeaderInfoLength = 256
VectorIndexRows = 256
VectorIndexCols = 256
VectorIndexSize = 8
SegmentIndexSize = 14


class XdbSearcher(object):
    __f = None

    vectorIndex = None
    contentBuff = None

    def __init__(self, dbfile=None, vectorIndex=None, contentBuff=None):
        # Open DB File & load into memory
        if dbfile is None:
            dbfile = os.path.join(
                os.path.dirname(iputil.__file__),
                "data/ip2region.xdb"
            )
        self.initDatabase(dbfile, vectorIndex, contentBuff)

    def search(self, ip):
        ip = self.ip2long(ip)

        # locate the segment index block based on the vector index
        sPtr = ePtr = 0
        il0 = (int)((ip >> 24) & 0xFF)
        il1 = (int)((ip >> 16) & 0xFF)
        idx = il0 * VectorIndexCols * VectorIndexSize + il1 * VectorIndexSize

        if self.vectorIndex is not None:
            sPtr = self.getLong(self.vectorIndex, idx)
            ePtr = self.getLong(self.vectorIndex, idx + 4)
        elif self.contentBuff is not None:
            sPtr = self.getLong(self.contentBuff, HeaderInfoLength + idx)
            ePtr = self.getLong(self.contentBuff, HeaderInfoLength + idx + 4)
        else:
            self.__f.seek(HeaderInfoLength + idx)
            buffer_ptr = self.__f.read(8)
            sPtr = self.getLong(buffer_ptr, 0)
            ePtr = self.getLong(buffer_ptr, 4)

        # binary search the segment index block to get the region info
        dataLen = dataPtr = int(-1)
        l = int(0)
        h = int((ePtr - sPtr) / SegmentIndexSize)
        while l <= h:
            m = int((l + h) >> 1)
            p = int(sPtr + m * SegmentIndexSize)
            # read the segment index
            buffer_sip = self.readBuffer(p, SegmentIndexSize)
            sip = self.getLong(buffer_sip, 0)
            if ip < sip:
                h = m - 1
            else:
                eip = self.getLong(buffer_sip, 4)
                if ip > eip:
                    l = m + 1
                else:
                    dataLen = self.getInt2(buffer_sip, 8)
                    dataPtr = self.getLong(buffer_sip, 10)
                    break

        # empty match interception
        if dataPtr < 0:
            return ""

        buffer_string = self.readBuffer(dataPtr, dataLen)
        return_string = buffer_string.decode("utf-8")
        return return_string

    def readBuffer(self, offset, length):
        buffer = None
        # check the in-memory buffer first
        if self.contentBuff is not None:
            buffer = self.contentBuff[offset:offset + length]
            return buffer

        # read from the file handle
        if self.__f is not None:
            self.__f.seek(offset)
            buffer = self.__f.read(length)
        return buffer

    def initDatabase(self, dbfile, vi, cb):
        """
        " initialize the database for search
        " param: dbFile, vectorIndex, contentBuff
        """
        try:
            if cb is not None:
                self.__f = None
                self.vectorIndex = None
                self.contentBuff = cb
            else:
                self.__f = io.open(dbfile, "rb")
                self.vectorIndex = vi
        except IOError as e:
            print("[Error]: %s" % e)
            sys.exit()

    def ip2long(self, ip):
        _ip = socket.inet_aton(ip)
        return struct.unpack("!L", _ip)[0]

    def getLong(self, b, offset):
        if len(b[offset:offset + 4]) == 4:
            return struct.unpack('I', b[offset:offset + 4])[0]
        return 0

    def getInt2(self, b, offset):
        return ((b[offset] & 0x000000FF) | (b[offset+1] & 0x0000FF00))

    def close(self):
        if self.__f is not None:
            self.__f.close()
        self.vectorIndex = None
        self.contentBuff = None
