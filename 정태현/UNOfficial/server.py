import socket
from _thread import *
import pickle
from game import Game

class socketServer():
    client_sockets = [] # 클라이언트들의 목록
    server = "10.50.99.36"
    port = 5555

    def __init__(self):
        print(">> Server Start")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 소켓 생성
        try:
            self.server_socket.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))

        self.server_socket.listen()
        print("Waiting for a connection, Server Started")

        self.connected = set()
        self.games = {}
        self.idCount = 0


    def server_run(self):
        try:
            while True:
                print(">> Waiting for a connection")
                conn, addr = self.server_socket.accept()
                print("Connected to: ", addr)

                self.idCount += 1
                p = 0
                gameId = (self.idCount - 1) // 2 # 2명의 플레이어가 한 게임에 들어가므로 2로 나눈다
                if self.idCount % 2 == 1:
                    self.games[gameId] = Game(gameId)
                    print("Creating a new game...")
                else:
                    self.games[gameId].ready = True
                    p = 1

                start_new_thread(self.threaded_client, (conn, p, gameId))
        except Exception as e:
            print("SocketServer error : ", e)
        finally:
            self.server_socket.close()


    def threaded_client(self, conn, p, gameId):
        conn.send(str.encode(str(p))) # 플레이어 번호를 클라이언트에게 보낸다

        reply = ""
        while True:
            try:
                data = conn.recv(4096).decode() # 클라이언트로부터 데이터를 받는다

                if gameId in self.games:
                    game = self.games[gameId]

                    if not data:
                        break
                    else:
                        if data == "reset":
                            game.resetWent()
                        elif data != "get":
                            game.play(p, data)
                        
                        reply = game
                        conn.sendall(pickle.dumps(reply)) # 데이터를 인코딩해서 클라이언트에게 보낸다
                else:
                    break
            except:
                break
        
        print("Lost connection")
        try:
            del self.games[gameId]
            print("Closing Game: ", gameId)
        except:
            pass
        self.idCount -= 1
        conn.close()

server = socketServer()
server.server_run()