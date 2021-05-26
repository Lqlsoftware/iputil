# iputil

Provide some useful util functions and a tool (`ip2region`) for ip processing.

# Install
```shell
pip3 install iputil
```

# Python usage

```python
import iputil

# Get Region by IP
iputil.get_region("60.30.1.1")
# return string '中国|0|天津|天津|联通'
```

Although region data in this program will update with the [@ip2region](https://github.com/lionsoul2014/ip2region) repo, or your can specify your own data source:
```python
import iputil

# Set Region source
iputil.set_region_source(data_file="ip2region.db")

# Get Region by IP
iputil.get_region("60.30.1.1")
# return string '中国|0|天津|天津|联通'
```


# Tools

An independent tool named `ip2region` will be install in your path.

Typing `ip2region` will start a prompt:
```shell
$ ip2region
ip> 192.168.0.1
[192.168.0.1]   0|0|0|内网IP|内网IP

ip> 60.30.1.1
[60.30.1.1]     中国|0|天津|天津|联通

ip> 120.100.0.1
[120.100.0.1]   中国|0|台湾|台北|0

ip> 8.8.8.8
[8.8.8.8]       美国|0|0|0|谷歌

ip> 
```

```shell
$ ip2region -h
usage: ip2region [-h] [-ip IP]

IP to Region

optional arguments:
  -h, --help       show this help message and exit
  -ip IP, --ip IP  Search specify IP
```

# Reflink
[@ip2region](https://github.com/lionsoul2014/ip2region)
