#!/usr/bin/python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.unit import DistanceCentimeters
import socket
import threading
import string 
bind_ip = "0.0.0.0"
bind_port = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print ("[*] Listening on %s:%d" % (bind_ip, bind_port))
def handle_client(client_socket):
    cmdstr = client_socket.recv(1024)
    cmdstr = cmdstr.decode('utf-8')
    move_to,step = cmdstr.split(':') 
    #print ("[*] Received cmd: %s:%s" % move_to, step)
    if move_to == "Up":
      print("Up")
      tank_drive=MoveTank(OUTPUT_A, OUTPUT_D)
      #tank_drive.on_for_seconds(SpeedPercent(50), SpeedPercent(50), 0.3)
      tank_drive.on_for_degrees(SpeedPercent(25), SpeedPercent(25),180*int(step))
    elif move_to == "Down":
      print("Down")
      tank_drive=MoveTank(OUTPUT_A, OUTPUT_D)
      tank_drive.on_for_degrees(SpeedPercent(-25), SpeedPercent(-25),180*int(step))
    elif move_to == "Left":
      print("Left")
      tank_drive=MoveTank(OUTPUT_A, OUTPUT_D)
      tank_drive.on_for_degrees(SpeedPercent(25), SpeedPercent(-25),180*int(step))
    elif move_to == "Right":
      print("Right")
      tank_drive=MoveTank(OUTPUT_A, OUTPUT_D)
      tank_drive.on_for_degrees(SpeedPercent(-25), SpeedPercent(25),180*int(step))
    else:
      print("not support this kind of command!")
    client_socket.send("ACK".encode('utf-8'))
    client_socket.close()
while True:
    client, addr = server.accept()
    print ("[*] Acepted connection from: %s:%d" % (addr[0],addr[1]))
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
