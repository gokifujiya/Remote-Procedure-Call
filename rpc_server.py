import socket
import json
import os
from rpc_functions import floor, nroot, reverse, validAnagram, sort

SOCKET_PATH = "./socket_file"

# Function registry
function_map = {
    "floor": floor,
    "nroot": nroot,
    "reverse": reverse,
    "validAnagram": validAnagram,
    "sort": sort
}

# Clean up socket file
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen()

print("RPC Server listening...")

while True:
    conn, _ = server.accept()
    with conn:
        data = conn.recv(4096).decode("utf-8")
        request = json.loads(data)

        method = request["method"]
        params = request["params"]
        request_id = request["id"]

        try:
            result = function_map[method](*params)
            response = {
                "results": result,
                "result_type": type(result).__name__,
                "id": request_id
            }
        except Exception as e:
            response = {
                "error": str(e),
                "id": request_id
            }

        conn.sendall(json.dumps(response).encode("utf-8"))
