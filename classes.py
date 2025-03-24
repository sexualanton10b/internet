import abc
import random
import json
import re

class Device(abc.ABC):
    def __init__(self, name):
        self.name = name
        print('create_Thing')

    @abc.abstractmethod
    def connect(self, *args):
        print('Connection start')


class Robot(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        print('robot has create')

    def connect(self):
        super().connect()
        self.emulate()
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({'value': self.value})

    def connect(self, request):
        super().connect()
        try:
            self.value = int(request.args.get('value', ''))
            print(f'Connection with {self.name} success, new value is {self.value}')
            return json.dumps({'value': self.value})
        except ValueError:
            print(f'New value has not been accepted, need int but given {type(request.args.get("value", ""))}')
            return json.dumps({'error': 'Invalid data type, expected int'})

    def emulate(self):
        self.value = random.randint(15, 25)


class SmartCamera(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        print('smart camera has create')

    def connect(self):
        super().connect()
        self.emulate()
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({'value': self.value})

    def connect(self, request):
        super().connect()
        try:
            self.value = float(request.args.get('value', ''))
            print(f'Connection with {self.name} success, new value is {self.value}')
            return json.dumps({'value': self.value})
        except ValueError:
            print(f'New value has not been accepted, need float but given {type(request.args.get("value", ""))}')
            return json.dumps({'error': 'Invalid data type, expected float'})

    def emulate(self):
        self.value = random.randint(0, 100)


class SignalLamp(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        print('SignalLamp has create')

    def connect(self):
        super().connect()
        self.emulate()
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({'value': self.value})

    def connect(self, request):
        super().connect()
        value = request.args.get('value', '')
        try:
            if not isinstance(value, str):
                raise ValueError
            self.value = value
            print(f'Connection with {self.name} success, new value is {self.value}')
            return json.dumps({'value': self.value})
        except ValueError:
            print(f'New value has not been accepted, need str but given {type(value)}')
            return json.dumps({'error': 'Invalid data type, expected str'})

    def emulate(self):
        self.value = random.randint(0, 1)  # 0 или 1, как для лампы (вкл/выкл)


class Terminal(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        print('terminal has create')

    def connect(self):
        super().connect()
        self.emulate()
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({'value': self.value})

    def connect(self, request):
        super().connect()
        value = request.args.get('value', '')
        if re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
            self.value = value
            print(f'Connection with {self.name} success, new value is {self.value}')
            return json.dumps({'value': self.value})
        else:
            print(f'New value has not been accepted, need date in format DD.MM.YYYY but given {value}')
            return json.dumps({'error': 'Invalid data format, expected date in DD.MM.YYYY'})

    def emulate(self):
        self.value = random.randint(-10, 10)
