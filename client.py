import json
import socket
import _thread

# System parameters
host = "localhost"
port = 50001
size = 1024

# Create connection to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
name = ""

def send_message():
    while True:
        print("To whom is the next message? (user name for direct message or b for broadcast)")
        dest = input()
        print("Which is the message?")
        msg = input()
        if dest == "b":
            data = json.dumps({"type": "broadcast", "payload": {"source": name, "content": msg}})
        else:
            data = json.dumps({"type": "message", "payload": {"source": name, "dest": dest, "content": msg}})
        s.send(data.encode("utf-8"))

# Request an user name (must be unique in the system)
print("What name do you want to use?")
while True:
    name = input()
    if name == "b":
        print("Reserved name. Try another one")
        continue
    data = json.dumps({"type": "connection", "payload": {"name": name}})
    s.send(data.encode("utf-8"))
    # Waits for server response
    data = s.recv(size)
    if data:
        data = json.loads(data.decode("utf-8"))
        # Ok status means the name has been accepted
        if data["payload"]["status"] == "ok":
            break
        else:
            print("Name already taken. Try another one.")

_thread.start_new_thread(send_message, ())

while True:
    data = s.recv(size)
    if data:
        data = s.recv(size)
        print("Received: %s" % data.decode('utf-8'))

# Close the connection
s.close()
