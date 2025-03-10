import abc


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

    def connect(self, source):
        super().connect()
        return ('Robot connection to ' + source + ' success')


class SmartCamera(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        print('smart camera has create')

    def connect(self, source):
        super().connect()
        return ('SmartCamera connection to ' + source + ' success')


class SignalLamp(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        print('SignalLamp has create')

    def connect(self, source):
        super().connect()
        return ('SignalLamp connection to ' + source + ' success')


class Terminal(Device):
    def __init__(self, unit, name):
        super().__init__(name)
        self.unit = unit
        self.value = 0
        print('terminal has create')

    def connect(self, source):
        super().connect()
        return ('Terminal connection to ' + source + ' success')
