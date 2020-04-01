#!/usr/bin/python3
from argparse import ArgumentParser
import sys

"""
TCP Client sample
"""

import socket
#Home
#target_host = "192.168.1.115"
#Labs
target_host = "172.17.8.237"
target_port = 9999
parser = ArgumentParser(description="Control ev3dev Robot !!")
parser.add_argument("Action", help="Up Down Right Left ZeroP ZoneA ZoneB Gohome")
parser.add_argument("Step", help="1~5")
args = parser.parse_args()

args = parser.parse_args()
print( len( vars(args) ) )

print("Action arg:", args.Action)
print("Step arg:", args.Step)
SndCmd=args.Action + ":" + args.Step
print(SndCmd)
# create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send(SndCmd.encode('utf-8'))
response = client.recv(4096)
