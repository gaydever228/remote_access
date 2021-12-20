import os
import sys
import json
import glob
import time
import base64
from PyQt5 import QtCore, QtGui, QtWidgets
import pyautogui
from des import *
import socket


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(list)
    def __init__(self, ip, port, parent = None):
        QtCore.QThread.__init__(self, parent)
  # Принимаем глобальные переменные
        self.ip = ip
        self.port = port
        self.command = 'screen'

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                self.client.connect((ip, port))
                print("connected")
                break
            except:
                time.sleep(5)

    def run(self):
        while True:
            print(self.command.split(' ')[0])
            print("run")
            if self.command.split(' ')[0] != 'screen':
                self.send_json(self.command.split(' '))
                responce = self.receive_json()
                self.mysignal.emit([responce])
                self.command = 'screen'
                print("brbbrsbr")
            if self.command.split(' ')[0] == 'screen':
                self.send_json(self.command.split(' '))
                responce = self.receive_json()
                self.mysignal.emit([responce])

    # Отправляем json данные серверу
    def send_json(self, data):
        # Если данные окажутся строкой
        print("sending")
        try:
            json_data = json.dumps(data.decode('utf-8'))
        except:
            json_data = json.dumps(data) 
        self.client.send(json_data.encode('utf-8'))



    # Получаем json данные от сервера
    def receive_json(self):
        json_data = ''
        while True:
            print("receiving")
            try:
                active = self.client.recv(8192).decode('utf-8')
                json_data += active
                return json.loads(json_data)
            except ValueError:
                print("over")
                pass


class VNCClient(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Создаем экземпляр обработчика
        self.ip = '91.203.193.48'
        self.port = 53210
        self.thread_handler = MyThread(self.ip, self.port)
        self.thread_handler.start()
        #self.thread_handler.send_json('ty pidor')
        # Обработчик потока для обновление GUI
        self.thread_handler.mysignal.connect(self.screen_handler)

    
    # Обработка и вывод изображения
    def screen_handler(self, screen_value):
        data = ['mouse_move_to', 'mouse_left_click',
                'mouse_right_click', 'mouse_double_left_click']

        # В случае если это не скрин, пропускаем шаг
        if screen_value[0] not in data:
            decrypt_image = base64.b64decode(screen_value[0])
            with open('2.png', 'wb') as file:
                file.write(decrypt_image)

            # Выводим изображение в панель
            image = QtGui.QPixmap('2.png')
            self.ui.label.setPixmap(image)


    # После закрытия сервера удаляем изображения
    def closeEvent(self, event):
        for file in glob.glob('*.png'):
            try: os.remove(file)
            except: pass


    # Обработка EVENT событий
    def event(self, event):
        # Обработка ЛКМ, ПКМ
        if event.type() == QtCore.QEvent.MouseButtonPress:
            current_button = event.button() # Определяем нажатую кнопку
            
            if current_button == 1:  
                mouse_cord = f'mouse_left_click {event.x()} {event.y()}'
            elif current_button == 2:
                mouse_cord = f'mouse_right_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord

        # Движение мыши без нажатий
        elif event.type() == QtCore.QEvent.MouseMove:
            mouse_cord = f'mouse_move_to {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord

        # Обработка double-кликов
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            mouse_cord = f'mouse_double_left_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord     
        
        return QtWidgets.QWidget.event(self, event)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = VNCClient()
    myapp.show()
    sys.exit(app.exec_())

