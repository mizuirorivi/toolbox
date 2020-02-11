import socket 
from threading import Thread
from datetime import datetime

buf_size = 1024
bind_ip = "0.0.0.0"
bind_port = 8000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))

server.listen(5)

print("[*] Listening on {0}:{1}".format(bind_ip,bind_port))

def handle_client(client_socket):
    request = client_socket.recv(buf_size)
    print("[*]Received:\n{}{}".format(request.decode('utf-8'),"-"*24))

    now = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    html = """<!DOCTYPE html><html lang="ja"><body><p>Test Server<p></body></html>"""
    header = """HTTP/1.0 200 OK\r\nDate: {}\r\nServer:Test Http Server\r\nContent-Type: text/html;charset=utf-8\r\n\r\n""".format(now)
    if request.startswith(b'HEAD'):
        client_socket.send(header.encode('utf-8'))
    elif request.startswith(b'GET'):
        response = header[:-2]+"Content-Length:{}\r\n".format(len(html))+"\r\n"+html
        client_socket.send(response.encode('utf-8'))

while True:
    client, addr = server.accept()
    print("[*] Accpeted connection from:{}:{}".format(addr[0],addr[1]))
    client_handler = Thread(target=handle_client,args=[client])
    client_handler.start()
    