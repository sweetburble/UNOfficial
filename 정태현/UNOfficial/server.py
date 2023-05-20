import socket
from _thread import *
import pickle
import dill
from game import *

class socketServer():
    client_sockets = [] # 클라이언트들의 목록
    server = "192.168.0.127"
    port = 10134

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
                    self.games[gameId] = Multi_Uno(gameId)
                    # self.games[gameId].create()
                    create(self.games[gameId])
                    print("Creating a new game...")
                else:
                    self.games[gameId].ready = True
                    p = 1

                start_new_thread(self.threaded_client, (conn, p, gameId))
        except Exception as e:
            print("SocketServer error : ", e)
        finally:
            self.server_socket.close()


    def threaded_client(self, conn, p, gameId): # p = player
        conn.send(str.encode(str(p))) # 플레이어 번호를 클라이언트에게 보낸다

        reply = ""
        while True:
            time.sleep(0.1)
            try:
                data = conn.recv(4096 * 128).decode() # 클라이언트로부터 데이터를 받는다

                if gameId in self.games:
                    game = self.games[gameId] # games 딕셔너리에 들어가 있는 Multi_Uno 클래스의 객체를 가져온다

                    if not data:
                        break
                    else:
                        if data == "reset":
                            re_initialize(game)
                        elif data == "get":
                            pass
                        elif data == "draw":
                            take_from_stack(game, 1, p)
                            print("draw: ", end="")
                            print(game)
                        elif data == "next_turn":
                            set_next_player(game)
                            print("next_turn: ", end="")
                            print(game)
                        elif data == "shout_uno":
                            shout_uno(game, p)
                        elif data == "Red":
                            change_card_color(game, p, "Red")
                        elif data == "Green":
                            change_card_color(game, p, "Green")
                        elif data == "Blue":
                            change_card_color(game, p, "Blue")
                        elif data == "Yellow":
                            change_card_color(game, p, "Yellow")
                        else: # 클라이언트가 카드를 내는 경우
                            play_this_card(game, p, data) 
                            print("play_this_card: ", end="")
                            print(game)
                        
                        reply = game # Multi_Uno 객체를 reply에 저장한다
                        print("reply: ", end="")
                        print(reply)
                        conn.sendall(dill.dumps(reply)) # Multi_Uno 객체를 인코딩해서 클라이언트에게 보낸다
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