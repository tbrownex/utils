from pathlib import Path
import platform

def getHomeOS():
    home = str(Path.home())
    os   = platform.system()
    return os, home