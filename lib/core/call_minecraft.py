import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 19537
# port = 19536
s.connect(("127.0.0.1", port))


string = b"""{
    "type": "commands",
    "commands": [
        "/time set night",
        "/summon tnt 0 -50 0",
        "/gamerule keepInventory true"
    ]
}"""
s.send(string)

data = s.recv(8192)
print(data.decode())
o = json.loads(data.decode())
print(o, type(o), len(o))
# j = json.load(data)
# print(j)

s.close()
