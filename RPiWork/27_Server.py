# 2_7_Client.py

# Echo client program
import socket
from ouimeaux.environment import Environment

env = Environment()
env.start()

switches = list()

env.discover(seconds=3)

switchesList = env.list_switches()
#switches = list()

for s in switchesList:
    switches.append(env.get_switch(s))

str_switches = ', '.join(switchesList) # to be sent to server



HOST = 'localhost'    # The remote host
PORT = 50010          # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, PORT))
s.bind((HOST, PORT))

print('Ready for Connections')

while 1:
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    
    conn.send(str_switches)
    
    while 1:
        # receive 2 strings <switch>, <command>
        # parse which switch is which... 
        switch = conn.recv(1024).decode()
        command = conn.recv(1024).decode()
    
        print(switch + ', ' + command)    
    
        indx = 99
    
        try:
            indx = switchesList.index(switch)
        except ValueError:
            response = 'nak'
            if (command == 'close'):
                break
            command = 'err'
    
        response = ' '
    
        try:
            # perfrom the command
            if (command == 'on'):
                switches[indx].on()
                response = 'ack'
            elif (command == 'off'):
                switches[indx].off()
                response = 'ack'
            elif (command == 'toggle'):
                switches[indx].toggle()
                response = 'ack'
            elif (command == 'status'):
                response = '%d' % switches[indx].get_state()
            elif (command == 'current_power'):
                # print('power')
                # reponse = 'val: ' + str(switches[indx].current_power)
                response = '%d' % switches[indx].current_power
            elif (command == 'today_kwh'):
                # print('kwh')
                # reponse = 'val: ' + str(switches[indx].today_kwh)
                response = '%.5f' % switches[indx].today_kwh
            elif (command == 'close'):
                reponse = 'ack'
                break
            else:
                response = 'nak'
        except AttributeError:
            response = 'nak'
    
        conn.send(response.encode())
        print(response)
    
    
    #data = s.recv(1024)
    conn.close()
    
    
print('Stopping Server')
