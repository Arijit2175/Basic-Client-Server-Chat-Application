import socket
import threading
import sys

clients = {}
client_names = {}

def broadcast_clients():
    """Send the list of connected clients to all clients."""
    client_list = ','.join(client_names.values())
    for client in clients.values():
        try:
            client.send(f"CLIENT_LIST:{client_list}".encode('utf-8'))
        except:
            pass

def handle_client(client, addr):
    """Handle communication with each connected client."""
    client_name = f"Client {addr[1]}"
    client_names[client] = client_name
    clients[client_name] = client
    print(f"{client_name} connected")
    
    broadcast_clients()  

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith("PRIVATE:"):
                target_client_name = message.split(":")[1].split(" ")[0]
                private_message = " ".join(message.split(":")[1].split(" ")[1:])
                if target_client_name in clients:
                    clients[target_client_name].send(f"PRIVATE {client_name}: {private_message}".encode('utf-8'))
            elif message:
                broadcast(message, client, client_name)
        except:
            break

    del clients[client_name]
    del client_names[client]
    client.close()
    broadcast_clients()

def broadcast(message, client, client_name):
    """Send the message to all clients except the sender."""
    for c in clients.values():
        if c != client:
            try:
                c.send(f"{client_name}: {message}".encode('utf-8'))
            except:
                clients.remove(c)

def start_server():
    """Start the server and accept incoming client connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server is running and waiting for connections...")

    global running
    try:
        while True:
            client, addr = server.accept()
            threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        for client in clients.values():
            client.close()
        server.close()
        sys.exit(0)  

start_server()
