from flask import Flask, request, render_template
from classes import *

app = Flask(__name__)
app.config['DATA_COLLECTION_ENABLED'] = False


# Создание глобальных экземпляров устройств
robot1 = Robot('1', 'Робот1')
robot2 = Robot('2', 'Робот2')
smartcam = SmartCamera('1', 'Умная камера')
signallamp = SignalLamp('1', 'Сигнальная лампа')
terminal = Terminal('1', 'Удаленный терминал')

# Маршруты для каждого устройства
@app.route('/connect_robot1')
def connect_robot1():
    return robot1.connect(request)

@app.route('/connect_robot2')
def connect_robot2():
    return robot2.connect(request)

@app.route('/connect_smartcam')
def connect_smartcam():
    return smartcam.connect(request)

@app.route('/connect_signallamp')
def connect_signallamp():
    return signallamp.connect(request)

@app.route('/connect_terminal')
def connect_terminal():
    return terminal.connect(request)

# Главная страница с интерфейсом
@app.route('/')
def hello_world():
    return render_template('device_emulator2.html')

if __name__ == '__main__':
    app.run()