import socket
import threading

def handle_client(client_socket):
    """Handle incoming messages from a client."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received message: {message}")
                # Broadcast the message to all clients
                for client in clients:
                    if client != client_socket:
                        client.send(message.encode('utf-8'))
            else:
                break
        except:
            break
    client_socket.close()
    clients.remove(client_socket)

# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen(5)
clients = []

print("Server started. Waiting for connections...")

while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr}")
    clients.append(client_socket)
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
