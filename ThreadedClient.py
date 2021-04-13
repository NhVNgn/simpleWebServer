import threading
from socket import *

# Constants
SERVER_PORT = 8000
HOST = gethostname().split('.')[0]
IF_MODIFIED_HEADER = 'If-Modified-Since: Wed, 9 Apr 2021 07:28:00 GMT'
SERVER_URL = '{}:{}'.format(HOST, SERVER_PORT)
CMD_OK = 'GET {}/test.html HTTP/1.1\r\n\r\n'.format(SERVER_URL).encode()
CMD_MODIFIED = 'GET {}/test.html HTTP/1.1\r\n{}\r\n\r\n'.format(SERVER_URL, IF_MODIFIED_HEADER).encode()


def client_thread(msg):
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, SERVER_PORT))
        while True:
            client_socket.send(msg)
            data = client_socket.recv(512)
            if len(data) < 1:
                return
            print("Thread id: {}".format(threading.get_ident()))
            print(data.decode(), end='')


if __name__ == '__main__':
    try:
        ok_thread = threading.Thread(target=client_thread, args=[CMD_OK])
        modified_thread = threading.Thread(target=client_thread, args=[CMD_MODIFIED])
        ok_thread.start()
        modified_thread.start()
    except KeyboardInterrupt:
        print("Shutting down multi-threaded client.")
        sys.exit(1)
