import argparse
import socket
import datetime
import threading
from collections import deque
import time


class LoggingService:
    def __init__(self, host, port, format):
        self.host = host
        self.port = port
        self.format = format

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Logging service started on {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                print(f"Connection established from {addr}")
                # Log the new connection
                self.log_message("Connection established",
                                 addr, "New Connection")
                # Start a new thread that will handle the client
                client_thread = threading.Thread(
                    target=self.handle_client, args=(conn, addr))
                client_thread.start()

    def handle_client(self, conn, addr):
        # Keep track of the last 10 request times
        request_times = deque(maxlen=10)

        with conn:
            while True:
                if len(request_times) == 10 and time.time() - request_times[0] < 1:
                    # If the client has made 10 requests in less than 1 second, disconnect them
                    self.log_message("Too many requests", addr, "WARNING")
                    break

                data = conn.recv(1024)
                if not data:
                    break  # Exit the loop if no more data is received

                # Add the current time to the request times
                request_times.append(time.time())

                message = data.decode()
                self.log_message(message, addr)

    def log_message(self, message, addr, level='INFO'):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip, port = addr
        formatted_message = self.format.format(
            level=level, timestamp=timestamp, ip=ip, port=port, message=message)
        with open("logfile.txt", "a") as log_file:
            log_file.write(formatted_message + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start a logging service.')
    parser.add_argument('--host', type=str, required=True,
                        help='The host to bind the logging service to.')
    parser.add_argument('--port', type=int, required=True,
                        help='The port to bind the logging service to.')
    parser.add_argument('--format', type=str, required=True,
                        help='The format for log messages.')
    args = parser.parse_args()

    logging_service = LoggingService(args.host, args.port, args.format)
    logging_service.start()
