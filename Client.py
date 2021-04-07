# Include Python's Socket Library
from socket import *

# Define Server IP Address and Port
# serverName = 'localhost'
# serverPort = 12000
# Build Server Address Using IP Address and Port
# serverAddress=(serverName, serverPort)

# Create UDP Socket for Client
# clientSocket = socket(AF_INET, SOCK_DGRAM)

# This is the message received from the keyboard
# message = input('Input lowercase sentence:')

# Message sent to the Server
# clientSocket.sendto(message.encode(), serverAddress)

# Read reply characters from socket into string
# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# Print uot received string
# print(modifiedMessage.decode())

# Close the client socket
# clientSocket.close()

import socket
serverPort = 8000
host = gethostname().split('.')[0]
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, serverPort))
cmd_OK = 'GET {}:{}/test.html HTTP/1.1\r\n\r\n'.format(host, serverPort).encode()
cmd_not_found = 'GET {}:{}/dogg.html HTTP/1.1\r\n\r\n'.format(host, serverPort).encode()
cmd_bad_req = 'G@ETT {}:{}/test.html HTTP/1.1\r\n\r\n'.format(host, serverPort).encode()
clientSocket.send(cmd_OK)

while True:
    data = clientSocket.recv(512)
    if len(data) < 1:
        break
    print(data.decode(),end='')

clientSocket.close()