#!/usr/bin/python3

import sys
from easysnmp import Session

if(len(sys.argv) > 3):
	print("Too many arguments.")
	print("community name and the router IP only required to execute the code")
	print("For example, the script will be run as follows: ./ID-129737-129503.py public 192.168.56.101")
	sys.exit()

if(len(sys.argv) < 3):
	print("Too few arguments.")
	print("community name and the router IP are both required to execute the code")
	print("For example, the script will be run as follows: ./ID-129737-129503.py public 192.168.56.101")
	sys.exit()

if(sys.argv[1] != "public"):
	print(sys.argv[1]+": wrong communtiy name")
	print('it should be "public"')
	sys.exit()

s = Session(hostname = sys.argv[2], community = sys.argv[1], version = 2, use_numeric = True, use_sprint_value = True)

response = s.get('.1.3.6.1.2.1.2.2.1.2.1')
interfaces_name = []
interfaces_name.append(response.value)
IF_name_INDEX = response.oid+'.'+response.oid_index
while(IF_name_INDEX[19] == '2'):
	response = s.get_next(IF_name_INDEX)
	IF_name_INDEX = response.oid+'.'+response.oid_index
	if(IF_name_INDEX[19] == '3'):
		break
	interfaces_name.append(response.value)

max_if_name = len(interfaces_name[0]) - 2
for i in range(1,len(interfaces_name)):
    if len(interfaces_name[i]) > max_if_name:
        max_if_name = len(interfaces_name[i]) - 2

#######################################################################################################################

response = s.get_next('.1.3.6.1.2.1.2.2.1.6')
interfaces_mac = []
interfaces_mac.append(response.value)
IF_mac_INDEX = response.oid+'.'+response.oid_index
while(IF_mac_INDEX[19] == '6'):
	response = s.get_next(IF_mac_INDEX)
	IF_mac_INDEX = response.oid+'.'+response.oid_index
	if(IF_mac_INDEX[19] == '7'):
		break
	interfaces_mac.append(response.value)

max_if_mac = len(interfaces_mac[0]) - 3
for i in range(1,len(interfaces_mac)):
    if len(interfaces_mac[i]) > max_if_mac:
        max_if_mac = len(interfaces_mac[i]) - 3

for i in range(len(interfaces_mac)):
	for j in range(len(interfaces_mac[i])):
		if(interfaces_mac[i][j] == " "):
			interfaces_mac[i] = interfaces_mac[i].replace(interfaces_mac[i][j],":")

for i in range(len(interfaces_mac)):
	if(interfaces_mac[i] == '""'):
		interfaces_mac[i] = interfaces_mac[i].replace('""',":::::")
	if(interfaces_mac[i] == '""'):
		interfaces_mac[i] = interfaces_mac[i].replace('""',":::::")

#######################################################################################################################

response1 = s.get_next('.1.3.6.1.2.1.2.2.1.1')
interfaces_index1 = []
interfaces_index1.append(response1.value)
IF_ip_INDEX1 = response1.oid+'.'+response1.oid_index
while(IF_ip_INDEX1[19] == "1"):
	response1 = s.get_next(IF_ip_INDEX1)
	IF_ip_INDEX1 = response1.oid+'.'+response1.oid_index
	if(IF_ip_INDEX1[19] != "1"):
		break;
	interfaces_index1.append(response1.value)

###############################################

response2 = s.get_next('.1.3.6.1.2.1.4.20.1.2')
interfaces_index2 = []
interfaces_index2.append(response2.value)
IF_ip_INDEX2 = response2.oid+'.'+response2.oid_index
while(IF_ip_INDEX2[20] == "2"):
	response2 = s.get_next(IF_ip_INDEX2)
	IF_ip_INDEX2 = response2.oid+'.'+response2.oid_index
	if(IF_ip_INDEX2[20] != "2"):
		break;
	interfaces_index2.append(response2.value)

###############################################

response = s.get_next('.1.3.6.1.2.1.4.20.1')
if_ip = []
if_ip.append(response.value)
IF_ip_INDEX = response.oid+'.'+response.oid_index
while(IF_ip_INDEX[20] == '1'):
	response = s.get_next(IF_ip_INDEX)
	IF_ip_INDEX = response.oid+'.'+response.oid_index
	if(IF_ip_INDEX[20] == '2'):
		break
	if_ip.append(response.value)

###############################################

IF_IP = if_ip
for i in range (len(interfaces_index1) - len(interfaces_index2)):
	IF_IP.append("−")

int_interfaces_index1 = [int(i) for i in interfaces_index1]
int_interfaces_index1 = [(i-1) for i in int_interfaces_index1]

int_interfaces_index2 = [int(i) for i in interfaces_index2]
int_interfaces_index2 = [(i-1) for i in int_interfaces_index2]
set_difference = set(int_interfaces_index1) - set(int_interfaces_index2)
list_difference = list(set_difference)
int_interfaces_index2 = int_interfaces_index2 + list_difference

interfaces_ip = []
for i in range (len(int_interfaces_index2)):
	interfaces_ip.append("−")

for i in range (len(int_interfaces_index2)):
	interfaces_ip[int_interfaces_index2[i]] = if_ip[i]

max_if_ip = len(interfaces_ip[0])
for i in range(1,len(interfaces_ip)):
    if len(interfaces_ip[i]) > max_if_ip:
        max_if_ip = len(interfaces_ip[i])

#######################################################################################################################

response = s.get_next('.1.3.6.1.2.1.2.2.1.7')
interfaces_status = []
interfaces_status.append(response.value)
IF_status_INDEX = response.oid+'.'+response.oid_index
while(IF_status_INDEX[19] == '7'):
	response = s.get_next(IF_status_INDEX)
	IF_status_INDEX = response.oid+'.'+response.oid_index
	if(IF_status_INDEX[19] == '8'):
		break
	interfaces_status.append(response.value)

for i in range(len(interfaces_status)):
	if(interfaces_status[i] == '1'):
		interfaces_status[i] = interfaces_status[i].replace('1',"UP")
	if(interfaces_status[i] == '2'):
		interfaces_status[i] = interfaces_status[i].replace('2',"DOWN")

max_if_status = len(interfaces_status[0])
for i in range(1,len(interfaces_status)):
    if len(interfaces_status[i]) > max_if_status:
        max_if_status = len(interfaces_status[i])
if max_if_status == 2:
    max_if_status += 4
else:
    max_if_status += 2

#######################################################################################################################

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
print("  ")

for i in range(len(interfaces_name)):
	if(interfaces_mac[i] != ':::::'):
		print(f"{{:{max_if_name+2}}}{{:{max_if_mac+2}}}{{:{max_if_ip+2}}}{{:{max_if_status+2}}}".format(interfaces_name[i][1:len(interfaces_name[i])-1], interfaces_mac[i][1:len(interfaces_mac[i])-2],interfaces_ip[i],interfaces_status[i]))
	if(interfaces_mac[i] == ':::::'):
		print(f"{{:{max_if_name+2}}}{{:{max_if_mac+2}}}{{:{max_if_ip+2}}}{{:{max_if_status+2}}}".format(interfaces_name[i][1:len(interfaces_name[i])-1], interfaces_mac[i],interfaces_ip[i],interfaces_status[i]))
