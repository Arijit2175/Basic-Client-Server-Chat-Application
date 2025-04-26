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