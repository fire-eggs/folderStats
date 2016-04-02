# calculate statistics on folders. this requires flattening the tree.

import numpy as np
from kfolder import *
from operator import itemgetter

def do_flat(fold):
    me = []
    if len(fold.subs) != 0:
        for x in fold.subs:
            me.append(x)
            me.extend(do_flat(x))
    return me

def stats(rootfold):
    #dt = np.dtype([('path', np.str_), ('count', np.int)])

    flatten = do_flat(rootfold)

##    for fold in flatten:
##        print( fold )

    #count = len(rootfold.subs)
    count = len(flatten)
    arr = np.ndarray((count,), dtype=np.uint64)  # file counts
    arr2 = np.ndarray((count,), dtype=np.uint64) # avg file size
    arr3 = np.ndarray((count,), dtype=np.uint32) # avg file age

    for i in range(count):
        arr[i] = flatten[i].myCount
        arr2[i] = flatten[i].avgSize()
        arr3[i] = flatten[i].avgAge()
        #arr[i] = rootfold.subs[i].myCount

    print ("==============================For file counts:")
    #print( arr )
    print( "..median :", np.median(arr) )
    print( "..mean : ", np.mean(arr) )
    Q1 = np.percentile(arr, 25)
    Q3 = np.percentile(arr, 75)
    #print( "Q1 : ", Q1 )
    #print( "Q3 : ", Q3 )
    IQR = Q3 - Q1
    #print ("IQR : ", IQR)

    IF1 = Q1 - 1.5 * IQR
    IF2 = Q3 + 1.5 * IQR
    OF1 = Q1 - 3.0 * IQR
    OF2 = Q3 + 3.0 * IQR
    for i in range(count):
        try:
            if flatten[i].myCount > OF2:
                print("..major outlier : ", flatten[i].fullPath(), flatten[i].myCount)
            elif flatten[i].myCount > IF2:
                print("..minor outlier : ", flatten[i].fullPath(), flatten[i].myCount)
        except:
            print("print fail", flatten[i].fullPath().encode('ascii', 'ignore'))
            
    print("==============================Outliers average size:")
    
    print( "  median :", human(np.median(arr2)) )
    print( "  mean : ", human(np.mean(arr2)) )
    Q1 = np.percentile(arr2, 25)
    Q3 = np.percentile(arr2, 75)
    #print( "Q1 : ", Q1 )
    #print( "Q3 : ", Q3 )
    IQR = Q3 - Q1
    #print ("IQR : ", IQR)

    IF1 = Q1 - 1.5 * IQR
    IF2 = Q3 + 1.5 * IQR
    OF1 = Q1 - 3.0 * IQR
    OF2 = Q3 + 3.0 * IQR
    bucket = []
    for i in range(count):
        if flatten[i].avgSize() > OF2:
            bucket.append((True,flatten[i].fullPath(), flatten[i].avgSize()))
#            print("..major outlier : ", flatten[i].fullPath(), human(flatten[i].avgSize()))
        elif flatten[i].avgSize() > IF2:
            bucket.append((False,flatten[i].fullPath(), flatten[i].avgSize()))
#            print("..minor outlier : ", flatten[i].fullPath(), human(flatten[i].avgSize()))

    bucket.sort(key=itemgetter(0,2), reverse=True)
    for i in bucket:
        print("  %s: %s %s" % ("Major" if i[0] else "Minor", human(i[2]), i[1]))
        
    print ("============================Outliers modification age [days]:")
    
    print( "  median :", np.median(arr3) )
    print( "  mean2:", np.mean(arr3, dtype="uint32", axis=0))
##    np.save('ages.npy',arr3)
##    print(arr3)
    print(len(arr3))
    print( "..mean : ", np.mean(arr3) )
    print("..sum : ", np.sum(arr3))
    print("avg:", np.sum(arr3) / len(arr3))
    
    Q1 = np.percentile(arr3, 25)
    Q3 = np.percentile(arr3, 75)
    #print( "Q1 : ", Q1 )
    #print( "Q3 : ", Q3 )
    IQR = Q3 - Q1
    #print ("IQR : ", IQR)

    IF1 = Q1 - 1.5 * IQR
    IF2 = Q3 + 1.5 * IQR
    OF1 = Q1 - 3.0 * IQR
    OF2 = Q3 + 3.0 * IQR
    bucket = []
    for i in range(count):
        if flatten[i].avgAge() > OF2:
            bucket.append((True, flatten[i].fullPath(), flatten[i].avgAge()))
#            print("..major outlier : ", flatten[i].fullPath(), flatten[i].avgAge())
        elif flatten[i].avgAge() > IF2:
            bucket.append((False, flatten[i].fullPath(), flatten[i].avgAge()))
#            print("..minor outlier : ", flatten[i].fullPath(), flatten[i].avgAge())

    bucket.sort(key=itemgetter(0,2), reverse=True)
    for i in bucket:
        print("  %s: %s %s" % ("Major" if i[0] else "Minor", i[2], i[1]))
