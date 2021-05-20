import threading
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server socket opened')

s.bind(('localhost', 58585))
print('Bind to the local port')

s.listen(5)
print('Started listening...')
clients={}
#New user connect Handler
def connectnewuser(c,ad):
    while True:
        m=c.recv(256).decode()
        m_data = m.split(":", 1)
        textMessage=m_data[1]
        client=clients[m_data[0]]
        sendtoclient(textMessage,client)

def sendtoclient(m,c):
            c.send(bytes(m, encoding='utf-8'))
while True:
    c,ad=s.accept()
    while(True):
        m=c.recv(256).decode()
        if m :break

    clients[m]=c
    print(clients)
    threading._start_new_thread(connectnewuser,(c,ad))


