import HWModule

Commands = [
    HWModule.ModuleCommand(["ffuf", "-s", "-u", "DOMAIN", "-w", "WORDLIST"], "ffuf f", ["ffuf_", "_HOST", "_", "_FFUFCOUNT"], True, [["WORDLIST", "/usr/share/wordlists/dirb/common.txt"], ["DOMAIN", "http://CHANGEME.TARGET/FUZZ"]]),
    HWModule.ModuleCommand(["ffuf", "-w", "WORDLIST", ""], "ffuf subdr", ["ffufSUBDR_", "_HOST", "_", "_FFUFCOUNT"]),
    HWModule.ModuleCommand(["ffuf", "-s", "_HOST"], "ffuf subdr", ["ffufSUBDR_", "_HOST", "_", "_FFUFCOUNT"]),
]

Globals = [
    HWModule.ModuleGlobal("_FFUFCOUNT", 0, _autoIncrement=True)
]