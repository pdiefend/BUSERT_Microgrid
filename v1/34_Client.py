# 3_4_Server.py

# Echo server program
import socket

HOST = 'localhost'                 # Symbolic name meaning the local host
PORT = 50010              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((HOST, PORT))
#s.listen(1)
#conn, addr = s.accept()
#print('Connected by', addr)
s.connect((HOST, PORT))

while 1:
    data = s.recv(1024)
    print(data.decode())
    st = input('S-> ')
    s.send(st.encode())
    st = input('C-> ')
    s.send(st.encode())
    if (st == 'close'):
        data = s.recv(1024)
        break
    
s.close()

# accept a connection
# receive the list of switches and parse it in to a list

# when ready to access wemos send the name of the wemo you want to access
# and the command or the name of the function you want to run

# then wait for the acknowledgement

# close the socket by sending close in the command line then
# wait for the client to disconnect
