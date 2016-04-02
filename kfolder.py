def human(num, power="b"):
    powers=["b","K","M","G","T"]
    while num >= 1000:
        num /= 1024.0
        power=powers[powers.index(power)+1]
        human(num,power)
    return "%.2f%s" % (num,power)

class kFolder:
    def __init__(self):
        self.parent = self
        self.name = ''
        self.path = ''
        self.subs = []
        self.mySize = 0
        self.myUsed = 0
        self.myCount = 0
        self.totSize = 0
        self.totUsed = 0
        self.totCount = 0
        self.myAgeDays = 0 # modify time

    def add_file(self, path, size, used):
        self.myCount += 1
        self.mySize += size
        self.myUsed += used
        self.totCount += 1
        self.totSize += size
        self.totUsed += used
        # todo: add to file list for later statistics

    def add_file(self, path, size, used, ageDays):
        self.myCount += 1
        self.mySize += size
        self.myUsed += used
        self.totCount += 1
        self.totSize += size
        self.totUsed += used
        self.myAgeDays += ageDays

    def add_fold(self, folder):
        self.subs.append(folder)
        self.totSize += folder.totSize
        self.totUsed += folder.totUsed
        self.totCount += folder.totCount
        folder.parent = self

    def fullPath(self):
        if len(self.name) == 0:
            return self.path
        else:
            return self.path + "/" + self.name
        
    def goodName(self):
        if len(self.name) == 0:
            return "<root>"
        else:
            return self.name
        
    def avgSize(self):
        if (self.myCount == 0):
            return 0
        return self.mySize / self.myCount

    def totAvgSize(self):
        if (self.totCount == 0):
            return 0
        return self.totSize / self.totCount
        
    def avgAge(self):
        if (self.myCount == 0):
            return 0
        return self.myAgeDays / self.myCount

    def get_title(self):
        return ["Folder","Local","LUsed","Total","TUsed","LFiles","TFiles","Subd","AvgSz"]
    
    def get_row(self):
        return [self.goodName(), \
                human(self.mySize),human(self.myUsed), \
                human(self.totSize),human(self.totUsed), \
                str(self.myCount),str(self.totCount),str(len(self.subs)),\
                human(self.totAvgSize())]
        
    def __str__(self):
        return "%s;%s(%s);%s(%s);%s;%s;%s;%s" % (self.goodName(), \
                                        human(self.mySize),human(self.myUsed), \
                                        human(self.totSize),human(self.totUsed), \
                                        self.myCount,self.totCount,len(self.subs),\
                                        human(self.totSize/self.totCount))
