import HWModule

Commands = [
    HWModule.ModuleCommand(["ffuf", "_HOST"], "nmap f", ["nmap_", "_HOST", "_", "_FFUFCOUNT"]),
]

Globals = [
    HWModule.ModuleGlobal("_FFUFCOUNT", 0, autoIncrement=True)
]