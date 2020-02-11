import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#接続を待ち受けるIPアドレスとポート番号の指定
server.bind((bind_ip,bind_port))
#接続キューの最大数を5として待受けを開始する
server.listen(5)
print("[*] Listening on {0}:{1}".format(bind_ip,bind_port))

#クライアントからの接続を処理するスレッド
def handle_client(client_socket):
    #クライアントが送信してきたデータを表示
    request = client_socket.recv(1024)
    print("[*] Received:{0}".format(request))

    #パケットの返送
    client_socket.send(b"ACK!")
    client_socket.close()

while True:
    client, addr = server.accept()
    print("[*] Accepted connection from: {0}:{1}".format(addr[0],addr[1]))

    #受信データを処理するスレッドの起動
    client_handler = threading.Thread(target=handle_client,args=(client,))
    #スレッドの開始
    client_handler.start()
