# Network-Automation

This is a Python script that acts as a minimalist network automation program.
The script sends the required command to a Cisco router, and receives and displays its output in a convenient, well-formatted manner.
The script is self executable, an it takes one command line argument.
for example, it should run as follow: ./script.py <router IP address>

using regex library, it gives the following output:

Interface Name   MAC Address       IP Address   Status
---------------- ----------------- ------------ ------
GigabitEthernet1 08:00:27:48:BB:1F 10.0.5.51    UP
GigabitEthernet2 08:00:27:5D:76:7E 192.168.1.70 UP
GigabitEthernet3 08:00:27:5A:52:10    −         DOWN
Loopback0        :::::             1.1.1.1      UP
Loopback1        :::::                −         DOWN
