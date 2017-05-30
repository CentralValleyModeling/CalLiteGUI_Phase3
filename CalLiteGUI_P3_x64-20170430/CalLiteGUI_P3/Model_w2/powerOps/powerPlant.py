####################################################################
# Author: Patrick Ho, MBK Engineers
# Date: June 23, 2015
# Description: Implementing LTGen and SWPGen calculations in Jython
####################################################################

import HEC
import os
from peaking import *
from powerEcon import *

# taf, static storage used in energy factor formula of San Luis Reservoir
oNeilStorage = 25.0

a = powerEcon("./tables/powerCosts.in")

class powerPlant:
    
    #constructor
    def __init__(self, *args, **kwargs):        
            
        # populate members using arguments
        try:
            self.facility = kwargs.pop("facility")
            self.dvFile = kwargs.pop("dv")
            self.outputDSS = kwargs.pop("outputDSS")
            self.releasePath = kwargs.pop("release")
            self.start = kwargs.pop("start")
            self.end = kwargs.pop("end")           
            self.characteristics = kwargs.pop("characteristics")
            self.months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]           
        except:
            raise self.usage()

        try:
            self.energyFactor_rate = kwargs.pop("energyFactor")
        except:
            self.energyFactor_rate = "STATIC"
            
        try:
            self.unitCap_rate = kwargs.pop("unitCap")
        except:
            self.unitCap_rate = None

        try:
            self.elevation_rate = kwargs.pop("elevation")
        except:
            self.elevation_rate = None
            
        try:
            self.storPath = kwargs.pop("storage")
        except:
            self.storPath = None
        
        try:
            self.flowInPath = kwargs.pop("flowIn")
        except:
            self.flowInPath = None
        try:
            self.storageFlag = kwargs.pop("storageFlag")
        except:
            self.storageFlag = 1

        try:
            self.tailRace_rate = kwargs.pop("tailRace")
        except:
            self.tailRace_rate = None
            
        try:
            self.availCap_rate = kwargs.pop("availCap")
        except:
            self.availCap_rate = None
            pass
        
        self.storageTS = ""
        self.releaseTS = ""

        #grab data from DV file
        self.getData()

        #build conversion structure
        self.getCfs2Taf()

        #calculate power plant characteristics
        self.ppChar()

        #calculate maximum possible powerplant
        self.maxPosPP()

        #calculate energy at plant
        self.energyAtPlant()

        #calculate actual energy at load center
        self.actualEnergyAtLC()

        #calculate capacity at load center
        self.capacityAtLC()

        
    def getData(self):
        
        fl = HEC.openDSS(self.dvFile)

        if self.storPath and len(self.storPath) == 2:
            self.storageTS0 = HEC.getDssTsValues( fl, self.storPath[0], self.start, self.end)
            self.storageTS1 = HEC.getDssTsValues( fl, self.storPath[1], self.start, self.end)
            
        elif self.storPath and len(self.storPath) == 3:
            self.storageTS0 = HEC.getDssTsValues( fl, self.storPath[0], self.start, self.end)
            self.storageTS1 = HEC.getDssTsValues( fl, self.storPath[1], self.start, self.end)        
            self.storageTS2 = HEC.getDssTsValues( fl, self.storPath[2], self.start, self.end)
            
        elif self.storPath:
            self.storageTS = HEC.getDssTsValues( fl, self.storPath, self.start, self.end)

        self.releaseTS = HEC.getDssTsValues( fl, self.releasePath, self.start, self.end)

        if self.flowInPath:
            self.flowInTS = HEC.getDssTsValues( fl, self.flowInPath, self.start, self.end)

        if self.facility in ["oNeilPP", "cvpSanLuisPP", "swpSanLuisPP"]:
            self.genReleaseTS = list()
            for i in range(len(self.flowInTS)):
                self.genReleaseTS.append( [ self.flowInTS[i][0], max( self.releaseTS[i][1] - self.flowInTS[i][1], 0 ) ] )

        fl.close()

    def getCfs2Taf(self):

        self.cfs2taf = {}
        
        for q in self.releaseTS:
            self.cfs2taf[ q[0] ] = 0.001 * 24.0 * 60.0 * 60.0 * float(HEC.getDaysInMonth(q[0])) / 43560.0

    # Powerplant characteristics
    def ppChar( self ):
        
        # EXCEL CALCULATION - POPULATE STORAGE COLUMNS

        self.minStorage = list()
        self.meanStorage = list()
        self.minStorage0 = list()
        self.meanStorage0 = list()
        self.minStorage1 = list()
        self.minStorage2 = list()
        self.meanStorage1 = list()
        self.meanStorage2 = list()
        self.usedStorage = list()
        self.usedStorage0 = list()
        self.usedStorage1 = list()

        # powerplant regressions depends on storage of one reservoir
        if self.facility in ["trinityPP", "carrPP", "shastaPP", "keswickPP", "folsomPP",
                             "nimbusPP", "newMelonesPP", "thermalitoPP", "devilCanyonPP"]:
            
            i = 1
            for stor in self.storageTS:    
                if i == 1:
                    self.minStorage.append(stor)
                    self.meanStorage.append(stor)
                else:
                    self.minStorage.append([ stor[0], min( prev, stor[1] )])
                    self.meanStorage.append([ stor[0], 0.5 * ( prev + stor[1] )])

                prev = stor[1]
                i+=1
                
            if self.storageFlag == 1:
                self.usedStorage = self.meanStorage
            else:
                self.usedStorage = self.minStorage

            HEC.setDssTsValues( self.outputDSS, self.usedStorage, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"STORAGE-USED")
                                , 0, "TAF", "STORAGE" )

        # powerplant regressions depends on storage of two reservoirs            
        elif self.facility in ["springCreekPP", "orovillePP", "castaicPP"]:

            i = 1
            
            for stor in self.storageTS0:

                if i == 1:
                    self.minStorage0.append(stor)
                    self.meanStorage0.append(stor)
                else:
                    self.minStorage0.append([ stor[0], min( prev, stor[1] )])
                    self.meanStorage0.append([ stor[0], 0.5 * ( prev + stor[1] )])

                prev = stor[1]
                i+=1

            i = 1
            for stor in self.storageTS1:
                if i == 1:
                    self.minStorage1.append(stor)
                    self.meanStorage1.append(stor)
                else:
                    self.minStorage1.append([ stor[0], min( prev, stor[1] )])
                    self.meanStorage1.append([ stor[0], 0.5 * ( prev + stor[1] )])

                prev = stor[1]
                i+=1
                
            if self.storageFlag == 1:
                self.usedStorage =self.meanStorage0
                self.usedStorage0 = self.meanStorage0
                self.usedStorage1 = self.meanStorage1
            else:
                self.usedStorage = self.minStorage0
                self.usedStorage0 = self.minStorage0
                self.usedStorage1 = self.minStorage1

            if self.facility == "springCreekPP":
                HEC.setDssTsValues( self.outputDSS, self.usedStorage0, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"STORAGE-USED-UPSTREAM")
                                    , 0, "TAF", "STORAGE" )
                HEC.setDssTsValues( self.outputDSS, self.usedStorage1, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"STORAGE-USED-DOWNSTREAM")
                                    , 0, "TAF", "STORAGE" )
            else: #orovillePP
                HEC.setDssTsValues( self.outputDSS, self.usedStorage0, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"STORAGE-USED")
                                    , 0, "TAF", "STORAGE" )                

        # powerplant regressions requiring three variables
        elif self.facility in ["cvpSanLuisPP", "swpSanLuisPP"]:
            i = 1
            
            for stor in self.storageTS0:

                if i == 1:
                    self.minStorage0.append(stor)
                    self.meanStorage0.append(stor)
                else:
                    self.minStorage0.append([ stor[0], min( prev, stor[1] )])
                    self.meanStorage0.append([ stor[0], 0.5 * ( prev + stor[1] )])

                prev = stor[1]
                i+=1

            i = 1
            for stor in self.storageTS1:
                if i == 1:
                    self.minStorage1.append(stor)
                    self.meanStorage1.append(stor)
                else:
                    self.minStorage1.append([ stor[0], min( prev, stor[1] )])
                    self.meanStorage1.append([ stor[0], 0.5 * ( prev + stor[1] )])

                prev = stor[1]
                i+=1

            i = 1
            for stor in self.storageTS2:
                if i == 1:
                    self.minStorage2.append(stor)
                    self.meanStorage2.append(stor)
                else:
                    self.minStorage2.append([ stor[0], min( prev, stor[1] )])
                    self.meanStorage2.append([ stor[0], 0.5 * ( prev + stor[1] )])

                prev = stor[1]
                i+=1
                
            if self.storageFlag == 1:
                for i in range(len(self.meanStorage0)):
                    self.usedStorage.append( [ self.meanStorage0[i][0],
                                          self.meanStorage0[i][1] + self.meanStorage1[i][1] + self.meanStorage2[i][1] ] )
            else:
                for i in range(len(self.minStorage0)):
                    self.usedStorage.append( [ self.minStorage0[i][0],
                                          self.minStorage0[i][1] + self.minStorage1[i][1] + self.minStorage2[i][1] ] )

            HEC.setDssTsValues( self.outputDSS, self.usedStorage, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"STORAGE-USED")
                                , 0, "TAF", "STORAGE" )
        
        # EXCEL CALCULATION - POPULATE ELEVATION COLUMN

        self.elevation = list()
        self.elevation0 = list()
        self.elevation1 = list()

        # elevation formula uses storage as argument
        if self.facility in [ "trinityPP", "shastaPP", "keswickPP", "folsomPP", "nimbusPP",
                             "newMelonesPP", "orovillePP", "thermalitoPP", "devilCanyonPP", "castaicPP" ]:
        
            for stor in self.usedStorage:
                self.elevation.append([ stor[0], self.elevation_rate(stor[1]) ])

            HEC.setDssTsValues( self.outputDSS, self.elevation, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"ELEVATION")
                               , 0, "FT", "STAGE" )

        # elevation formula uses reservoir elevation upstream and downstream as arguments
        elif self.facility in ["carrPP"]:
            
            for stor in self.usedStorage:
                self.elevation0.append( [ stor[0], self.elevation_rate[0](stor[1]) ] )
                self.elevation1.append( [ stor[0], self.elevation_rate[1](stor[1]) ] )

            HEC.setDssTsValues( self.outputDSS, self.elevation0, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"ELEVATION-UPSTREAM")
                               , 0, "FT", "STAGE" )
            HEC.setDssTsValues( self.outputDSS, self.elevation1, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"ELEVATION-DOWNSTREAM")
                               , 0, "FT", "STAGE" )

        # elevation formula uses reservoir storage upstream and downstream as arguments
        elif self.facility in ["springCreekPP"]:
            
            for i in range (len(self.usedStorage0)):
                self.elevation0.append([ self.usedStorage0[i][0], self.elevation_rate[0]( self.usedStorage0[i][1] )])
                self.elevation1.append([ self.usedStorage1[i][0], self.elevation_rate[1]( self.usedStorage1[i][1] )])

            HEC.setDssTsValues( self.outputDSS, self.elevation0, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"ELEVATION-UPSTREAM")
                               , 0, "FT", "STAGE" )
            HEC.setDssTsValues( self.outputDSS, self.elevation1, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"ELEVATION-DOWNSTREAM")
                               , 0, "FT", "STAGE" )
        
        elif self.facility in ["cvpSanLuisPP", "swpSanLuisPP"]:

            for stor in self.usedStorage:
                self.elevation.append( [ stor[0], self.elevation_rate(stor[1], 0) ] )

            HEC.setDssTsValues( self.outputDSS, self.elevation, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"ELEVATION")
                               , 0, "FT", "STAGE" )
        
        # EXCEL CALCULATION - POPULATE TAIL RACE COLUMN
        self.tailRace = list()

        # using no arguments in tail race formula
        if self.facility in ["trinityPP", "thermalitoPP", "devilCanyonPP"]:
           
            for stor in self.usedStorage:
                self.tailRace.append([ stor[0], self.tailRace_rate() ])
                            
        # using flow as argument in tail race formula
        elif self.facility in ["shastaPP", "keswickPP", "folsomPP", "nimbusPP", "newMelonesPP"]:
        
            for q in self.releaseTS:
                self.tailRace.append([ q[0], self.tailRace_rate(q[1]) ])
                
        #using downstream storage as argument in tail race formula                   
        elif self.facility in ["orovillePP", "warnePP", "castaicPP"]:

            for s in self.storageTS1:    
                self.tailRace.append( [ s[0], self.tailRace_rate(s[1]) ])
        
        try:
            HEC.setDssTsValues( self.outputDSS, self.tailRace, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"TAIL-RACE")
                                , 0, "FT", "STAGE" )
        except:
            pass
                            
        # EXCEL CALCULATION - POPULATE ENERGY FACTOR COLUMN

        self.energyFactor = list()

        # using elevation and tailRace as arguments in energy factor formula
        if self.facility in ["trinityPP", "shastaPP", "keswickPP", "folsomPP", "nimbusPP", "newMelonesPP",
                             "orovillePP", "thermalitoPP", "castaicPP"]:
        
            for i in range( 0, len(self.elevation) ):
                
                self.energyFactor.append([ self.elevation[i][0],
                        self.energyFactor_rate( self.elevation[i][1],
                                                self.tailRace[i][1] ) ])

        # using upstream and downstream elevation as arguments in energy factor formula                
        elif self.facility in ["carrPP", "springCreekPP"]:
            
            for i in range( 0, len(self.elevation0) ):

                self.energyFactor.append([ self.elevation0[i][0],
                        self.energyFactor_rate( self.elevation0[i][1],
                                                self.elevation1[i][1] ) ])
                
        # using upstream and downstream storage as arguments in energy factor formula
        elif self.facility in ["cvpSanLuisPP", "swpSanLuisPP"]:

            for stor in self.usedStorage:
                
                self.energyFactor.append( [ stor[0], self.energyFactor_rate( stor[1], oNeilStorage) ] )

        # using zero as argument in energy factor formula
        elif self.facility in ["oNeilPP"]:

            for qOut in self.releaseTS:

                self.energyFactor.append( [ qOut[0], self.energyFactor_rate( 0 ) ] )
                
        # using energy factor from characteristics table (*.in file)
        elif self.facility in ["alamoPP", "mojavePP", "devilCanyonPP", "warnePP"]:

            for q in self.releaseTS:

                self.energyFactor.append( [ q[0],
                                            float(self.characteristics.energyFactor[ self.months[ q[0].getMonth() ] ] )] )
             
        HEC.setDssTsValues( self.outputDSS, self.energyFactor, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"ENERGY-FACTOR")
                            , 0, "kWh/AF", "POWER-GENERATION-PER-VOLUME" )
        
        # EXCEL CALCULATION - POPULATE UNIT CAPACITY COLUMN
        
        self.unitCap = list()

        # using elevation and tail race as arguments in unit capacity equation
        if self.facility in ["trinityPP", "shastaPP", "keswickPP", "folsomPP", "nimbusPP", "newMelonesPP"]:

            for i in range( 0, len(self.elevation) ):

                self.unitCap.append( [ self.elevation[i][0],
                        self.unitCap_rate( self.elevation[i][1],
                                           self.tailRace[i][1] )] )
                
        # using upstream and downstream elevation as arguments in unit capacity equation                
        elif self.facility in ["carrPP", "springCreekPP"]:

            for i in range( 0, len(self.elevation0) ):

                self.unitCap.append( [ self.elevation0[i][0],
                        self.unitCap_rate( self.elevation0[i][1],
                                          self.elevation1[i][1]) ] )

        # using upstream and downstream storage as arguments in unit capacity equation                
        elif self.facility in ["cvpSanLuisPP", "swpSanLuisPP"]:

            for stor in self.usedStorage:

                self.unitCap.append( [stor[0], self.unitCap_rate( stor[1], oNeilStorage )] )
                
        elif self.facility in ["oNeilPP"]:

            for qOut in self.releaseTS:

                self.unitCap.append( [ qOut[0], 3.0 ] )

        try:
            HEC.setDssTsValues( self.outputDSS, self.unitCap, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"UNIT-CAPACITY")
                                , 0, "MW", "POWER" )
        except:
            pass
        
        # EXCEL CALCULATION - POPULATE AVAILABLE CAPACITY COLUMN
            
        self.availCap = list()

        # using unit capacity and number of units in available capacity equation                    
        if self.facility in ["trinityPP", "carrPP", "springCreekPP", "shastaPP", "folsomPP",
                             "newMelonesPP", "cvpSanLuisPP", "swpSanLuisPP"]:
            
            for cap in self.unitCap:
            
                self.availCap.append( [ cap[0],
                    cap[1] *
                    float(self.characteristics.noUnits[ self.months[ cap[0].getMonth() ]]) *
                    float(self.characteristics.capShare[ self.months[ cap[0].getMonth() ] ]) ] )

        # using release, energyfactor, unit capacity, and number of units in available capacity
        # equation
        elif self.facility in ["keswickPP", "nimbusPP"]:

            for i in range(len(self.releaseTS)):
                
                self.availCap.append( [ self.releaseTS[i][0],
                                   self.availCap_rate(self.releaseTS[i][1],
                                                     self.energyFactor[i][1],
                                                     self.unitCap[i][1],
                                                     float(self.characteristics.noUnits[ self.months[ self.unitCap[i][0].getMonth() ] ])) ])

        # using release, energyfactor, unit capacity, and number of units in available capacity
        # equation        
        elif self.facility in ["oNeilPP"]:
            
            for i in range(len(self.releaseTS)):
                
                self.availCap.append( [ self.releaseTS[i][0],
                                   self.availCap_rate(self.genReleaseTS[i][1],
                                                     self.energyFactor[i][1],
                                                     self.unitCap[i][1],
                                                     float(self.characteristics.noUnits[ self.months[ self.unitCap[i][0].getMonth() ] ])) ])

        elif self.facility in ["orovillePP", "thermalitoPP", "devilCanyonPP", "warnePP", "castaicPP"]:

            if self.facility == "warnePP": #not very elegant, but will work, don't want to build another If Block just for warne. Ho, P
                self.elevation = [[q[0], 3299.0] for q in self.releaseTS]
                
            for i in range( len( self.elevation ) ):

                self.availCap.append( [ self.elevation[i][0],
                                        min( self.availCap_rate(self.elevation[i][1] - self.tailRace[i][1],
                                                                self.releaseTS[i][1],
                                                                float(self.characteristics.efficiency[ self.months[ self.elevation[i][0].getMonth() ] ])),
                                             float(self.characteristics.powerRating[ self.months[ self.elevation[i][0].getMonth() ] ]) ) ] )
                
        elif self.facility in ["alamoPP", "mojavePP"]:
            
            head = { "alamoPP": 133.0, "mojavePP": 135.0 }
                       
            for q in self.releaseTS:
            
                self.availCap.append( [ q[0],
                                        min( self.availCap_rate(head[ self.facility ],
                                                                q[1],
                                                                float(self.characteristics.efficiency[ self.months[ q[0].getMonth() ] ])),
                                             float(self.characteristics.powerRating[ self.months[ q[0].getMonth() ] ]) ) ] )
                                        
        try:
            HEC.setDssTsValues( self.outputDSS, self.availCap, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-CHARACTERISTICS/" % (self.facility,"AVAILABLE-CAPACITY")
                               , 0, "MW", "POWER" )
        except:
            pass
        
    # Maximum Possible Powerplant (MPP)
    def maxPosPP( self ):
        peak = peakingSchedule("./tables/peakingPercentage.in")

        # EXCEL CALCULATION - POPULATE MPP Energy

        self.MPPEnergy = list()

        # using available capacity to determine MPP energy
                            
        if self.facility in ["trinityPP", "carrPP", "springCreekPP", "shastaPP",
                             "folsomPP", "newMelonesPP", "cvpSanLuisPP", "oNeilPP",
                             "orovillePP", "thermalitoPP", "swpSanLuisPP", "alamoPP",
                             "mojavePP", "devilCanyonPP", "warnePP", "castaicPP"]:
            
            for i in range( len(self.availCap) ):
            
                self.MPPEnergy.append( [ self.availCap[i][0],
                                         0.001 * self.availCap[i][1] *
                                         ( peak.onPeakHours [ str( 1900 + self.availCap[i][0].getYear() + 0.01 * ( self.availCap[i][0].getMonth() + 1 ) ) ] +
                                           peak.offPeakHours [ str( 1900 + self.availCap[i][0].getYear() + 0.01 * ( self.availCap[i][0].getMonth() + 1 ) ) ] ) ] )

        # using unit capacity to determine MPP energy
        elif self.facility in ["keswickPP", "nimbusPP"]:

            for i in range( len( self.unitCap ) ):
                self.MPPEnergy.append( [ self.unitCap[i][0],
                                         0.001 * self.unitCap[i][1] *
                                         ( peak.onPeakHours [ str( 1900 + self.availCap[i][0].getYear() + 0.01 * ( self.availCap[i][0].getMonth() + 1 ) ) ] +
                                           peak.offPeakHours [ str( 1900 + self.availCap[i][0].getYear() + 0.01 * ( self.availCap[i][0].getMonth() + 1 ) ) ] ) *
                                           float(self.characteristics.noUnits[ self.months[ self.unitCap[i][0].getMonth() ] ]) ] )
                
        HEC.setDssTsValues( self.outputDSS, self.MPPEnergy, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-POTENTIAL/" % (self.facility,"ENERGY")
                           , 0, "GW-Hour", "ENERGY" )
                
        # EXCEL CALCULATION - POPULATE MPP Release

        self.MPPRelease = list()

        if self.facility in [ "trinityPP", "newMelonesPP" ]:

            minElevation = { "trinityPP":2213.0, "newMelonesPP":808.0 }
            
            for i in range( len(self.elevation) ):
                
                if self.elevation[i][1] > minElevation[self.facility]:
                    self.MPPRelease.append( [ self.elevation[i][0],
                                              1000.0 * self.MPPEnergy[i][1] / self.energyFactor[i][1] ])
                else:
                    self.MPPRelease.append( [self.elevation[i][0], 0.0] )
                    
        elif self.facility in ["carrPP", "springCreekPP", "shastaPP", "keswickPP",
                               "folsomPP", "nimbusPP", "cvpSanLuisPP", "oNeilPP",
                               "orovillePP", "thermalitoPP", "swpSanLuisPP", "alamoPP",
                               "mojavePP", "devilCanyonPP", "warnePP", "castaicPP"]:
            
            for i in range( len(self.energyFactor) ):
                if self.energyFactor[i][1] > 0.0:
                    self.MPPRelease.append( [ self.energyFactor[i][0],
                                              1000.0 * self.MPPEnergy[i][1] / self.energyFactor[i][1] ])
                else:
                    self.MPPRelease.append( [self.energyFactor[i][0], 0.0] )    

        HEC.setDssTsValues( self.outputDSS, self.MPPRelease, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-POTENTIAL/" % (self.facility,"RELEASE")
                           , 0, "TAF", "FLOW" )

    # Energy at Plant Computations (EPC)
    def energyAtPlant( self ):

        # EXCEL CALCULATION - POPULATE EPC Powerplant Release

        self.EPCPPRelease = list()

        if self.facility in ["trinityPP", "carrPP", "springCreekPP", "shastaPP", "keswickPP",
                             "folsomPP", "nimbusPP", "newMelonesPP", "orovillePP", "thermalitoPP",
                             "alamoPP", "mojavePP", "devilCanyonPP", "warnePP", "castaicPP"]:

            for i in range( len(self.releaseTS) ):
                self.EPCPPRelease.append( [ self.releaseTS[i][0],
                                            min( self.releaseTS[i][1] * self.cfs2taf[ self.releaseTS[i][0] ],
                                                 self.MPPRelease[i][1],
                                                 float(self.characteristics.maxFlow[ self.months[ self.releaseTS[i][0].getMonth() ] ]) * float(self.cfs2taf[ self.releaseTS[i][0] ])) ] )
                
        elif self.facility in ["cvpSanLuisPP", "oNeilPP", "swpSanLuisPP"]:

            for i in range( len(self.genReleaseTS) ):

                self.EPCPPRelease.append( [ self.genReleaseTS[i][0],
                                            min( self.genReleaseTS[i][1] * self.cfs2taf[ self.genReleaseTS[i][0] ],
                                                 self.MPPRelease[i][1] )] )
                
        HEC.setDssTsValues( self.outputDSS, self.EPCPPRelease, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-GENERATION/" % (self.facility,"RELEASE")
                           , 0, "TAF", "FLOW" )
        
        # EXCEL CALCULATION - POPULATE EPC Energy

        self.EPCEnergy = list()

        for i in range( len(self.energyFactor) ):

            self.EPCEnergy.append( [ self.energyFactor[i][0],
                                     0.001 * self.energyFactor[i][1] * self.EPCPPRelease[i][1]] )            

        HEC.setDssTsValues( self.outputDSS, self.EPCEnergy, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-GENERATION/" % (self.facility,"ENERGY")
                           , 0, "GW-Hour", "Energy" )
            
        # EXCEL CALCULATION - POPULATE EPC Spill

        self.EPCSpill = list()

        if self.facility in ["trinityPP", "carrPP", "springCreekPP", "shastaPP",
                             "keswickPP", "folsomPP", "nimbusPP", "newMelonesPP",
                             "orovillePP", "thermalitoPP", "alamoPP", "mojavePP",
                             "devilCanyonPP", "warnePP", "castaicPP"]:
            
            for i in range( len(self.releaseTS) ):

                self.EPCSpill.append( [ self.releaseTS[i][0],
                                         max( self.releaseTS[i][1] * self.cfs2taf[ self.releaseTS[i][0] ]
                                              - self.EPCPPRelease[i][1], 0.0)] )

        elif self.facility in ["cvpSanLuisPP", "oNeilPP", "swpSanLuisPP"]:

            for i in range( len(self.genReleaseTS) ):

                self.EPCSpill.append( [ self.genReleaseTS[i][0],
                                            max( self.genReleaseTS[i][1] * self.cfs2taf[ self.genReleaseTS[i][0] ]
                                                 - self.EPCPPRelease[i][1], 0.0 ) ] )

        HEC.setDssTsValues( self.outputDSS, self.EPCSpill, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-GENERATION/" % (self.facility,"SPILL")
                           , 0, "TAF", "FLOW" )
                
        # EXCEL CALCULATION - POPULATE EPC Forgone Energy

        self.EPCForgone = list()

        for i in range( len(self.energyFactor) ):
            self.EPCForgone.append( [ self.energyFactor[i][0], 0.001 * self.EPCSpill[i][1] * self.energyFactor[i][1] ] )
            
        HEC.setDssTsValues( self.outputDSS, self.EPCForgone, self.start, "/HYDROPOWER/%s/%s//1MON/POWERPLANT-GENERATION/" % (self.facility,"FORGONE")
                           , 0, "GW-Hour", "Energy" )            
            
    # Actual Energy at Load Center (ELC)
    def actualEnergyAtLC( self ):

        # EXCEL CALCULATION - POPULATE ELC Loss

        self.percentLoss = list()

        for q in self.releaseTS:
            self.percentLoss.append( [ q[0], float(self.characteristics.transmissionLoss[ self.months[ q[0].getMonth() ]]) ] )

        HEC.setDssTsValues( self.outputDSS, self.percentLoss, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-AT-LC/" % (self.facility,"PERCENT-LOSS")
                           , 0, "PERCENT", "LOSS" )

        # EXCEL CALCULATION - POPULATE ELC Total Energy

        self.ELCTotal = list()
        revenue = list()
        
        for i in range( len( self.EPCEnergy ) ):
        
            self.ELCTotal.append( [ self.EPCEnergy[i][0], self.EPCEnergy[i][1] * (1.0 - self.percentLoss[i][1] ) ] )
            revenue.append( [ self.EPCEnergy[i][0],
                              self.EPCEnergy[i][1] *
                              (1.0 - self.percentLoss[i][1] ) *
                              0.5 * (float(a.onPeak[ str(self.EPCEnergy[i][0].getMonth() + 1) ]) + float(a.offPeak[ str(self.EPCEnergy[i][0].getMonth() + 1) ]) ) ] )

        HEC.setDssTsValues( self.outputDSS, self.ELCTotal, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-AT-LC/" % (self.facility,"TOTAL")
                           , 0, "GW-Hour", "ENERGY" )

        HEC.setDssTsValues (self.outputDSS, revenue , self.start, "/HYDROPOWER/%s/%s//1MON/ECONOMICS/" % (self.facility, "GENERATION-REVENUE"), 0, "$1,000", "REVENUE")

        # EXCEL CALCULATION - POPULATE ELC Total Energy

        self.ELCLosses = list()
        
        for i in range( len( self.EPCEnergy ) ):
            self.ELCLosses.append( [ self.EPCEnergy[i][0], self.EPCEnergy[i][1] - self.ELCTotal[i][1] ] )

        HEC.setDssTsValues( self.outputDSS, self.ELCLosses, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-AT-LC/" % (self.facility,"LOSSES")
                           , 0, "GW-Hour", "ENERGY" )
        
    # Capacity at Load Center
    def capacityAtLC( self ):
        
        # EXCEL CALCULATION - POPULATE Capacity at Load Center

        self.capAtLC = list()

        for i in range( len( self.percentLoss ) ):
            self.capAtLC.append( [ self.percentLoss[i][0],
                                   self.availCap[i][1] * (1.0 - self.percentLoss[i][1] ) ] )
            
        HEC.setDssTsValues( self.outputDSS, self.capAtLC, self.start, "/HYDROPOWER/%s/%s//1MON/CAPACITY-AT-LC/" % (self.facility,"TOTAL")
                           , 0, "MW", "POWER" )

   
    def usage(self):
        
        raise Usage(
            "\npowerPlant (" +
            "\n        facility = \"name\"," +
            "\n        dv = \"DSS DV file path\"," +
            "\n        Work In Progress\n")

class Usage(Exception):
    
    def __init__(self,value):      
        self.value = value
        
    def __str__(self):
        print self.value
