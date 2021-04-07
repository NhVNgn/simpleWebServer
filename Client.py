from socket import *
import Constants


HOST = gethostname().split('.')[0]
CMD_OK = 'GET {}:{}/test.html HTTP/1.1\r\n\r\n'.format(HOST, Constants.SERVER_PORT).encode()
CMD_NOT_FOUND = 'GET {}:{}/dogg.html HTTP/1.1\r\n\r\n'.format(HOST, Constants.SERVER_PORT).encode()
CMD_BAD_REQ = 'G@ETT {}:{}/test.html HTTP/1.1\r\n\r\n'.format(HOST, Constants.SERVER_PORT).encode()


if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as clientSocket:
        clientSocket.connect((HOST, Constants.SERVER_PORT))
        clientSocket.send(CMD_OK)

        while True:
            data = clientSocket.recv(512)
            if len(data) < 1:
                break
            print(data.decode(), end='')
