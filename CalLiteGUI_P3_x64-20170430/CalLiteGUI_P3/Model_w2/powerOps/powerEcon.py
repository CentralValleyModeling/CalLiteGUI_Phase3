
class powerEcon:
    def __init__(self, fl):
        import csv
        fl = open(fl, "rb")
        csvFile = csv.reader(fl)
        i = 1
        index = []
        for row in csvFile:
            if '!' in row[0]:
                pass
            else:
                if i == 1:
                    j = 0
                    for data in row:
                        if j > 0:
                            setattr(self, data, dict())
                            index.append(data)
                        j += 1
                else:
                    for j in range( 1, len(row) ):
                        getattr( self, index[ j - 1 ] )[ row[0] ] = row[ j ]
                    
                i += 1
            
        fl.close()
        




