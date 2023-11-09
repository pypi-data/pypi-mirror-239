from varwwwhtml.server import Server
from argparse import ArgumentParser

argParser = ArgumentParser(description="CLI tool that allows you to serve your static web app.")
argParser.add_argument("--host", type=str, default="localhost", help="Host to serve on")
argParser.add_argument("--port", type=int, default=8080, help="Port to serve on")
argParser.add_argument("--path", type=str, default=".", help="Path where static files in")
argParser.add_argument("--search-for", type=str, default="index.html", help="File to search for if path is a directory")

args = argParser.parse_args()

def run_server():
    server = Server(host_=args.host, port_=args.port, search_for_=args.search_for, base_path=args.path)
    server.start_listener()

if __name__ == '__main__':
    run_server()