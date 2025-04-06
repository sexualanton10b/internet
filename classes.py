import abc
import random
import json
import re
import pymongo
import datetime

class Logger:
    def __init__(self, db_name):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.last_device_states = {}
        self.last_alert = None

    def insert_device_state(self, device_name, state):
        # Проверка на изменение состояния
        if device_name not in self.last_device_states or state != self.last_device_states[device_name]:
            self.last_device_states[device_name] = state
            self.db['DeviceStates'].insert_one({
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'device': device_name,
                'state': state
            })
            print(f'State of {device_name} logged.')
        else:
            print(f'State of {device_name} unchanged.')

    def insert_alert(self, message):
        # Проверка на повторение алерта
        if message != self.last_alert:
            self.last_alert = message
            self.db['Alerts'].insert_one({
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message': message
            })
            print(f'Alert logged: {message}')

    def get_robot_data(self, robot_name):
        """Извлечь данные робота из коллекции DeviceStates."""
        return self.db['DeviceStates'].find({'device': robot_name})

    def robot_chart(self, robot_name):
        cursor = self.db['DeviceStates'].find({'device': robot_name})
        robot_data = []
        time_data = []
        for elem in cursor:
            robot_data.append(elem['state']['value'])
            time_data.append(elem['timestamp'])
        return {'robot_data': robot_data, 'time_data': time_data}

    def calculate_stats(self, robot_name):
        """Вычислить среднее и максимальное значения для робота."""
        data = self.get_robot_data(robot_name)
        values = []
        for entry in data:
            if 'state' in entry and 'value' in entry['state']:
                values.append(entry['state']['value'])
        if not values:
            return {'average': 0, 'max': 0}
        return {
            'average': sum(values) / len(values),
            'max': max(values)
        }

class Device(abc.ABC):
    def __init__(self, name):
        self.name = name
        self.power = "off"  # По умолчанию выключено
        print('create_Thing')

    @abc.abstractmethod
    def connect(self, *args):
        print('Connection start')


class Robot(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.joint_angles=[0.0] * 6
        self.monor_loads = [0.0] * 6
        self.temperature = 25.0
        self.value = 0
        print('robot has create')

    def connect(self, request):
        super().connect()
        try:
            value = request.args.get('value', '')
            if value.lower() in ['on', 'off']:
                self.power = value.lower()
            else:
                self.value = int(value)
                self.power = "on"  # Автоматически включаем при успешном получении значения
            print(f'Connection with {self.name} success, power: {self.power}, value: {self.value}')
            return json.dumps({'value': self.value, 'power': self.power})
        except ValueError:
            print(f'New value has not been accepted, need int but given {type(request.args.get("value", ""))}')
            return json.dumps({'error': 'Invalid data type, expected int'})


class SmartCamera(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        print('smart camera has create')

    def connect(self, request):
        super().connect()
        try:
            value = request.args.get('value', '')
            if value.lower() in ['on', 'off']:
                self.power = value.lower()
            else:
                self.value = float(value)
                self.power = "on"  # Автоматически включаем при успешном получении значения
            print(f'Connection with {self.name} success, power: {self.power}, value: {self.value}')
            return json.dumps({'value': self.value, 'power': self.power})
        except ValueError:
            print(f'New value has not been accepted, need float but given {type(request.args.get("value", ""))}')
            return json.dumps({'error': 'Invalid data type, expected float'})


class SignalLamp(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.power = 'Off'
        print('SignalLamp has create')

    def connect(self):
        super().connect()
        print(f'Connection with {self.name} success, power: {self.power}')
        return json.dumps({'power': self.power})

    def auto_power(self, parametr1, parametr2):
        # Если хотя бы одно из значений роботов выходит за пределы от 0 до 100, включаем сигнальную лампу
        if not (0 <= parametr1 <= 100) or not (0 <= parametr2 <= 100):
            self.power = 'On'  # Включаем сигнальную лампу
        else:
            self.power = 'Off'  # Оставляем выключенной, если значения в пределах допустимого диапазона



class Terminal(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        print('terminal has create')

    def connect(self, request):
        super().connect()
        value = request.args.get('value', '')
        if value.lower() in ['on', 'off']:
            self.power = value.lower()
            print(f'Connection with {self.name} success, power: {self.power}')
            return json.dumps({'power': self.power})
        elif re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
            self.value = value
            self.power = "on"  # Автоматически включаем при успешном получении значения
            print(f'Connection with {self.name} success, value: {self.value}, power: {self.power}')
            return json.dumps({'value': self.value, 'power': self.power})
        else:
            print(f'New value has not been accepted, need date in format DD.MM.YYYY but given {value}')
            return json.dumps({'error': 'Invalid data format, expected date in DD.MM.YYYY'})