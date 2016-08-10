from tkinter import *
from datetime import datetime
from tkinter.messagebox import *
import socket


class Window():
    '''Класс отвечает за создание и отображение элементов.'''
    active_page = 'login' #при запуске отображать страницу входа
    lgn = [] #список использованных логинов
    def __init__(self):
        '''
        Создание основного окна, без виджетов.
        '''
        self.window = Tk()
        self.window.geometry('500x395')
        self.window.minsize(300,395)
        self.window.title('SpamChat')
        
        '''Здесь виджеты для ввода логина и пароля,
        кнопка ок и Enter привязаны к app.ctrl.click_to_login()'''

        self.state = StringVar()
        self.state.set('Введите ник, чтобы начать.')

        self.frame2 = Frame(self.window,borderwidth=4,bg='gainsboro',height=400,width=500)
        self.frame2.pack(fill='both',expand='true')

        self.lbl=Label(self.frame2,textvariable=self.state)
        self.lbl.pack()

        self.login_entry=Entry(self.frame2,bg='ghostwhite',font=('Arial', 18))
        self.login_entry.pack()

        self.bttn2 = Button(self.frame2, text='Начать!',borderwidth=2,\
                            command=self.change_page,bg='#124580', \
                            font=("Helvetica", "16"),fg='white', \
                            width=14)
        self.bttn2.pack()

        if self.active_page == 'login':
            self.window.bind("<Return>",self.b1)
        
        '''Основное окно, с полем для ввода и
        полем отображения сообщений. '''
        
        self.frame = Frame(self.window,borderwidth=4,bg='gainsboro',height=400,width=50)
        
        self.bttn2 = Button(self.frame, text='Change user', command=self.change_page)
        self.bttn2.pack(side='top')
        
        self.msg=Text(self.frame,bg='white',fg="#0F1112",height=20,borderwidth=4,wrap=WORD) 
        self.msg.pack(side='top',expand='true')

        self.entry=Entry(self.frame,bg='ghostwhite')
        self.entry.pack(side='left',fill='both',expand='true')
        self.entry.focus()

        self.btn=Button(self.frame,text='Отправить',borderwidth=4,command=Controller.click)
        self.btn.pack(side='right')

        #привязка Enter к отправке.
        if self.active_page == 'main':
            self.window.bind('<Return>',Controller.enter_pressed)

    def change_page(self):
        #Меняет страницы, только вид. Вызывает ckick_to_login для проверки ввода.
        if self.active_page == 'login':
            if self.click_to_login()==True:
                self.frame2.pack_forget()
                self.frame.pack()
                self.entry.focus()
                self.window.bind('<Return>',Controller.enter_pressed)
                self.active_page = 'main'
        elif self.active_page == 'main':
            self.frame.pack_forget()
            self.frame2.pack()
            self.login_entry.focus()
            self.window.bind("<Return>",self.b1)
            self.active_page = 'login'
        else:
            pass

    def click_to_login(self):
        #Проверяет ввод догина, записывает логин в переменную.
        if not self.login_entry.get():
            self.state.set('Введите ник, пожалуйста.')
            return False 
        else:
            if self.login_entry.get() in self.lgn:
                self.state.set('Этот ник уже занят.')
                return False
            else:
                self.lgn.append(self.login_entry.get())
                login.set(self.login_entry.get())
                self.state.set('Зашел под ником {}'.format(login.get()))
                return True
        self.login_entry.delete(0,END)

    def b1(self,event):
        #Привязка Enter ко входу. 
        self.change_page()
        

class Controller():
    '''Логика, обработчики событий.'''
    login = ''
    def login(self):
        ##НЕ ДОДЕЛАНО
        '''Считать ввод логина/пароля, отправить серверу.
        Получить ответ true/false'''
        if response == True:
            #window.main_page()
            login.set(login)
        elif response == False:
            pass
            #messagebox Неверный логин/пароль
    def click():
        #Считывает сообщения из строки ввода и передает на отправку на сервер.
        if app.main_win.entry.get():
            message = app.main_win.entry.get()
            app.conn.send_message(message)
        
    def enter_pressed(event):
        #Enter на отправку
        Controller.click()
        
    def time_upd(self):
        #Обновляет время отправки
        time.set(datetime.strftime(datetime.now(), '%H:%M:%S'))
    

class Connection():
    '''Отвечает за подключение и отправку данных.'''
    def __init__(self):
        #При запуске сразу создает сокет и подключается к серверу.
        self.connector = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self._host = '127.0.0.1'
        self._port = 12345
        self.connector.connect ((str(self._host), int(self._port)))
        self.connector.setblocking(0)
        self.recvBuffer = 2000
    
    def update_msgbox(self):
        #Проверить буфер, догрузить сообщения в msgbox.
        try:
            recvData = self.connector.recv(self.recvBuffer)
        except socket.error:
            pass
            #showinfo('Sorry','There are no new messages.')
        else:
            str_inbox = recvData.decode('utf-8')
            inbox = str_inbox.split('END')
            for msg in inbox:
                if msg:
                    parts = msg.split('ø')
                    sender = parts[0]
                    message = parts[1]
                    time = parts[2]
                    print('{0} wrote on {1}:\n{2}\n'.format(sender,time,message))
                    app.main_win.msg.insert(END,'{} wrote on {}:\n{}\n\n'.format(sender,time,message))
            app.main_win.msg.see("end")

    def send_message(self, message):
        #отправка сообщения
        sendData = message
        app.ctrl.time_upd()
        sendData = (login.get()+'ø'+sendData+'ø'+time.get()+'END')
        self.connector.send(sendData.encode('utf-8'))
        app.main_win.entry.delete(0,END)
        

class Application():
    '''Класс-контейнер. Создает все объекты приложения.'''
    def __init__(self):
        self.main_win = Window()
        self.ctrl = Controller()
        self.conn = Connection()
        self.checker()
    def checker(self):
        self.main_win.window.after(100,self.checker)
        self.conn.update_msgbox()

app = Application()

#блок с переменными 
time = StringVar()
login = StringVar()

app.main_win.window.mainloop()
