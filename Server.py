# Include Python's Socket Library
from socket import *

# Define Server Port
# serverPort = 12000

# Create UDP Socket
# serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to local port 12000
# serverSocket.bind(('', serverPort))

# while True: # Forever Loop
    # Read from UDP Socket into message & client address
    # message, clientAddress = serverSocket.recvfrom(2048)
    
    # Uppder Case (as the simple function intended)
    # modifiedMessage = message.decode().upper()
    
    # Send the upper case string back to the same client
    # serverSocket.sendto(modifiedMessage.encode(), clientAddress)

serverPort = 8000
def createServer():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', serverPort))
        serverSocket.listen(5)
        while True:
            clientSocket, clientAddress = serverSocket.accept()
            message = clientSocket.recv(5000).decode()
            decoded_msg = message.split("\n")
            if (len(decoded_msg) > 0):
                for i in range (0,len(decoded_msg)):
                    print("decoded msg: ", decoded_msg[i])
                print("-------------------------------")

            fin = open('test.html')
            content = fin.read()
            fin.close()
            response = "HTTP/1.1 200 OK\r\n" + content
            clientSocket.sendall(response.encode())
            clientSocket.shutdown(SHUT_WR)

    except KeyboardInterrupt :
        print("\nShutting down...\n")
    except Exception as exc :
        print("Error:\n")
        print(exc)

    serverSocket.close()   


print("Access localhost")
createServer()