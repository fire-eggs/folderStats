# folderStats
Python scripts to perform 'dirusage' functionality.

##### Interface

`python3 test.py [-stats] [-counts] <path to folder>`

Default (no options) is to collect and print rolled up folder data ordered by size.
The `-counts` option will additionally print rolled up folder data ordered by file counts.
The `-stats` option will perform statistical analysis on folders and print outliers regarding size, number of files and age.

##### Requires

1. numpy (when using -stats)
2. python 3.5 (for os.scandir)

##### Example

```
>python3 test.py r:/pix/a/to_sort
Folder sizes: r:/pix/a/to_sort
                        Folder    Local    LUsed    Total    TUsed  LFiles  TFiles  Subd    AvgSz
                        <root>  922.07K  924.00K    3.13G    3.14G       1    8126    10  403.80K
                      AutoDone  522.70M  526.13M    1.53G    1.54G    1775    5241    27  306.67K
                        ny2016  650.45M  652.90M  810.59M  813.11M    1268    1300     1  638.50K
                  new_gelbooru    0.00b    0.00b  311.90M  313.07M       0     612     2  521.87K
                 halloween2015  171.88M  172.18M  171.88M  172.18M     162     162     0    1.06M
                           new    9.72M    9.73M  142.68M  143.41M       7     382     5  382.48K
                          new2   26.94M   27.00M   59.04M   59.17M      35      73     8  828.18K
                   new2 - Copy   59.04M   59.17M   59.04M   59.17M      73      73     0  828.18K
            manga_and_artbooks   47.94M   48.25M   56.86M   57.23M     163     200     9  291.13K
          found in wrong place   18.10M   18.22M   18.10M   18.22M      74      74     0  250.52K
usashiro mani - piyodera mucha    3.78M    3.80M    3.78M    3.80M       8       8     0  483.97K
```

- Local : this folder's file sizes
- LUsed : Windows blocks
- Total : this folder's and all sub folders file sizes
- TUsed : Windows blocks
- LFiles : this folder's file count
- TFiles : this folders's and all sub folders file count
- Subd: count of subfolders at this level
- AvgSz : average file size in this and all sub folders

The `-stats` option produces a lot of output so I won't show all of it, but here are two examples from the above folder:
```
==============================Outliers average size:
  median : 307.39K
  mean :  398.55K
  Major: 5.00M r:/pix/a/to_sort\ny2016/known artbook
```
The specific folder has an average file size of 5M, which is a major outlier from the median of 307K. I.e. the folder has much larger-than-usual files. The `-stats` option can help identify folders with more files, larger files or older files.
