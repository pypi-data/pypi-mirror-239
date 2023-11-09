import os
import socket
import threading

EXT_TEXT = ["html", "js", "css"]
EXT_IMG = ["jpg", "jpeg", "png", "ico"]


class HTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code} {message}")


class Server:
    host: str
    port: int
    search_for: str
    path: str

    def __init__(
        self,
        host_: str = "localhost",
        port_: int = 8080,
        search_for_: str = "index.html",
        base_path: str = "."
    ) -> None:
        self.host = host_
        self.port = port_
        self.search_for = search_for_
        self.path = base_path

    def arrange_path(self, path):
        path = path.split("?")[0]

        while len(path) > 0 and path[0] in ["/", "\\"]:
            path = path[1:]

        while len(path) > 0 and path[-1] in ["/", "\\"]:
            path = path[:-1]

        if "." not in path.split("/")[-1]:
            path +=  f"{'/' if len(path)>0 else ''}{self.search_for}"

        return os.path

    def parse_request(self, request):
        if request == "":
            raise HTTPError(400, "Not a http request.")

        rows = request.split("\r\n")
        print(rows[0])
        method, path, _ = rows[0].split(" ")

        if method != "GET":
            raise HTTPError(405, "Method not allowed")

        path = self.arrange_path(path)
        path = os.path.join(self.path, path)

        return path, path.split(".")[-1]

    @staticmethod
    def send_file_as_text_response(path, client_socket):
        content_type = {
            "css":"css",
            "html":"html",
            "js":"javascript"
        }[path.split(".")[-1]]
        with open(path, "r") as fp:
            content = fp.read()
            response = f"HTTP/1.1 {200} OK\r\nContent-Type: text/{content_type}\r\n\r\n{content}"
            client_socket.sendall(response.encode("utf-8"))

    @staticmethod
    def send_file_as_image_response(path, client_socket):
        with open(path, 'rb') as file:
            image_data = file.read()

        response = b"HTTP/1.1 200 OK\r\n"
        response += b"Content-Type: image/png\r\n"
        response += b"Content-Length: " + str(len(image_data)).encode() + b"\r\n"
        response += b"\r\n"
        response += image_data

        client_socket.sendall(response)


    def respond_request(self, client_socket, request):
        try:
            path, ext = self.parse_request(request)
            if not os.path.exists(path):
                raise HTTPError(404, "Not Found")
            if ext in EXT_TEXT:
                self.send_file_as_text_response(path, client_socket)
            elif ext in EXT_IMG:
                self.send_file_as_image_response(path, client_socket)
            else:
                raise HTTPError(406, "Not Acceptable. Extension")
        except HTTPError as err:
            print(err)
            response = f"HTTP/1.1 {err.status_code} OK\r\nContent-Type: text/html\r\n\r\n{err.message}"
            client_socket.sendall(response.encode("utf-8"))
        finally:
            client_socket.close()


    def start_listener(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind((self.host, self.port))
        listener.listen(1)
        print(f"Listening ...\nhttp://{self.host}:{self.port}")

        while True:
            client_socket, _ = listener.accept()
            request = client_socket.recv(1024).decode("utf-8")
            threading.Thread(target=self.respond_request, args=(client_socket, request,)).start()
