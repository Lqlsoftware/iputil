#-*- coding:utf-8 -*-
import iputil

def get_region(ip, algorithm="binary"):
    if not iputil.region_db.isip(ip):
        return ""
        
    if algorithm == "binary":
        data = iputil.region_db.binarySearch(ip)
    else:
        data = iputil.region_db.memorySearch(ip)

    return data