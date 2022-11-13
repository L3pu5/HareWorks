import os
import subprocess
from datetime import datetime

import HWModule
import HWModule_nmap
#-

Host = ""
Port = ""

Ports = {}

Commands = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: []
}

Colours = {
    "yellow": u"\u001b[33m",
    "red": u"\u001b[31m",
    "brightRed": u"\u001b[31;1m",
    "green": u"\u001b[32m",
    "brightGreen": u"\u001b[32;1m",
    "reset": u"\u001b[0m"
}

Globals = []

Continue = True

def ToDo():
    print("To do.")

def Output(_data):
    print("["+ Colours["brightGreen"] + "HareWork" + Colours["reset"] + "]: " + _data)

def AppendLog(_data, _logFile = "Notes"):
    with open(_logFile, "a") as _notes:
        _notes.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + _data)

def CommandLog(_data, _logFile = "Notes"):
    with open(_logFile, "a") as _notes:
        _notes.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n" + _data + "\n")

def AppendCommand(_data):
    with open("CommandHistory", "a") as _commands:
        _commands.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + _data)

def Prompt():
    if Host == "":
        print("[" + Colours["brightGreen"] + "HareWork" + Colours["reset"] + "]> ", end="")
    else:
        if Port == "":
            print("[" + Colours["red"] + Host + Colours["reset"] + "]> ", end="")
        else:
            print("[" + Colours["red"] + Host + Colours["reset"] + ":" + Colours["yellow"] + Port + Colours["reset"] + "]> ", end="")

def DoWork(Command):
    global Host
    global Commands
    global Port
    _command = Command.split(' ')
    if len(_command) == 1:
        if _command[0] == "exit":
            exit()
        else:
            ToDo()
    elif len(_command) == 2:
        if(_command[0]) == "tar":
            Host = _command[1]
            Output("Host="+Host)
            return
        elif(_command[0]) == "port":
            Port = _command[1]
            Output("Port="+Port)
            return
    else:
        if(_command[0]) == "log":
            AppendLog("[Manual Operator Log]:" + ' '.join(ProcessArgs(_command[1:])) + '\n')
            return
        ToDo()

    #all other commands
    for command in Commands[len(_command)]:
        if command.hwCommand == Command:
            print(ProcessArgs(command.osCommand))
            AppendLog("[Operator Command]: " + Command)
            sp = subprocess.run(ProcessCommandArgs(command.osCommand), capture_output=True, shell=True)
            CommandLog(sp.stdout.decode("utf-8"), ProcessLogFiles(command.logFile))

def PreLoad():
    LoadCommands(HWModule_nmap)
    LoadGlobals(HWModule_nmap)

def LoadCommands(_module):
    global Commands
    for command in _module.Commands:
        Commands[command.hwCount].append(command)

def LoadGlobals(_module):
    global Globals
    for _global in _module.Globals:
        Globals.append(_global)

def ProcessArgs(_args):
    output = []
    for i in range(len(_args)):
        if(_args[i] == "_HOST"):
            output.append(Host)
        elif(_args[i] == "_PORT"):
            output.append(Port);
        else:
            output.append(_args[i])
    return output

def ProcessLogFiles(_logFile):
    global Globals
    output = []
    for i in range(len(_logFile)):
        if(_logFile[i] == "_HOST"):
            output.append(Host)
        elif(_logFile[i] == "_PORT"):
            output.append(Port);
        else:
            for _global in Globals:
                if _global.tag == _logFile[i]:
                    if _global.autoIncrement:
                        output.append(str(_global.Get()))
                    else:
                        output.append(str(_global.value))
                else:
                    output.append(str(_logFile[i]))
    return ''.join(output)

def ProcessCommandArgs(_logFile):
    global Globals
    output = []
    for i in range(len(_logFile)):
        if(_logFile[i] == "_HOST"):
            output.append(Host)
        elif(_logFile[i] == "_PORT"):
            output.append(Port);
        else:
            for _global in Globals:
                if _global.tag == _logFile[i]:
                    if _global.autoIncrement:
                        output.append(str(_global.Get()))
                    else:
                        output.append(str(_global.value))
                else:
                    output.append(str(_logFile[i]))
    return ' '.join(output)


def Main():
    PreLoad()
    while Continue:
        Prompt()
        DoWork(input())

if __name__ == "__main__":
    Main()
