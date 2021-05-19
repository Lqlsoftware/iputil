#-*- coding:utf-8 -*-
import iputil

def get_region(ip, algorithm="b-tree"):
    if not iputil.region_db.isip(ip):
        return ""
        
    if algorithm == "binary":
        data = iputil.region_db.binarySearch(ip)
    elif algorithm == "memory":
        data = iputil.region_db.memorySearch(ip)
    else:
        data = iputil.region_db.btreeSearch(ip)

    return data["region"]