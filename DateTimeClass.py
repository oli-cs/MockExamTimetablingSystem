
#!class is now deprecated, use the datetime module
class DateTime():
    def __init__(self,day,month,year):
        self.day = day
        self.month = month
        self.year = year
        self.date = str(self.day) + "/" + str(self.month) + "/" + str(self.year)
        self.hour = 0 #24 hour format
        self.minuite = 0
    
    def __copy__(self):
        return DateTime(self.day,self.month,self.year)