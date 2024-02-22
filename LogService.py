import socket


class LoggingService:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Logging service started on {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Connection established from {addr}")
                    data = conn.recv(1024)
                    if data:
                        message = data.decode()
                        self.log_message(message)

    def log_message(self, message):
        with open("logfile.txt", "a") as log_file:
            log_file.write(message + "\n")


if __name__ == "__main__":
    logging_service = LoggingService("10.169.92.126", 5300)
    logging_service.start()
