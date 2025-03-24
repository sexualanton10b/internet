import abc
import random
import json


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
        self.value = request.args.get('value', '')
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({'value': self.value})

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
        self.value = request.args.get('value', '')
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({'value': self.value})

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
        self.value = request.args.get('value', '')
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({'value': self.value})

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
        self.value = request.args.get('value', '')
        print(f'Connection with {self.name} success, new value is {self.value}')
        return json.dumps({'value': self.value})

    def emulate(self):
        self.value = random.randint(-10, 10)
