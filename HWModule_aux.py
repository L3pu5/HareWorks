import HWModule

Commands = [
    HWModule.ModuleCommand(["enum4linux", "_HOST"], "enum4linux", ["enum4linux_", "_HOST", "_", "_ENUM4LINUXCOUNT"]),
]

Globals = [
    HWModule.ModuleGlobal("_ENUM4LINUXCOUNT", 0, autoIncrement=True)
]