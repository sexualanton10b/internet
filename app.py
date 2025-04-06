from flask import Flask, request, render_template, json
from classes import *

app = Flask(__name__)
app.config['DATA_COLLECTION_ENABLED'] = True  # Включить сбор данных

# Создание глобальных экземпляров устройств и логгера
logger = Logger('IoT_Logs')  # Инициализация логгера
robot1 = Robot('1', 'Робот1')
robot2 = Robot('2', 'Робот2')
signal_lamp = SignalLamp('1', 'Сигнальная лампа')
smartcam = SmartCamera('1', 'Умная камера')
terminal = Terminal('1', 'Удаленный терминал')

@app.route('/connect_robot1')
def connect_robot1():
    response = robot1.connect(request)
    # Логирование состояния робота
    logger.insert_device_state(robot1.name, {'value': robot1.value, 'power': robot1.power})
    return response

@app.route('/connect_robot2')
def connect_robot2():
    response = robot2.connect(request)
    logger.insert_device_state(robot2.name, {'value': robot2.value, 'power': robot2.power})
    return response

@app.route('/connect_signallamp')
def connect_signallamp():
    parametr1 = robot1.value
    parametr2 = robot2.value
    signal_lamp.auto_power(parametr1, parametr2)
    alert_message = ''
    if signal_lamp.power == 'On':
        alert_message = 'Аварийная ситуация! Сигнальная лампа включена.'
        logger.insert_alert(alert_message)  # Логирование аварии
    signal_lamp.connect()
    logger.insert_device_state(signal_lamp.name, {'power': signal_lamp.power})  # Логирование состояния
    return json.dumps({'power': signal_lamp.power, 'alert_message': alert_message})

@app.route('/connect_smartcam')
def connect_smartcam():
    response = smartcam.connect(request)
    logger.insert_device_state(smartcam.name, {'value': smartcam.value, 'power': smartcam.power})
    return response

@app.route('/connect_terminal')
def connect_terminal():
    response = terminal.connect(request)
    logger.insert_device_state(terminal.name, {'value': terminal.value, 'power': terminal.power})
    return response

@app.route('/stats_robot1')
def stats_robot1():
    stats = logger.calculate_stats('Робот1')
    return json.dumps(stats)

@app.route('/stats_robot2')
def stats_robot2():
    stats = logger.calculate_stats('Робот2')
    return json.dumps(stats)

@app.route('/')
def hello_world():
    return render_template('device_emulator2.html')

if __name__ == '__main__':
    app.run()