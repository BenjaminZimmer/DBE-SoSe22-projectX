import errno
import imp
import socket
import sys
from threading import Thread

# Header Utils
LENGTH_HEADER_SIZE = 8
USER_HEADER_SIZE = 16

# Function for formatting the messages to dynamically calculate buffersize


def format_message(username, message):
    if not message:
        return None
    length_header = f'{len(message):<{LENGTH_HEADER_SIZE}}'
    user_header = f'{username:<{USER_HEADER_SIZE}}'
    return f'{length_header}{user_header}{message}'
# Header Utils End


IP = '127.0.0.1'
PORT = 5555
username = ''

# Creating a username for each new participant
while not username:
    username = input('Please enter a username (max. 16 characters)')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# Function for sending messages as a client


def send():
    message = input(f'{username} > ')
    if message == '[exit]':
        message = format_message(username, 'Signing out')
        client_socket.send(message.encode('utf-8'))
        print('Signed out')
        client_socket.close()
        sys.exit()
    elif message:
        message = format_message(username, message).encode('utf-8')
        client_socket.send(message)

# Function for receiving messages that are sent from other clients via server


def receive():
    try:
        message_size = client_socket.recv(LENGTH_HEADER_SIZE)
        if message_size:
            message_size = int(message_size.decode('utf-8').strip())
            sender = client_socket.recv(
                USER_HEADER_SIZE).decode('utf-8').strip()
            message = client_socket.recv(message_size).decode('utf-8')
            print(f'\n{sender} > {message}\n{username} > ')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Encountered error while readeing', e)
            client_socket.close()
            sys.exit()
    except Exception as e:
        client_socket.close()
        sys.exit()

# Function to receive messages when there are some


def loop_receive():
    while True:
        receive()


receive_thread = Thread(target=loop_receive)
receive_thread.start()
while True:
    send()
