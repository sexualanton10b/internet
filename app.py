from flask import Flask
from classes import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    print(robot1.unit)
    print(robot2.unit)
    print(smartcam.unit)
    print(signallamp.unit)
    print(terminal.unit)
    return robot1.connect('temp unit') + '\n' + robot2.connect('temp unit') + '\n' + smartcam.connect('temp unit') + '\n' + signallamp.connect('temp unit') + '\n' + terminal.connect('temp unit')

if __name__ == '__main__':
    robot1 = Robot('1','Робот1')
    robot2 = Robot('2', 'Робот2')
    smartcam = SmartCamera('1', 'Умная камера')
    signallamp = SignalLamp('1', 'Сигнальная лампа')
    terminal = Terminal('1', 'Удаленный терминал')
    app.run()