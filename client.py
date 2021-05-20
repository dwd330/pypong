import socket
import threading

class Client:
    def __init__(self, clientid1,clientid2):
        self.clientid1 = clientid1
        self.clientid2 = clientid2
        #socket create
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('localhost', 58585))
        self.s.send(bytes(self.clientid1, encoding='utf-8'))
        threading._start_new_thread( self.RecivHandler,())
        self.recived=''
        self.newrecived=''
        self.newdata=False
    #handle recive
    def RecivHandler(self):
        while True:
            self.newrecived=self.s.recv(256).decode()
            if self.newrecived !='':
                if self.newrecived !=self.recived:
                    self.recived=self.newrecived 
                    self.newdata=True

    #recive message
    def get_data(self) :
        if self.newdata:
            self.newdata=False
            return self.newrecived


    #send message
    def send(self,key):
        self.key=key
        pos_data=self.clientid2 +':'+str(key)
        self.s.send(bytes(pos_data, encoding='utf-8'))









   
