import socket
import threading

clients = []

def broadcast(message, client):
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                clients.remove(c)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)
            else:
                break
        except:
            break
    clients.remove(client)
    client.close()