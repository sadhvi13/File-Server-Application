import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
port = 1028
address = (IP, port)
#client socket creation
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)
#connection established
size = 1024
format = "utf-8"
while True:
#taking input
    inp = input("enter client request:")
#sending message to server
    client.send(inp.encode(format))
    if inp == "listallfiles":
        serverMessage = client.recv(size).decode(format)
        filenames = serverMessage
        print(filenames)
        filenames = filenames.split()
    if inp == "exit":
        serverMessage = client.recv(size).decode(format)
        print(serverMessage)
#closing client sockt
        client.close()
        break
    clientRequest = inp.split()
    if "download" in clientRequest:
#multiple files receiving
        if clientRequest[1] == "all":
            fileslist = client.recv(size).decode(format)
            allfiles = fileslist
            fileslist = fileslist.split()
            for x in fileslist:
                udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udpPort = 1029
                udpAddress = (IP, udpPort)
                udpSocket.bind(udpAddress)
                file = open(x, "wb")
                while True:
                    fileAddressPair = udpSocket.recvfrom(size)
                    fileInbytes = fileAddressPair[0]
                    s = fileInbytes.decode(format)
                    if s == "file transfer over":
                        break
                    file.write(fileInbytes)
                file.close()
                udpSocket.close()
            print("downloaded ", allfiles)
        else:
#single file receiving
            udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpPort = 1029
            udpAddress = (IP, udpPort)
            udpSocket.bind(udpAddress)
            file = open(clientRequest[1], "wb")
            while True:
                fileAddressPair = udpSocket.recvfrom(size)
                fileInbytes = fileAddressPair[0]
                s = fileInbytes.decode(format)
                if s == "file transfer over":
                    break
                file.write(fileInbytes)
            file.close()
            print("downloaded ",clientRequest[1])
#closing UDP client socket
            udpSocket.close()
