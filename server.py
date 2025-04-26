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

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server is running and waiting for connections...")

    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f"New connection: {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

start_server()