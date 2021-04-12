from socket import *

# Constants
SERVER_PORT = 8000
CHUNK_SIZE = 2048
HTTP_VERSION = 1.1
CRLF = "\r\n\r\n"
HOST = gethostname().split('.')[0]
IF_MODIFIED_HEADER = 'If-Modified-Since: Wed, 9 Apr 2021 07:28:00 GMT'
SERVER_URL = '{}:{}'.format(HOST, SERVER_PORT)
CMD_OK = 'GET {}/test.html HTTP/1.1\r\n\r\n'.format(SERVER_URL).encode()
CMD_NOT_FOUND = 'GET {}/dogg.html HTTP/1.1\r\n\r\n'.format(SERVER_URL).encode()
CMD_BAD_REQ = 'G@ETT {}/test.html HTTP/1.1\r\n\r\n'.format(SERVER_URL).encode()
CMD_MODIFIED = 'GET {}/test.html HTTP/1.1\r\n{}\r\n\r\n'.format(SERVER_URL, IF_MODIFIED_HEADER).encode()

if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as clientSocket:
        clientSocket.connect((HOST, SERVER_PORT))
        # clientSocket.send(CMD_OK)

        while True:
            data = clientSocket.recv(512)
            if len(data) < 1:
                break
            print(data.decode(), end='')
