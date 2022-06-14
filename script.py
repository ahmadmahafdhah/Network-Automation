#!/usr/bin/python3

import sys
from time import sleep
from netmiko import ConnectHandler
import re

device = {
    'device_type': 'cisco_ios',
    'host': sys.argv[1],
    'username': 'nes470user',
    'password': 'nes470passwd',
}

connection = ConnectHandler(**device)                                          # connecting to the router

output1 = connection.send_command("show ip interface brief\n")
output2 = connection.send_command("show interfaces | i (Hardware is)\n")
output3 = connection.send_command("show interfaces\n")


interface_name = re.findall(r'[a-zA-z]+\d+', output1)                          # retrieving interface name from show ip interface brief


interface_ip = re.findall(r'unassigned|[\d.]{7,15}', output1)                  # retrieving interface ip address from show ip interface brief
for i in range(len(interface_ip)):                                             #
    if interface_ip[i] == "unassigned":                                        # changing format by replacing unassigned IPs with −
        interface_ip[i] = "−"


RE_interface_mac = re.findall(r'Loopback| [a-fA-f0-9.]{14} ', output2)         # retrieving interface mac address from show interfaces
interface_mac = []                                                             #
for i in range(len(RE_interface_mac)):                                         # changing format by replacing Loopback interface mac address with :::::
    if RE_interface_mac[i] == "Loopback":
        interface_mac.append(":::::")
    else:
        interface_mac.append(                                                  # changing format of the mac address to AB:CD:EF:WX:YZ
        RE_interface_mac[i][1].upper() + RE_interface_mac[i][2].upper() +':'+ 
        RE_interface_mac[i][3].upper() + RE_interface_mac[i][4].upper() +':'+ 
        RE_interface_mac[i][6].upper() + RE_interface_mac[i][7].upper() +':'+ 
        RE_interface_mac[i][8].upper() + RE_interface_mac[i][9].upper() +':'+ 
        RE_interface_mac[i][11].upper() + RE_interface_mac[i][12].upper() +':'+ 
        RE_interface_mac[i][13].upper() + RE_interface_mac[i][14].upper())


RE_interface_status = re.findall(r' up | down ', output3)                      # retrieving interface status from show interfaces
interface_status = []                                                          #
for i in range(len(RE_interface_status)):                                      # changing format of interface status
    if RE_interface_status[i] == " up ":
        interface_status.append(RE_interface_status[i][1].upper() + RE_interface_status[i][2].upper())
    elif RE_interface_status[i] == " down ":
        interface_status.append(RE_interface_status[i][1].upper() + RE_interface_status[i][2].upper() + RE_interface_status[i][3].upper() + RE_interface_status[i][4].upper())


max_if_name = len(interface_name[0])                                           # finding interface with the longest name to print same # of - in top of interfaces names
for i in range(1,len(interface_name)):
    if len(interface_name[i]) > max_if_name:
        max_if_name = len(interface_name[i])

max_if_mac = len(interface_mac[0])                                             # finding interface with the longest mac to print same # of - in top of interfaces mac
for i in range(1,len(interface_mac)):
    if len(interface_mac[i]) > max_if_mac:
        max_if_mac = len(interface_mac[i])

max_if_ip = len(interface_ip[0])                                               # finding interface with the longest ip to print same # of - in top of interfaces ip
for i in range(1,len(interface_ip)):
    if len(interface_ip[i]) > max_if_ip:
        max_if_ip = len(interface_ip[i])

max_if_status = len(interface_status[0])                                       # finding interface with the longest status to print same # of - in top of interfaces status
for i in range(1,len(interface_status)):
    if len(interface_status[i]) > max_if_status:
        max_if_status = len(interface_status[i])
if max_if_status == 2:
    max_if_status += 4
else:
    max_if_status += 2


print(f"{{:{max_if_name+2}}}{{:{max_if_mac+2}}}{{:{max_if_ip+2}}}{{:{max_if_status+2}}}".format("Interface Name","MAC Address","IP Address","Status"))

for i in range(max_if_name):
    print("-",end="")
print("  ",end="")

for i in range(max_if_mac):
    print("-",end="")
print("  ",end="")

for i in range(max_if_ip):
    print("-",end="")
print("  ",end="")

for i in range(max_if_status):
    print("-",end="")
print("")

for i in range(len(interface_name)):
    print(f"{{:{max_if_name+2}}}{{:{max_if_mac+2}}}{{:{max_if_ip+2}}}{{:{max_if_status+2}}}".format(interface_name[i], interface_mac[i], interface_ip[i], interface_status[i]))
