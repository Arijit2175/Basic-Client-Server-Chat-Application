import socket 
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    threading.Thread(target=receive_messages, args=(client,)).start()

    while True:
        message = input()
        client.send(message.encode('utf-8'))

start_client()