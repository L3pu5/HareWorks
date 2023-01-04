import HWModule

Commands = [
    HWModule.ModuleCommand(["nmap", "_HOST"], "nmap f", ["nmap_SIMPLE_", "_HOST", "_", "_NMAPCOUNT"]),
    HWModule.ModuleCommand(["nmap", "-Sc", "-Sv", "-Pn", "_HOST"], "nmap", ["nmap_DETAIL_", "_HOST", "_", "_NMAPCOUNT"]),
    HWModule.ModuleCommand(["nmap", "_HOST", "-p-", "-T5"], "nmap all", ["nmap_FULL_", "_HOST", "_", "_NMAPCOUNT"]),
    HWModule.ModuleCommand(["nmap", "_HOST", "-p", "_PORTSCOMMA", "-A", "-T5"], "nmap all", ["nmap_AGGRESSIVE_", "_HOST", "_", "_NMAPCOUNT"]),
    HWModule.ModuleCommand(["nmap", "-verbose 4" ,"-p", "_PORT", "--script", "krb5-enum-users", "--script-args", "_NMAPKERBREALM", "userdb=user.txt", "_HOST"], "nmap kerb", ["nmap_", "_HOST", "_", "_PORT", "_", "KERB"])
]
#krb5-enum-users-realm='kerbrealm'
Globals = [
    HWModule.ModuleGlobal("_NMAPCOUNT", 0, _autoIncrement=True),
    HWModule.ModuleGlobal("_NMAPKERBREALM", "", _autoFormat="krb5-enum-users-realm='$1'")
]