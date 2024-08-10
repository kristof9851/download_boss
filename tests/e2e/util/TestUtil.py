import os

def getTmpDirPath():
    utilDir = os.path.dirname(__file__)
    e2eDir = os.path.dirname(utilDir)
    tmpDir = os.path.join(e2eDir, "tmp")
    return tmpDir
