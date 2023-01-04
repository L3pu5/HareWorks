import os
import subprocess
from datetime import datetime
import re

import HWModule
import HWModule_nmap
import HWModule_ffuf
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
        _notes.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + _data + "\n")

#Logging command returned from the subprocess.
def CommandLog(_data, _logFile = "Notes"):
    #If we are the NMAP log file, we should probably update our ports appropriately.
    if(_data.startswith("Starting Nmap")):
        portsRegex = re.compile("^([0-9]+)")
        for group in portsRegex.finditer(_logFile):
            Ports.append(group)
    #Continue to log
    with open(_logFile, "a") as _notes:
        _notes.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n" + _data + "\n")

def AppendCommand(_data):
    with open("CommandHistory", "a") as _commands:
        _commands.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + _data + "\n")

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
        elif _command[0] == "show":
            ShowGlobals()
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
        if(_command[0] == "set"):
            SetGlobal(_command[1].upper(), _command[2])
            return
        ToDo()

    #all other commands
    for command in Commands[len(_command)]:
        if command.hwCommand == Command:
            AppendLog("[Operator Command]: " + Command + " " + ProcessCommandArgs(command.osCommand) + " -> " + ProcessLogFiles(command.logFile, Read=True))
            if(command.hasAdditionaArgs != False):
                commandString = ' '.join(command.osCommand) # Have to create a string to use replace and not iterate over the objects
                for x in command.additionalArgs:
                    print("Additional argument required: " + x[0])
                    response = input("Default: " + x[1])
                    if not response:
                        commandString = commandString.replace(x[0], x[1]) # Substitute the default where the additional argument lives
                    else:
                        commandString = commandString.replace(x[0], response) #Take the user response instead.
                #Forward the command for global arg processing.
                #  
                commandString = commandString.split(' ') #This requires making the string back into an array
                print(ProcessArgs(commandString))
                sp = subprocess.run(ProcessCommandArgs(commandString), capture_output=True, shell=True)
            else:
                print(ProcessArgs(command.osCommand))
                sp = subprocess.run(ProcessCommandArgs(command.osCommand), capture_output=True, shell=True)
            
            CommandLog(sp.stdout.decode("utf-8"), ProcessLogFiles(command.logFile))

def PreLoad():
    #GLOBALS such as PORTS
    LoadGlobal_Globals()
    #NMAP
    LoadCommands(HWModule_nmap)
    LoadGlobals(HWModule_nmap)
    #FFUF
    LoadCommands(HWModule_ffuf)
    LoadGlobals(HWModule_ffuf)

def LoadGlobal_Globals():
    Globals.append(HWModule.ModuleGlobal("_PORTSCOMMA", ','.join(Ports)))

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

def ProcessLogFiles(_logFile, Read=False):
    global Globals
    output = []

    for i in range(len(_logFile)):
        if(_logFile[i] == "_HOST"):
            output.append(Host)
        elif(_logFile[i] == "_PORT"):
            output.append(Port);
        else:
            isGlobal = False
            for _global in Globals:
                if _global.tag == _logFile[i]:
                    if _global.autoIncrement:
                        if Read:
                            output.append(str(_global.Read()))
                            isGlobal = True
                        else:
                            output.append(str(_global.Get()))
                            isGlobal = True
                    else:
                        output.append(str(_global.value))
                        isGlobal = True
            if not isGlobal:
                output.append(str(_logFile[i]))
    return ''.join(output)

def ProcessCommandArgs(_command, Read=False):
    global Globals
    output = []
    for i in range(len(_command)):
        if(_command[i] == "_HOST"):
            output.append(Host)
        elif(_command[i] == "_PORT"):
            output.append(Port);
        else:
            for _global in Globals:
                if _global.tag == _command[i]:
                    if _global.autoIncrement:
                        if Read:
                            output.append(str(_global.Read()))
                        else:
                            output.append(str(_global.Get()))
                    else:
                        output.append(str(_global.value))
                else:
                    output.append(str(_command[i]))
    return ' '.join(output)

def SetGlobal(_globalToSet, _value):
    global Globals
    for _global in Globals:
        if _global.tag == _globalToSet:
            _global.Set(_value)
            Output("GLOBAL " + Colours["brightRed"] + _global.tag + Colours["reset"] + "=" + _global.Read())
            return
    Output(Colours["brightRed"] + "Global not fount" + Colours["reset"])

def ShowGlobal(_globalToShow):
    global Globals
    for _global in Globals:
        if _global.tag == _globalToShow:
            Output("GLOBAL " + Colours["brightRed"] + _global.tag + Colours["reset"] + "=" + _global.Read())
            return
    Output(Colours["brightRed"] + "Global not fount" + Colours["reset"])
    
def ShowGlobals():
    global Globals
    print("{0:20} | {1}".format("Global Tag", "Value"))
    for _global in Globals:
        print("{0:20} | {1}".format(_global.tag, _global.Read()))   

def Main():
    PreLoad()
    while Continue:
        Prompt()
        DoWork(input())

if __name__ == "__main__":
    Main()
