import HWModule

Commands = [
    HWModule.ModuleCommand(["enum4linux", "_HOST"], "enum4linux", ["enum4linux_", "_HOST", "_", "_FFUFCOUNT"]),
]

Globals = [
    HWModule.ModuleGlobal("_ENUM4LINUXCOUNT", 0, autoIncrement=True)
]