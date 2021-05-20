#-*- coding:utf-8 -*-
"""
" ip2region python seacher client module
"
" Author: koma<komazhang@foxmail.com>
" Date : 2015-11-06
"""
import struct, io, socket, sys, os
import iputil

class Ip2Region(object):
    dbfile = "data/ip2region.db"

    def __init__(self):
        self.__INDEX_BLOCK_LENGTH  = 12
        self.__TOTAL_HEADER_LENGTH = 8192
        self.__f          = None
        self.__headerSip  = []
        self.__headerPtr  = []
        self.__headerLen  = 0
        self.__indexSPtr  = 0
        self.__indexLPtr  = 0
        self.__indexCount = 0
        self.__dbBinStr   = ''
        path = os.path.dirname(iputil.__file__)
        self.initDatabase(os.path.join(path, self.dbfile))

    def memorySearch(self, ip):
        """
        " memory search method
        " param: ip
        """
        if not ip.isdigit(): ip = self.ip2long(ip)

        if self.__dbBinStr == '':
            self.__dbBinStr   = self.__f.read() #read all the contents in file
            self.__indexSPtr  = self.getLong(self.__dbBinStr, 0)
            self.__indexLPtr  = self.getLong(self.__dbBinStr, 4)
            self.__indexCount = int((self.__indexLPtr - self.__indexSPtr)/self.__INDEX_BLOCK_LENGTH)+1

        l, h, dataPtr = (0, self.__indexCount, 0)
        while l <= h:
            m = int((l+h) >> 1)
            p = self.__indexSPtr + m*self.__INDEX_BLOCK_LENGTH
            sip = self.getLong(self.__dbBinStr, p)

            if ip < sip:
                h = m -1
            else:
                eip = self.getLong(self.__dbBinStr, p+4)
                if ip > eip:
                    l = m + 1;
                else:
                    dataPtr = self.getLong(self.__dbBinStr, p+8)
                    break

        if dataPtr == 0: raise Exception("Data pointer not found")

        return self.returnData(dataPtr)

    def binarySearch(self, ip):
        """
        " binary search method
        " param: ip
        """
        if not ip.isdigit(): ip = self.ip2long(ip)

        if self.__indexCount == 0:
            self.__f.seek(0)
            superBlock = self.__f.read(8)
            self.__indexSPtr = self.getLong(superBlock, 0)
            self.__indexLPtr = self.getLong(superBlock, 4)
            self.__indexCount = int((self.__indexLPtr - self.__indexSPtr) / self.__INDEX_BLOCK_LENGTH) + 1

        l, h, dataPtr = (0, self.__indexCount, 0)
        while l <= h:
            m = int((l+h) >> 1)
            p = m*self.__INDEX_BLOCK_LENGTH

            self.__f.seek(self.__indexSPtr+p)
            buffer = self.__f.read(self.__INDEX_BLOCK_LENGTH)
            sip = self.getLong(buffer, 0)
            if ip < sip:
                h = m - 1
            else:
                eip = self.getLong(buffer, 4)
                if ip > eip:
                    l = m + 1
                else:
                    dataPtr = self.getLong(buffer, 8)
                    break

        if dataPtr == 0: raise Exception("Data pointer not found")

        return self.returnData(dataPtr)

    def initDatabase(self, dbfile):
        """
        " initialize the database for search
        " param: dbFile
        """
        try:
            self.__f = io.open(dbfile, "rb")
        except IOError as e:
            print("[Error]: %s" % e)
            sys.exit()

    def returnData(self, dataPtr):
        """
        " get ip data from db file by data start ptr
        " param: dsptr
        """
        dataLen = (dataPtr >> 24) & 0xFF
        dataPtr = dataPtr & 0x00FFFFFF

        self.__f.seek(dataPtr)
        data = self.__f.read(dataLen)

        return data[4:].decode('utf-8')

    def ip2long(self, ip):
        _ip = socket.inet_aton(ip)
        return struct.unpack("!L", _ip)[0]

    def isip(self, ip):
        p = ip.split(".")

        if len(p) != 4           : return False
        for pp in p:
            if not pp.isdigit()  : return False
            if len(pp) > 3       : return False
            if int(pp) > 255     : return False

        return True

    def getLong(self, b, offset):
        if len(b[offset:offset+4]) == 4:
            return struct.unpack('I', b[offset:offset+4])[0]
        return 0

    def close(self):
        if self.__f != None:
            self.__f.close()

        self.__dbBinStr  = None
        self.__headerPtr = None
        self.__headerSip = None
