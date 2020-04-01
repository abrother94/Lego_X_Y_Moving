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

Move_D=180
ZeroPoint = [0,0,0]
ZoneA = [0,0,0]
ZoneB = [0,0,0]
X_Step=0
Y_Step=0
Z_Step=0
Setting=False
Rev=2
#Dbg=True
Dbg=False

def handle_client(client_socket):
    cmdstr = client_socket.recv(1024)
    cmdstr = cmdstr.decode('utf-8')
    if cmdstr == "Quit":
      client_socket.send("ACK".encode('utf-8'))
      client_socket.close()
      return True

    r_cmd,step = cmdstr.split(':')
    #print ("[*] Received cmd: %s:%s" % r_cmd, step)
    global Y_Step
    global X_Step
    global Z_Step

    if r_cmd == "Up":
      print("Up")
      tank_drive=MoveTank(OUTPUT_A, OUTPUT_D)
      MD=Move_D*int(step)
      if Dbg != True:
          tank_drive.on_for_degrees(SpeedPercent(25*Rev), SpeedPercent(25*Rev),MD)
      Y_Step += MD
      print(" X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
    elif r_cmd == "Down":
      print("Down")
      tank_drive=MoveTank(OUTPUT_A, OUTPUT_D)
      MD=Move_D*int(step)
      if Dbg != True:
          tank_drive.on_for_degrees(SpeedPercent(-25*Rev), SpeedPercent(-25*Rev),MD)
      Y_Step -= MD
      print(" X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
    #elif r_cmd == "Left":
    elif r_cmd == "Right":
      #print("Left")
      print("Right")
      tank_drive=MoveTank(OUTPUT_A, OUTPUT_D)
      MD=Move_D*int(step)
      if Dbg != True:
          tank_drive.on_for_degrees(SpeedPercent(25*Rev), SpeedPercent(-25*Rev),MD)
      X_Step -= MD
      print(" X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
    #elif r_cmd == "Right":
    elif r_cmd == "Left":
      #print("Right")
      print("Left")
      tank_drive=MoveTank(OUTPUT_A, OUTPUT_D)
      MD=Move_D*int(step)
      if Dbg != True:
          tank_drive.on_for_degrees(SpeedPercent(-25*Rev), SpeedPercent(25*Rev),MD)
      X_Step += MD
      print(" X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
    elif r_cmd == "ZeroP":
      print("Set Zero Point")
      ZeroPoint = [0,0,0]
      X_Step = 0
      Y_Step = 0
      Z_Step = 0
      print("Set B Zone X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
    elif r_cmd == "ZoneA":
      print("Set A Zone X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
      ZoneA = [X_Step,Y_Step,0]
      print(ZoneA)
    elif r_cmd == "ZoneB":
      print("Set B Zone X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
      ZoneB = [X_Step,Y_Step,0]
      print(ZoneB)
    elif r_cmd == "Gohome":
      print("Gohome!!!!....")
      tank_drive=MoveTank(OUTPUT_A, OUTPUT_D)
      if Y_Step < 0:
          print("Move Up...")
          if Dbg != True:
              tank_drive.on_for_degrees(SpeedPercent(25*Rev), SpeedPercent(25*Rev),abs(Y_Step))
          Y_Step += abs(Y_Step)
          print(" X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
      else:
          print("Move Down...")
          if Dbg != True:
              tank_drive.on_for_degrees(SpeedPercent(-25*Rev), SpeedPercent(-25*Rev),abs(Y_Step))
          Y_Step -= abs(Y_Step)
          print(" X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))

      if X_Step < 0:
          print("Move Right...")
          if Dbg != True:
             tank_drive.on_for_degrees(SpeedPercent(-25*Rev), SpeedPercent(25*Rev),abs(X_Step))
          X_Step += abs(X_Step)
          print(" X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
      else:
          print("Move Left...")
          if Dbg != True:
              tank_drive.on_for_degrees(SpeedPercent(25*Rev), SpeedPercent(-25*Rev),abs(X_Step))
          X_Step -= abs(X_Step)
          print(" X[%d] Y[%d] Z[%d]" % (X_Step, Y_Step, Z_Step))
    else:
      print("not support this kind of command!")
    client_socket.send("ACK".encode('utf-8'))
    client_socket.close()
while True:
    client, addr = server.accept()
    print ("[*] Acepted connection from: %s:%d" % (addr[0],addr[1]))
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
