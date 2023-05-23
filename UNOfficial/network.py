import socket
import pickle
import dill

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 소켓 생성
        self.server = "192.168.0.127"
        self.port = 10134
        self.addr = (self.server, self.port)
        self.p = self.connect()
    
    def getP(self):
        return self.p
    
    def connect(self):
        try:
            self.client.connect(self.addr) # 서버에 연결
            return self.client.recv(4096 * 128).decode() # 서버로부터 데이터를 받는다
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(str.encode(data)) # 데이터를 인코딩해서 서버에 보낸다
            received_data = self.client.recv(4096 * 128) # 서버로부터 데이터를 받는다

            # if not received_data:
            #     print(">> No data received")
            #     return None
            
            return dill.loads(received_data) # 받은 데이터를 디코딩해서 반환한다
        except socket.error as e:
            print(e)
