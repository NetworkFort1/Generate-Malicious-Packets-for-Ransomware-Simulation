import socket
import threading
import json
import logging

class ControlServer:
    def __init__(self, host, port, log_file):
        self.host = host
        self.port = port
        self.server = None
        self.setup_logging(log_file)

    def setup_logging(self, log_file):
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def handle_client(self, connection, address):
        try:
            data = connection.recv(1024)
            if not data:
                return

            message = json.loads(data.decode())
            if 'request' in message and message['request'] == 'key':
                logging.info(f"Key request received from: {address}")
                # Instead of user input, you can generate a random key here
                key = "random_generated_key"
                response = json.dumps({'key': key})
                connection.sendall(response.encode())
                logging.info(f"Sent key: {key} to {address}")
            else:
                logging.info(f"Data received from {address}: {message}")
        except json.JSONDecodeError:
            logging.error("Invalid JSON data received.")
        finally:
            connection.close()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        logging.info(f"Server listening at {self.host}:{self.port}.")

        try:
            while True:
                connection, address = self.server.accept()
                logging.info(f"Connection established from {address}.")
                client_thread = threading.Thread(target=self.handle_client, args=(connection, address))
                client_thread.start()
        except KeyboardInterrupt:
            logging.info("Shutting down the server.")
        finally:
            self.server.close()

if __name__ == "__main__":
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 12345      # Port number
    LOG_FILE = 'server_log.txt'  # Name of the log file

    control_server = ControlServer(HOST, PORT, LOG_FILE)
    control_server.start()