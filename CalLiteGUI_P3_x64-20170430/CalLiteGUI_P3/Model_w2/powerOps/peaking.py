
class peakingSchedule:
    def __init__(self, fl):
        self.onPeakPercent = dict()
        self.offPeakPercent = dict()
        self.onPeakHours = dict()
        self.offPeakHours = dict()
        
        fl = open(fl, "rb")
        import csv
        csvfile = csv.reader(fl)
        i = 1
        index = []
        for row in csvfile:
            if i == 1:
                for data in row:
                    setattr(self, data, list())
                    index.append(data)
            
            else:
                for j in range( len(row) ):
                    getattr( self, index[ j ] ).append( row[ j ] )            
            i += 1
               
        for i in range(len( getattr( self, index[2] ) )):
            self.onPeakPercent[ getattr( self, index[2] )[i] ] = float(getattr( self, index[3] )[i])
            self.offPeakPercent[ getattr( self, index[2] )[i] ] = 1.0 - float(getattr( self, index[3] )[i])
            self.onPeakHours[ getattr( self, index[2] )[i] ] = float(getattr( self, index[4] )[i])
            self.offPeakHours[ getattr( self, index[2] )[i] ] = float(getattr( self, index[5] )[i])
    
        fl.close()
        
