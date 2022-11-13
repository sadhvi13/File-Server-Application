import socket
import os
import threading

IP = socket.gethostbyname(socket.gethostname())
port = 1028
address = (IP, port)
#TCP socket creation
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)
server.listen()
print("server is running")
format = "utf-8"
size = 1024
#Tcp connection established
connection, addr = server.accept()
#list of files in server directory
fileslist = os.listdir()
files = ' '.join(fileslist)
while True:
    clientMessage = connection.recv(size).decode(format)
    if clientMessage == "listallfiles":
        connection.send(files.encode(format))
    elif clientMessage == "exit":
        connection.send("exitting".encode(format))
#closing server sockets
        connection.close()
        server.close()
        break
    else:
        message = clientMessage.split()
        #sending multiple files
        if "download" in message:
            if message[1] == "all":
                connection.send(files.encode(format))
                for x in fileslist:
                    file = open(x, "r")
                    data = file.read(size)
                    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    udpPort = 1029
                    udpAddress = (IP, udpPort)
                    while (data):
                        udpSocket.sendto(str.encode(data), udpAddress)
                        data = file.read(size)
                    udpSocket.sendto(str.encode("file transfer over"), udpAddress)
                    file.close()
                    import time
                    time.sleep(0.05)
                    udpSocket.close()
#sending single file
            else:
                filename = message[1]
                file = open(filename, "r")
                data = file.read(size)
                udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udpPort = 1029
                udpAddress = (IP, udpPort)
                while (data):
                    udpSocket.sendto(str.encode(data), udpAddress)
                    data = file.read(size)
                udpSocket.sendto(str.encode("file transfer over"), udpAddress)
                udpSocket.close()
                file.close()




