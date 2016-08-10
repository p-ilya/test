import socket, time

global DB
DB = {'elias': 'qwerty',
      'sasha': '123456',
      'vika': '1q2w3e4r'}

class Controller():
    '''Логика программы. '''
    def login(self):
        '''
        Проверяет, есть ли юзер в базе, и разрешает/запрещает вход.
        '''
        user = input('login: ')
        password = input('password: ')
        input
        if user in DB and DB[user]==password:
            #grant access
            print('OK')
            pass
        else:
            #deny access
            print('ne OK')
            pass
        
class Connection():
    def connect(self):
        HOST = '127.0.0.1'        
        PORT = 50007              
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.s.listen(1)
        self.conn = self.s.accept()
        self.addr = self.s.accept()
        print ("\nConnected client\n")
    def receive(self):
        data = self.conn.recv(1024)
        data = str(data)
        return data

ctrl = Controller()
ctrl.login()
conn = Connection()

while True:
    print(conn.conn.receive())

