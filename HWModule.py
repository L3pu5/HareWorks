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
    autoFormat = False

    def Get(self):
        if self.autoIncrement:
            self.value = self.value+1
            return self.value-1
        else:
            return self.value

    def Set(self, _value):
        if self.autoFormat == False:
            self.value = _value
        else:
            self.value= self.autoFormat.replace("$1", _value)

    def Read(self):
        return self.value

    def __init__(self, _tag, _value, _autoIncrement = False, _autoFormat = False):
        self.tag = _tag
        self.value = _value
        self.autoIncrement = _autoIncrement
        self.autoFormat = _autoFormat