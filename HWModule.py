class ModuleCommand:
    osCommand = ""
    hwCommand = ""
    hwCount = 0
    logFile = [""]

    def __init__(self, _osCommand, _hwCommand, _logFile = ["logs"]):
        self.osCommand = _osCommand
        self.hwCommand = _hwCommand
        self.hwCount = len(self.hwCommand.split())
        self.logFile = _logFile

class ModuleGlobal:
    tag = ""
    value = ""
    autoIncrement = False

    def Get(self):
        if self.autoIncrement:
            self.value = self.value+1
            return self.value-1
        else:
            return self.value

    def __init__(self, _tag, _value, _autoIncrement = False):
        self.tag = _tag
        self.value = _value
        self.autoIncrement = _autoIncrement