import socket
import threading

def receive_messages(client_socket):
    """Receive messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"New message: {message}")
            else:
                break
        except:
            break

def main():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))
    
    # Start the receive thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    
    # Send messages to the server
    while True:
        message = input()
        if message:
            client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    main()
