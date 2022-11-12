import HWModule

Commands = [
    HWModule.ModuleCommand(["nmap", "_HOST"], "nmap f", ["nmap_", "_HOST", "_", "_NMAPCOUNT"]),
    HWModule.ModuleCommand(["nmap", "-Sc", "-Sv", "_HOST"], "nmap", ["nmap_", "_HOST", "_", "_NMAPCOUNT"]),
    HWModule.ModuleCommand(["nmap", "_HOST", "-p-"], "nmap all", ["nmap_", "_HOST", "_", "_NMAPCOUNT"])
]

Globals = [
    HWModule.ModuleGlobal("_NMAPCOUNT", 0, autoIncrement=True)
]