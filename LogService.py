import argparse
import socket
import datetime


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
                with conn:
                    print(f"Connection established from {addr}")
                    # Log the new connection
                    self.log_message("Connection established",
                                     addr, "New Connection")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break  # Exit the loop if no more data is received
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
