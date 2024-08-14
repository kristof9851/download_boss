import os

def getCacheDirPath():
    utilDir = os.path.dirname(__file__)
    e2eDir = os.path.dirname(utilDir)
    cacheDir = os.path.join(e2eDir, "cache")
    return cacheDir
