import sys
import socket                      #create socket 
from urllib.parse import urlparse #to parse absolute URI
from pathlib import Path           # create cache folder 

"""
@Purpose: This program implements a basic web proxy server that handles simple GET requests for HTML files.
          It includes a file-based caching mechanism to reduce repeated server calls for previously fetched pages.
          The proxy listens for one request per execution, and handles malformed requests gracefully.

@Author: Randy Rizo 
@Course: CPSC5510 - Computer Networks
@Date: 4/23/2025
@Version: 1.0
"""

""" @Purpose: create proxy class and constructor
 """

class Proxy:
    def __init__(self, port):
        self.port = port
        self.cache_dir = Path("cache")

        """@Purpose: start socket listener and listen for requests. """

    def start(self):
        print("\n **** Ready to connect ****")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            # re use port after restarting 
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #bind to all networks 
            listener.bind(("0.0.0.0", self.port)) 
            #allow only one cnnection
            listener.listen(1)

            #conn new socket obj 
            #addr is the IP address 

            conn, addr = listener.accept()
            print(f"Received a client connection from {addr}")
            with conn:
                self.handle_client(conn)

        print("All done! Closing socket...")

        """@Purpose: handle client HTTP request """
        

    def handle_client(self, conn):
        request_data = conn.recv(1024)
        print(f"Received a message from this client: {request_data}")

        try:
            #get first line of request 
            request_line = request_data.decode().split("\r\n")[0]
            method, full_url, http_version = request_line.split()

            if method != "GET":
                print("[!] Only GET is supported. Rejecting request.")
                return

            if http_version != "HTTP/1.1":
                print("!!!Only HTTP/1.1 is supported. Rejecting request!!!")
                return

        except ValueError:
            print(" !!!500 Malformed request!!!!")
            return
        # parse URL
        parsed_url = urlparse(full_url)
        host = parsed_url.hostname
        path = parsed_url.path or "/"
        port = parsed_url.port or 80

        # create cache folder 

        safe_path = path.lstrip("/") or "index.html"
        cache_path = self.cache_dir / host / safe_path
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        if cache_path.exists():
            print("Yay! The requested file is in the cache...")
            self.serve_from_cache(conn, cache_path)
        else:
            print("Oops! No cache hit! Requesting origin server for the file...")
            self.fetch_and_cache(conn, host, port, path, cache_path)

        print("Now responding to the client...")

    """
      @Purpose: if cache hit exists serve from cache, serve from the cache
      """

    def serve_from_cache(self, conn, cache_path):
        with open(cache_path, "rb") as f:
            content = f.read()

        headers = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(content)}\r\n"
            f"Connection: close\r\n"
            f"Content-Type: text/html\r\n"
            f"Cache-Hit: 1\r\n\r\n"
        )
        conn.sendall(headers.encode() + content)

        
        """@Purpose; Send all from socket to server and cache if no cache hit and status code 200 """

    def fetch_and_cache(self, conn, host, port, path, cache_path):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((host, port))

            request = (
                f"GET {path} HTTP/1.1\r\n"
                f"host: {host}\r\n"
                f"Connection: close\r\n\r\n"
            )

            print("Sending the following message from proxy to server:")
            print(request.strip())

            server_socket.sendall(request.encode())

            response = bytearray()
            while True:
                chunk = server_socket.recv(4096)
                if not chunk:
                    break
                response.extend(chunk)

        header_part, _, body = response.partition(b"\r\n\r\n")
        status_line = header_part.decode(errors='ignore').split("\r\n")[0]

        if "200 OK" in status_line:
            print("Response received from server, and status code is 200! Write to cache, save time next time...")
            with open(cache_path, "wb") as f:
                f.write(body)
            conn.sendall(response)
        elif "404" in status_line:
            print("Response received from server, status 404! NOT FOUND ")
            not_found_response = (
                    f"HTTP/1.1 404 Not Found\r\n"
                    f"Cache-Hit: 0\r\n"
                    f"Content-Type: text/html\r\n"
                    f"Connection: close\r\n\r\n"
                    f"<html><body><h1>404 Not Found</h1><p>The requested resource could not be found.</p></body></html>"
                    )
            conn.sendall(not_found_response.encode())
        else:
            print("Response received from server, but status code is not 200! No cache writing...")
            conn.sendall(header_part + b"\r\nCache-Hit: 0\r\n\r\n" + body)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 proxy.py <PORT>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Port must be an integer.")
        sys.exit(1)

    proxy = Proxy(port)
    proxy.start()
