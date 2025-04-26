import socket
import threading
import sys
import signal

clients = []
server_running = True  

def broadcast(message, client):
    """Send the message to all clients except the sender."""
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                clients.remove(c)

def handle_client(client):
    """Handle communication with each connected client."""
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

def shutdown_server(server):
    """Gracefully shutdown the server."""
    global server_running
    server_running = False
    print("\nServer is shutting down...")
    for client in clients:
        client.close()
    server.close()
    sys.exit(0)  

def start_server():
    """Start the server and accept incoming client connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server is running and waiting for connections...")

    signal.signal(signal.SIGINT, lambda sig, frame: shutdown_server(server))

    try:
        while server_running:
            client, addr = server.accept()
            clients.append(client)
            print(f"New connection: {addr}")
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
    except Exception as e:
        print(f"Error: {e}")
        shutdown_server(server)

start_server()
