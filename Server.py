import sys
import traceback
from datetime import datetime
from email.parser import BytesParser

# Importing the status code enum to reduce hard-coded strings
from http import HTTPStatus

from io import BytesIO
from os import stat
from socket import *

# Constants used in the code.
DATE_TIME_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
TEST_HTML = 'test.html'
HEAD = 'HEAD'
GET = 'GET'
IF_NONE_MATCH = 'If-None-Match'
IF_MODIFIED_SINCE = 'If-Modified-Since'
SERVER_PORT = 8000
CRLF = '\r\n'


def create_header(code):
    """
    Generate the response start line based on the given status code.
    """

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


def read_file(headers, requested_file_name, http_method_name):
    """
    Read a local HTML file.
    """

    requested_file_name = requested_file_name.split('/')[1]
    if requested_file_name == '' or requested_file_name == 'favicon.ico':
        requested_file_name = TEST_HTML

    try:
        last_modified = datetime.fromtimestamp(stat(requested_file_name).st_mtime)
        with open(requested_file_name) as file_in:
            if IF_MODIFIED_SINCE in headers and IF_NONE_MATCH not in headers:
                # Check last modified date.
                if_modified_since = datetime.strptime(headers[IF_MODIFIED_SINCE], DATE_TIME_FORMAT)
                if last_modified <= if_modified_since:
                    return create_header(HTTPStatus.NOT_MODIFIED)

            html_content = file_in.read()
            response = create_header(HTTPStatus.OK)
    except Exception as exc:
        print("Exception:", exc)
        response = create_header(HTTPStatus.NOT_FOUND)
        html_content = "<html><body><h1>Error 404: File not found</h1></body></html>"

    if http_method_name == 'GET':
        response += html_content

    return response


class Server:
    def __init__(self, port=SERVER_PORT):
        self.host = gethostname().split('.')[0]
        self.serverPort = port
        self.isRunning = True

    def start(self):
        """
        Create a single-threaded server socket listening and handling incoming requests.
        """

        try:
            with socket(AF_INET, SOCK_STREAM) as serverSocket:
                serverSocket.bind((self.host, self.serverPort))
                print("Starting server {}:{}".format(self.host, self.serverPort))
                serverSocket.listen(5)

                while self.isRunning:
                    client_socket, client_address = serverSocket.accept()
                    client_socket.settimeout(5)
                    try:
                        request = client_socket.recv(2048).decode().split(CRLF)
                        request_headers = BytesParser().parsebytes(request[1].encode())
                        start_line = request[0].split(' ')
                        http_method_name = start_line[0]
                        # print http body
                        decoded_msg = request[2]
                        if len(decoded_msg) > 0:
                            for i in range(0, len(decoded_msg)):
                                print("decoded msg: ", decoded_msg[i])
                            print("---------------------------------")

                        if http_method_name == GET or http_method_name == HEAD:
                            requested_file_name = start_line[1]
                            response = read_file(request_headers, requested_file_name, http_method_name)
                            print(response)
                            client_socket.sendall(response.encode())
                            client_socket.shutdown(SHUT_WR)
                        else:  # bad request
                            response = create_header(400)
                            response += "<html><body><h1>Error 400: Bad Request</h1></body></html>"
                            client_socket.sendall(response.encode())
                            client_socket.shutdown(SHUT_WR)
                    except timeout:
                        print("408 Request Timed Out")
                        timeout_header = create_header(HTTPStatus.REQUEST_TIMEOUT)
                        client_socket.sendall(timeout_header.encode())
                        client_socket.shutdown(SHUT_WR)
        except KeyboardInterrupt:
            print("\nShutting down...\n")
            self.stop()
        except Exception as exc:
            self.stop()
            print("Error: \n")
            print(exc)
            print(traceback.format_exc())
            sys.exit(1)

    def stop(self):
        """
        Set isRunning to stop.
        """

        self.isRunning = False


if __name__ == '__main__':
    tcp_server = Server()
    tcp_server.start()
