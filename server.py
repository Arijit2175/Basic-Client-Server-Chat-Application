import socket
import threading
import sys

#List of connected clients
clients = []

def broadcast(message, client, client_name):
    """Send the message to all clients except the sender."""
    for c in clients:
        if c != client:
            try:
                c.send(f"{client_name}: {message}".encode('utf-8'))
            except:
                #Remove the client if sending fails
                clients.remove(c)

def handle_client(client, addr):
    """Handle communication with each connected client."""
    client_name = f"Client {addr[1]}"  # Unique name for each client based on port number
    print(f"{client_name} connected")
    
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                broadcast(message, client, client_name)
            else:
                break
        except:
            break
    clients.remove(client)
    client.close()

def start_server():
    """Start the server and accept incoming client connections."""
    #Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server is running and waiting for connections...")

    try:
        while True:
            client, addr = server.accept()
            clients.append(client)
            threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        for client in clients:
            client.close()
        server.close()
        sys.exit(0)

# Start the server
start_server()
