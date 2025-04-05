from flask import Flask, request, render_template
from classes import *

app = Flask(__name__)
app.config['DATA_COLLECTION_ENABLED'] = False

# Создание глобальных экземпляров устройств
robot1 = Robot('1', 'Робот1')
robot2 = Robot('2', 'Робот2')
signal_lamp = SignalLamp('1', 'Сигнальная лампа')
smartcam = SmartCamera('1', 'Умная камера')
terminal = Terminal('1', 'Удаленный терминал')

# Маршруты для каждого устройства
@app.route('/connect_robot1')
def connect_robot1():
    return robot1.connect(request)

@app.route('/connect_robot2')
def connect_robot2():
    return robot2.connect(request)

@app.route('/connect_signallamp')
def connect_signallamp():
    # Получаем значения роботов, чтобы обновить состояние сигнальной лампы
    parametr1 = robot1.value
    parametr2 = robot2.value
    # Проверяем состояние роботов и включаем/выключаем сигнальную лампу
    signal_lamp.auto_power(parametr1, parametr2)
    # Проверка аварийной ситуации
    alert_message = ''
    if signal_lamp.power == 'On':
        alert_message = 'Аварийная ситуация! Сигнальная лампа включена.'
    signal_lamp.connect()
    # Отправляем сообщение в ответе
    return json.dumps({'power': signal_lamp.power, 'alert_message': alert_message})



@app.route('/connect_smartcam')
def connect_smartcam():
    return smartcam.connect(request)

@app.route('/connect_terminal')
def connect_terminal():
    return terminal.connect(request)

# Главная страница с интерфейсом
@app.route('/')
def hello_world():
    return render_template('device_emulator2.html')


if __name__ == '__main__':
    app.run()