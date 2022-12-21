import socket, threading


HEADER_SIZE = 64


def send_text(sock: socket.socket, text: str):
    """Send text to server."""
    payload = text.encode('utf8')
    header = f'{len(payload):<{HEADER_SIZE}}'.encode('utf8')
    sock.sendall(header + payload)

def receive_text(sock: socket.socket) -> str:
    """Receive text from server."""
    header = sock.recv(HEADER_SIZE)
    while len(header) < HEADER_SIZE:
        header += sock.recv(HEADER_SIZE - len(header))
    payload_size = int(header.decode('utf8').strip())

    payload = sock.recv(payload_size)
    while len(payload) < payload_size:
        payload += sock.recv(payload - len(payload))
    return payload.decode('utf8')

def recv_loop(sock: socket.socket):
    """Receive text from server."""
    while True:
        text = receive_text(sock)
        print(text)

def main():
    """Main function."""
    
    username = input('Enter your username: ')
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8888))

    # Start receiving loop
    threading.Thread(target=recv_loop, args=(sock,), daemon=True).start()

    user_input = ''
    while user_input != 'exit':
        user_input = input()
        send_text(sock, f'{username}: {user_input}')

    
    sock.close()


if __name__ == '__main__':
    main()
