import iputil


def get_region(ip, algorithm="binary"):
    if not valid_ip(ip):
        return ""
    try:
        return iputil.region_db.binarySearch(ip)
    except Exception:
        return ""


def valid_ip(ip):
    p = ip.split(".")

    if len(p) != 4:
        return False
    for pp in p:
        if not pp.isdigit():
            return False
        if len(pp) > 3:
            return False
        if int(pp) > 255:
            return False

    return True
