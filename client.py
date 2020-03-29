#!/usr/bin/python3
import sys
 
"""
TCP Client sample
"""
 
import socket
 
target_host = "192.168.1.115"
target_port = 9999 
 
# create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send(sys.argv[1].encode('utf-8'))
response = client.recv(4096)
