import os
import sys
import operator
import ctypes
import math
import time
from kfolder import *
from burst import *
from stats import *

def blocks(size):
    return math.ceil(size / blockSize) * blockSize

def du(name, ppath, level):
    now = time.time()
    fold = kFolder()
    fold.name = name
    fold.path = ppath
    
#    print(name, ppath, level)
    path = os.path.join(ppath, name)

    try:
        for entry in os.scandir(path):
            if entry.is_file():

                try:
                    stat = entry.stat()
                except OSError:
                    continue

                ageDays = (now - stat.st_mtime) / (60 * 60 * 24)
                fold.add_file(entry.name, stat.st_size, blocks(stat.st_size), ageDays)
            else:
                fold.add_fold(du(entry.name, path, level+1))

#        print(path, human(this[0]), human(this[1]), human(this[0]+childs[0]), human(this[1]+childs[1]))
    except OSError:
        return fold

#    if level == 2:
#        print (fold)
    return fold

def calcBlockSize(path):
    root = os.path.splitdrive(path)
    
    sectorsPerCluster = ctypes.c_ulonglong(0)
    bytesPerSector = ctypes.c_ulonglong(0)
    rootPathName = ctypes.c_wchar_p(root[0]) #(u"E:\\")

    ctypes.windll.kernel32.GetDiskFreeSpaceW(rootPathName,
        ctypes.pointer(sectorsPerCluster),
        ctypes.pointer(bytesPerSector),
        None,
        None,
    )
    return int(bytesPerSector.value) * int(sectorsPerCluster.value)

def output():
    global rootfold
    rows = []
    rows.append(rootfold.get_title())
    rows.append(rootfold.get_row())
    for fold in subfolds:
        if fold.totCount != 0:
            rows.append(fold.get_row())
    widths = [max(map(len, col)) for col in zip(*rows)]
    for row in rows:
        print ("  ".join((val.rjust(width) for val, width in zip(row, widths))))
    
if len(sys.argv) == 1:
    sys.argv.append('r:/pix/a/') #'e:\projects\sumatra')

showstats = "-stats" in sys.argv
showcount = "-counts" in sys.argv
path = sys.argv[len(sys.argv)-1]

blockSize = calcBlockSize(path)
dirlist = []
rootfold = du('', path, 1)

if showstats:
    stats(rootfold)

if showcount:
    subfolds = sorted(rootfold.subs, key=lambda foo: foo.totCount, reverse=True)
    print("File counts: " + path)
    output()
    print()

subfolds = sorted(rootfold.subs, key=lambda foo: foo.totSize, reverse=True)
print("Folder sizes: " + path)
output()
    
##print("Folder;Local;Total;LFiles;TFiles;Subdirs;AvgSize")
##print (rootfold)
##for fold in subfolds:
##    print(fold)

#dirlist.sort(key=lambda foo: foo[2])
#dirlist.reverse()

#doChart(rootfold)
