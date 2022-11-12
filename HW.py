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

Globals = []

Continue = True

def ToDo():
    print("To do.")

def Output(_data):
    print("[HareWork]: " + _data)

def AppendLog(_data, _logFile = "Notes"):
    with open(_logFile, "a") as _notes:
        _notes.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + _data)

def AppendCommand(_data):
    with open("CommandHistory", "a") as _commands:
        _commands.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + _data)

def Prompt():
    print("[HareWork]> ", end="")

def DoWork(Command):
    global Host
    global Commands
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
    else:
        ToDo()

    #all other commands
    for command in Commands[len(_command)]:
        if command.hwCommand == Command:
            print(ProcessArgs(command.osCommand))
            sp = subprocess.run(ProcessArgs(command.osCommand), capture_output=True)
            AppendLog(sp.stdout, ProcessLogFiles(command.logFile))
            Output(sp)

    Prompt()

def PreLoad():
    LoadCommands(HWModule_nmap)
    LoadGlobals(HWModule_nmap)

def LoadCommands(_module):
    global Commands
    for command in _module.Commands:
        Commands[command.hwCount].append(command)
        print(ProcessArgs(command.osCommand))

def LoadGlobals(_module):
    global Globals
    for _global in _module.Globals:
        Globals.append(_global)

def ProcessArgs(_args):
    output = []
    for i in range(len(_args)):
        if(_args[i] == "_HOST"):
            output.append(Host)
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
                    output.append(_global.value)
                else:
                    output.append(_logFile[i])
    return ''.join(output)


def Main():
    PreLoad()
    Prompt()
    while Continue:
        DoWork(input())

if __name__ == "__main__":
    Main()
