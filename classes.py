import abc
import random
import json
import re

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
        self.value = 0
        print('SignalLamp has create')

    def connect(self, request):
        super().connect()
        value = request.args.get('value', '')
        try:
            if value.lower() in ['on', 'off']:
                self.power = value.lower()
                self.value = 1 if value.lower() == 'on' else 0
            else:
                if not isinstance(value, str):
                    raise ValueError
                self.value = value
                self.power = "on"  # Автоматически включаем при успешном получении значения
            print(f'Connection with {self.name} success, power: {self.power}, value: {self.value}')
            return json.dumps({'value': self.value, 'power': self.power})
        except ValueError:
            print(f'New value has not been accepted, need str but given {type(value)}')
            return json.dumps({'error': 'Invalid data type, expected str'})


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