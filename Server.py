from http import HTTPStatus
from socket import *
import Constants
import sys
import traceback
# serverPort = 8000
# def createServer():
#     serverSocket = socket(AF_INET, SOCK_STREAM)
#     try:
#         serverSocket.bind(('localhost', serverPort))
#         serverSocket.listen(5)
#         while True:
#             clientSocket, clientAddress = serverSocket.accept()
#             message = clientSocket.recv(5000).decode()
#             decoded_msg = message.split("\n")
#             if (len(decoded_msg) > 0):
#                 for i in range (0,len(decoded_msg)):
#                     print("decoded msg: ", decoded_msg[i])
#                 print("-------------------------------")

#             fin = open('test.html')
#             content = fin.read()
#             fin.close()
#             response = "HTTP/1.1 200 OK\r\n" + content
#             clientSocket.sendall(response.encode())
#             clientSocket.shutdown(SHUT_WR)

#     except KeyboardInterrupt :
#         print("\nShutting down...\n")
#     except Exception as exc :
#         print("Error:\n")
#         print(exc)

#     serverSocket.close()


# print("Access localhost")
# createServer()

class Server:
    def __init__(self, port=Constants.SERVER_PORT):
        self.host = gethostname().split('.')[0]
        self.serverPort = port
        self.isRunning = True

    def createdHeader(self, code):
        header = ''
        if code == HTTPStatus.OK:
            header += 'HTTP/1.1 200 OK\n'
        elif code == HTTPStatus.NOT_MODIFIED:
            header += 'HTTP/1.1 304 Not Modified\n'
        elif code == HTTPStatus.BAD_REQUEST:
            header += 'HTTP/1.1 400 Bad Request\n'
        elif code == HTTPStatus.NOT_FOUND:
            header += 'HTTP/1.1 404 Not Found\n'
        elif code == HTTPStatus.REQUEST_TIMEOUT:
            header += 'HTTP/1.1 408 Request Timed Out\n'
        return header

    def ReadFile(self, requested_file_name, http_method_name):
        requested_file_name = requested_file_name.split('/')[1]
        if requested_file_name == "" or requested_file_name == "favicon.ico":
            requested_file_name = "test.html"

        html_content = ''
        try:
            file_in = open(requested_file_name)
            if http_method_name == "GET":
                html_content = file_in.read()
            file_in.close()
            header = self.createdHeader(HTTPStatus.OK)
        except Exception as exc:
            print("Exception:", exc)
            header = self.createdHeader(HTTPStatus.NOT_FOUND)
            html_content = "<html><body><h1>Error 404: File not found</h1></body></html>"

        response = header
        if http_method_name == "GET":
            response += html_content
        return response

    def start(self):
        try:
            with socket(AF_INET, SOCK_STREAM) as serverSocket:
                serverSocket.bind((self.host, self.serverPort))
                print("Starting server {}:{}".format(self.host, self.serverPort))
                serverSocket.listen(5)

                while self.isRunning:
                    clientSocket, clientAddress = serverSocket.accept()
                    message = clientSocket.recv(5000).decode()
                    http_method_name = message.split(' ')[0]
                    # print http body
                    decoded_msg = message.split("\n")
                    if (len(decoded_msg) > 0):
                        for i in range(0, len(decoded_msg)):
                            print("decoded msg: ", decoded_msg[i])
                        print("---------------------------------")

                    if http_method_name == "GET" or http_method_name == "HEAD":
                        requested_file_name = message.split(' ')[1]
                        response = self.ReadFile(requested_file_name, http_method_name)
                        print(response)
                        clientSocket.sendall(response.encode())
                        clientSocket.shutdown(SHUT_WR)  
                    else:  # bad request
                        response = self.createdHeader(400)
                        response += "<html><body><h1>Error 400: Bad Request</h1></body></html>"
                        clientSocket.sendall(response.encode())
                        clientSocket.shutdown(SHUT_WR)

        except KeyboardInterrupt:
            print("\nShutting down...\n")
        except Exception as exc:
            print("Error: \n")
            print(exc)
            print(traceback.format_exc())
            sys.exit(1)

    def stop(self):
        self.isRunning = False


if __name__ == '__main__':
    tcp_server = Server()
    tcp_server.start()
