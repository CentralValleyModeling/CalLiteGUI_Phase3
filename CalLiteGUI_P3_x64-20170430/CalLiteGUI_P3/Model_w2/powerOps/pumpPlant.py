####################################################################
# Author: Patrick Ho, MBK Engineers
# Date: June 23, 2015
# Description: Implementing LTGen and SWPGen calculations in Jython
####################################################################

import HEC
import os
from peaking import *
from powerEcon import *
import math

peak = peakingSchedule("./tables/peakingPercentage.in")
a = powerEcon("./tables/powerCosts.in")
   
class pumpPlant:
    
    #constructor
    def __init__(self, *args, **kwargs):        
            
        # populate members using arguments
        try:
            self.facility = kwargs.pop("facility")
            self.dvFile = kwargs.pop("dv")
            self.outputDSS = kwargs.pop("outputDSS")
            self.start = kwargs.pop("start")
            self.end = kwargs.pop("end")           
            self.characteristics = kwargs.pop("characteristics")
            self.months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        except:
            raise self.usage()

        try:
            self.pumpingPath = kwargs.pop("pumping")
        except:
            self.pumpingPath = None
            
        try:
            self.energyFactor_rate = kwargs.pop("energyFactor")
        except:
            self.energyFactor_rate = None

        try:
            self.unitCap_rate = kwargs.pop("unitCap")
        except:
            self.unitCap_rate = None

        try:
            self.volInPath = kwargs.pop("volIn")
        except:
            self.volInPath = None

        try:
            self.volOutPath = kwargs.pop("volOut")
        except:
            self.volOutPath = None

        #grab data from DV file
        self.getData()
        
        #build conversion structure
        self.getCfs2Taf()

        #calculate pumping plant characteristics
        self.pumpChar()

        #calculate energy
        self.energyComputation()

        #calculate capacity
        self.computedCapacity()
        
        #calculate actual pumping energy use at load center
        self.pumpingEnergyAtLC()

        #calculate capacity at load center
        self.capacityAtLC()
       
    def getData(self):
        
        fl = HEC.openDSS(self.dvFile)

        if (isinstance(self.pumpingPath, list )):

            self.pumpingTS = HEC.summation(fl, self.pumpingPath, self.start, self.end)

        elif not(self.pumpingPath) and self.volInPath and self.volOutPath:

            self.volIn = HEC.getDssTsValues( fl, self.volInPath, self.start, self.end)
            self.volOut = HEC.getDssTsValues( fl, self.volOutPath, self.start, self.end)
            self.pumpingTS = list()

            for i in range(len(self.volIn)):
                self.pumpingTS.append( [ self.volIn[i][0],
                                         max(self.volIn[i][1] - self.volOut[i][1], 0.0) ] )
            
        else:
            
            self.pumpingTS = HEC.getDssTsValues( fl, self.pumpingPath, self.start, self.end )           
            
        fl.close()

    def getCfs2Taf(self):

        self.cfs2taf = {}
        
        for q in self.pumpingTS:
            self.cfs2taf[ q[0] ] = 0.001 * 24.0 * 60.0 * 60.0 * float(HEC.getDaysInMonth(q[0])) / 43560.0
        
    #calculate pumping plant characteristics
    def pumpChar(self):

        # EXCEL CALCULATION - Energy Factor

        self.energyFactor = list()

        if self.facility in ["tracyPump", "cvpBanksPump", "contraCostaPump", "cvpDosAmigosPump", "corningPump",
                             "redBluffPump", "dmcIntertiePump", "sanLuisOtherPump", "dmcOtherPump", "tcOtherPump",
                             "oNeillPump", "banksPump", "swpDosAmigosPump", "buenaVistaPump", "teerinkPump",
                             "chrismanPump", "edmonstonPump", "pearblossomPump", "osoPump", "southBayPump",
                             "delVallePump", "lasPerillasPump", "badgerHillPump"]:
            for q in self.pumpingTS:
                self.energyFactor.append( [ q[0],
                                            float(self.characteristics.energyFactor[ self.months[ q[0].getMonth() ] ]) ] )

        elif self.facility in ["sanFelipePump"]:
            for s in HEC.getDssTsValues( self.outputDSS, "/HYDROPOWER/CVPSANLUISPP/STORAGE-USED//1MON/POWERPLANT-CHARACTERISTICS/", self.start, self.end):
                self.energyFactor.append( [s[0],
                                           self.energyFactor_rate(s[1])] )
                
        elif self.facility in ["folsomPump"]:
            for s in HEC.getDssTsValues( self.outputDSS, "/HYDROPOWER/FOLSOMPP/STORAGE-USED//1MON/POWERPLANT-CHARACTERISTICS/", self.start, self.end):
                self.energyFactor.append( [s[0],
                                           self.energyFactor_rate(s[1])] )
                
        elif self.facility in ["cvpSanLuisPump"]:
            for s in HEC.getDssTsValues( self.outputDSS, "/HYDROPOWER/CVPSANLUISPP/STORAGE-USED//1MON/POWERPLANT-CHARACTERISTICS/", self.start, self.end):
                self.energyFactor.append( [s[0],
                                           self.energyFactor_rate(s[1], 25.0)] )
                
        elif self.facility in ["swpSanLuisPump"]:
            for s in HEC.getDssTsValues( self.outputDSS, "/HYDROPOWER/SWPSANLUISPP/STORAGE-USED//1MON/POWERPLANT-CHARACTERISTICS/", self.start, self.end):
                self.energyFactor.append( [s[0],
                                           self.energyFactor_rate(s[1], 25.0)] )
                                
        HEC.setDssTsValues( self.outputDSS, self.energyFactor, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPINGPLANT-CHARACTERISTICS/" % (self.facility, "ENERGY-FACTOR")
                           , 0, "kWh/AF", "POWER-GENERATION-PER-VOLUME" )

        # EXCEL CALCULATION - Unit Cap

        self.unitCap = list()

        if self.facility in ["tracyPump", "cvpBanksPump", "contraCostaPump", "sanFelipePump", "cvpDosAmigosPump",
                             "folsomPump", "corningPump", "redBluffPump","dmcIntertiePump", "sanLuisOtherPump",
                             "dmcOtherPump", "tcOtherPump", "oNeillPump", "banksPump", "swpDosAmigosPump", "buenaVistaPump",
                             "teerinkPump", "chrismanPump", "edmonstonPump", "pearblossomPump", "osoPump", "southBayPump",
                             "delVallePump", "lasPerillasPump", "badgerHillPump"]:
            
            for q in self.pumpingTS:
                self.unitCap.append( [ q[0],
                                            float(self.characteristics.unitCap[ self.months[ q[0].getMonth() ] ] ) ] )
        elif self.facility in ["cvpSanLuisPump"]:

            for s in HEC.getDssTsValues( self.outputDSS, "/HYDROPOWER/CVPSANLUISPP/STORAGE-USED//1MON/POWERPLANT-CHARACTERISTICS/", self.start, self.end):
                self.unitCap.append( [s[0],
                                           self.unitCap_rate(s[1], 25.0)] )
                
        elif self.facility in ["swpSanLuisPump"]:

            for s in HEC.getDssTsValues( self.outputDSS, "/HYDROPOWER/SWPSANLUISPP/STORAGE-USED//1MON/POWERPLANT-CHARACTERISTICS/", self.start, self.end):
                self.unitCap.append( [s[0],
                                           self.unitCap_rate(s[1], 25.0)] )                
                
        HEC.setDssTsValues( self.outputDSS, self.unitCap, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPINGPLANT-CHARACTERISTICS/" % (self.facility, "UNIT-CAPACITY")
                           , 0, "MW", "POWER" )

        # EXCEL CALCULATION - # units
     
        self.noUnits = list()

        if self.facility in ["tracyPump", "cvpBanksPump", "contraCostaPump", "sanFelipePump", "cvpDosAmigosPump",
                             "folsomPump", "corningPump", "redBluffPump","dmcIntertiePump", "sanLuisOtherPump",
                             "dmcOtherPump", "tcOtherPump", "oNeillPump", "cvpSanLuisPump", "banksPump",
                             "swpSanLuisPump", "swpDosAmigosPump", "buenaVistaPump", "teerinkPump",
                             "chrismanPump", "edmonstonPump", "pearblossomPump", "osoPump", "southBayPump",
                             "delVallePump", "lasPerillasPump", "badgerHillPump"]:
            
            for q in self.pumpingTS:
                self.noUnits.append( [ q[0],
                                            float(self.characteristics.noUnits[ self.months[ q[0].getMonth() ] ] ) ] )
                
        HEC.setDssTsValues( self.outputDSS, self.noUnits, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPINGPLANT-CHARACTERISTICS/" % (self.facility, "NUMBER-OF-UNITS")
                           , 0, "UNIT", "COUNT" )

        # EXCEL CALCULATION - Off Peak Energy

        self.offPeakPercent = list()

        if self.facility in ["tracyPump", "cvpBanksPump", "contraCostaPump", "sanFelipePump", "cvpDosAmigosPump",
                             "folsomPump", "corningPump", "redBluffPump", "dmcIntertiePump", "sanLuisOtherPump",
                             "dmcOtherPump", "tcOtherPump", "oNeillPump", "cvpSanLuisPump", "banksPump",
                             "swpSanLuisPump", "swpDosAmigosPump", "buenaVistaPump", "teerinkPump",
                             "chrismanPump", "edmonstonPump", "pearblossomPump", "osoPump", "southBayPump",
                             "delVallePump", "lasPerillasPump", "badgerHillPump"]:
            
            for q in self.pumpingTS:
                
                if float(self.characteristics.offPeakPercent[ self.months[ q[0].getMonth() ] ]) < 0.001:
                    self.offPeakPercent.append( [ q[0],
                                                  1.0 - float(peak.onPeakPercent[ str( 1900 + q[0].getYear() + 0.01 * ( q[0].getMonth() + 1 ) ) ]) ] )
                    
                else:
                    self.offPeakPercent.append( [ q[0],
                                                float(self.characteristics.offPeakPercent[ self.months[ q[0].getMonth() ] ] ) ] )
                
        HEC.setDssTsValues( self.outputDSS, self.offPeakPercent, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPINGPLANT-CHARACTERISTICS/" % (self.facility, "OFF-PEAK-PERCENT")
                           , 0, "PERCENT", "OFF-PEAK" )

        # EXCEL CALCULATION - On Peak Energy

        self.onPeakPercent = list()

        if self.facility in ["tracyPump", "cvpBanksPump", "contraCostaPump", "sanFelipePump", "cvpDosAmigosPump",
                             "folsomPump", "corningPump", "redBluffPump","dmcIntertiePump", "sanLuisOtherPump",
                             "dmcOtherPump", "tcOtherPump", "oNeillPump", "cvpSanLuisPump","banksPump",
                             "swpSanLuisPump","swpDosAmigosPump", "buenaVistaPump", "teerinkPump",
                             "chrismanPump", "edmonstonPump", "pearblossomPump", "osoPump", "southBayPump",
                             "delVallePump", "lasPerillasPump", "badgerHillPump"]:
            
            for q in self.pumpingTS:
                
                if float(self.characteristics.offPeakPercent[ self.months[ q[0].getMonth() ] ]) < 0.001:
                    self.onPeakPercent.append( [ q[0],
                                                  float(peak.onPeakPercent[ str( 1900 + q[0].getYear() + 0.01 * ( q[0].getMonth() + 1 ) ) ]) ] )
                    
                else:
                    self.onPeakPercent.append( [ q[0],
                                                1.0 - float(self.characteristics.offPeakPercent[ self.months[ q[0].getMonth() ] ] ) ] )
                        
        HEC.setDssTsValues( self.outputDSS, self.onPeakPercent, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPINGPLANT-CHARACTERISTICS/" % (self.facility, "ON-PEAK-PERCENT")
                           , 0, "PERCENT", "ON-PEAK" )

        # EXCEL CALCULATION - Off-Peak Adjustment Factor
        
        self.offPeakAdj = list()

        for q in self.pumpingTS:

            self.offPeakAdj.append( [ q[0], float(self.characteristics.offPeakCapFactor[ self.months[ q[0].getMonth() ] ] ) ] )

        HEC.setDssTsValues( self.outputDSS, self.offPeakAdj, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPINGPLANT-CHARACTERISTICS/" % (self.facility, "OFF-PEAK-ADJUSTMENT")
                           , 0, "FACTOR", "OFF-PEAK" )           

        # EXCEL CALCULATION - On-Peak Adjustment Factor

        self.onPeakAdj = list()

        for q in self.pumpingTS:

            self.onPeakAdj.append( [ q[0], float(self.characteristics.onPeakCapFactor[ self.months[ q[0].getMonth() ] ] ) ] )

        HEC.setDssTsValues( self.outputDSS, self.onPeakAdj, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPINGPLANT-CHARACTERISTICS/" % (self.facility, "ON-PEAK-ADJUSTMENT")
                           , 0, "FACTOR", "ON-PEAK" )

        # EXCEL CALCULATION - Max Possible Capacity

        self.maxPossibleCap = list()

        for i in range(len(self.pumpingTS)):

            self.maxPossibleCap.append( [ self.pumpingTS[i][0], self.unitCap[i][1] * self.noUnits[i][1] ] )
            
        HEC.setDssTsValues( self.outputDSS, self.maxPossibleCap, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPINGPLANT-CHARACTERISTICS/" % (self.facility, "MAX-CAPACITY")
                           , 0, "MW", "POWER" )

    #calculate energy
    def energyComputation(self):

        # EXCEL CALCULATION - Total Pumping Energy
        
        self.totalPumpingEnergy = list()

        for i in range(len(self.pumpingTS)):

            self.totalPumpingEnergy.append( [ self.pumpingTS[i][0],
                                              .001 * self.pumpingTS[i][1] *
                                              self.cfs2taf[self.pumpingTS[i][0]] *
                                              self.energyFactor[i][1] ] )
            
        HEC.setDssTsValues( self.outputDSS, self.totalPumpingEnergy, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-COMPUTATION/" % (self.facility, "TOTAL-PUMPING-ENERGY")
                           , 0, "GW-Hour", "ENERGY" )
                                            
        # EXCEL CALCULATION - Off-Peak Energy - Desired

        self.offPeakEnergyDesired = list()

        for i in range(len(self.totalPumpingEnergy)):

            self.offPeakEnergyDesired.append( [ self.totalPumpingEnergy[i][0],
                                                self.totalPumpingEnergy[i][1] * self.offPeakPercent[i][1] ] )
                                            
        HEC.setDssTsValues( self.outputDSS, self.offPeakEnergyDesired, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-COMPUTATION/" % (self.facility, "OFF-PEAK-ENERGY-DESIRED")
                           , 0, "GW-Hour", "ENERGY" )
        
        # EXCEL CALCULATION - Off-Peak Energy - Physical Max

        self.offPeakEnergyPhysicalMax = list()

        for p in self.maxPossibleCap:
            
            self.offPeakEnergyPhysicalMax.append( [ p[0],
                                                    0.001 *
                                                    p[1] *
                                                    float(peak.offPeakHours[ str( 1900 + p[0].getYear() + 0.01 * ( p[0].getMonth() + 1 ) ) ]) ] )
                                            
        HEC.setDssTsValues( self.outputDSS, self.offPeakEnergyPhysicalMax, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-COMPUTATION/" % (self.facility, "OFF-PEAK-ENERGY-PHYS-MAX")
                           , 0, "GW-Hour", "ENERGY" )

        # EXCEL CALCULATION - Off-Peak Energy - Actual

        self.offPeakEnergyActual = list()

        for i in range(len(self.noUnits)):

            if self.noUnits[i][1] < 0.5:
                self.offPeakEnergyActual.append( [ self.noUnits[i][0],
                                                   self.offPeakEnergyDesired[i][1] ] )
            else:
                self.offPeakEnergyActual.append( [ self.noUnits[i][0],
                                                   min( self.offPeakEnergyDesired[i][1], self.offPeakEnergyPhysicalMax[i][1] ) ] )
                                            
        HEC.setDssTsValues( self.outputDSS, self.offPeakEnergyActual, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-COMPUTATION/" % (self.facility, "OFF-PEAK-ENERGY-ACTUAL")
                           , 0, "GW-Hour", "ENERGY" )

        # EXCEL CALCULATION - Off-Peak Energy - Energy Check

        self.offPeakEnergyCheck = list()

        for i in range(len(self.offPeakEnergyDesired)):

            self.offPeakEnergyCheck.append( [ self.offPeakEnergyDesired[i][0],
                                              self.offPeakEnergyDesired[i][1] - self.offPeakEnergyActual[i][1] ] )
                                            
        HEC.setDssTsValues( self.outputDSS, self.offPeakEnergyCheck, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-COMPUTATION/" % (self.facility, "OFF-PEAK-ENERGY-CHECK")
                           , 0, "GW-Hour", "ENERGY" )

        # EXCEL CALCULATION - On-Peak Energy - Desired

        self.onPeakEnergyDesired = list()

        for i in range(len(self.totalPumpingEnergy)):

            self.onPeakEnergyDesired.append( [ self.totalPumpingEnergy[i][0],
                                               self.totalPumpingEnergy[i][1] - self.offPeakEnergyActual[i][1] ] )
                                            
        HEC.setDssTsValues( self.outputDSS, self.onPeakEnergyDesired, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-COMPUTATION/" % (self.facility, "ON-PEAK-ENERGY-DESIRED")
                           , 0, "GW-Hour", "ENERGY" )
        
        # EXCEL CALCULATION - On-Peak Energy - Physical Max

        self.onPeakEnergyPhysicalMax = list()

        for p in self.maxPossibleCap:
            
            self.onPeakEnergyPhysicalMax.append( [ p[0],
                                                    0.001 *
                                                    p[1] *
                                                    float(peak.onPeakHours[ str( 1900 + p[0].getYear() + 0.01 * ( p[0].getMonth() + 1 ) ) ]) ] )
                                            
        HEC.setDssTsValues( self.outputDSS, self.onPeakEnergyPhysicalMax, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-COMPUTATION/" % (self.facility, "ON-PEAK-ENERGY-PHYS-MAX")
                           , 0, "GW-Hour", "ENERGY" )

        # EXCEL CALCULATION - On-Peak Energy - Actual

        self.onPeakEnergyActual = list()

        for i in range(len(self.noUnits)):

            if self.noUnits[i][1] < 0.5:
                self.onPeakEnergyActual.append( [ self.noUnits[i][0],
                                                  self.onPeakEnergyDesired[i][1] ] )
            else:
                self.onPeakEnergyActual.append( [ self.noUnits[i][0], min( self.onPeakEnergyDesired[i][1],
                                                                           self.onPeakEnergyPhysicalMax[i][1] ) ] )
                                            
        HEC.setDssTsValues( self.outputDSS, self.onPeakEnergyActual, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-COMPUTATION/" % (self.facility, "ON-PEAK-ENERGY-ACTUAL")
                           , 0, "GW-Hour", "ENERGY" )

        # EXCEL CALCULATION - On-Peak Energy - Energy Check

        self.onPeakEnergyCheck = list()

        for i in range(len(self.onPeakEnergyDesired)):

            self.onPeakEnergyCheck.append( [ self.onPeakEnergyDesired[i][0], self.onPeakEnergyDesired[i][1] - self.onPeakEnergyActual[i][1] ] )
                                            
        HEC.setDssTsValues( self.outputDSS, self.onPeakEnergyCheck, self.start, "/HYDROPOWER/%s/%s//1MON/ENERGY-COMPUTATION/" % (self.facility, "On-PEAK-ENERGY-CHECK")
                           , 0, "GW-Hour", "ENERGY" )
                                
    #calculate capacity
    def computedCapacity(self):
        
        # EXCEL CALCULATION - Computed Capacity - Off-Peak Energy

        self.offPeakComputedCap = list()
        
        for i in range(len(self.offPeakEnergyActual)):

            if self.noUnits[i][1] < 0.5:

                self.offPeakComputedCap.append( [ self.offPeakEnergyActual[i][0],
                                                  1000.0 *
                                                  self.offPeakAdj[i][1] *
                                                  self.offPeakEnergyActual[i][1] /
                                                  float(peak.offPeakHours[ str( 1900 + self.offPeakEnergyActual[i][0].getYear() + 0.01 * ( self.offPeakEnergyActual[i][0].getMonth() + 1 ) ) ]) ] )
            elif (math.ceil(1000.0 *
                  self.offPeakEnergyActual[i][1] *
                  self.offPeakAdj[i][1] /
                  float(peak.offPeakHours[ str( 1900 + self.offPeakEnergyActual[i][0].getYear() + 0.01 * ( self.offPeakEnergyActual[i][0].getMonth() + 1 ) ) ]) >
                  self.maxPossibleCap[i][1])):

                self.offPeakComputedCap.append( [ self.offPeakEnergyActual[i][0], self.maxPossibleCap[i][1]] )

            else:

                self.offPeakComputedCap.append( [ self.offPeakEnergyActual[i][0],
                                                  math.ceil(
                                                      1000.0 *
                                                      self.offPeakEnergyActual[i][1] *
                                                      self.offPeakAdj[i][1] /
                                                      float(peak.offPeakHours[ str( 1900 + self.offPeakEnergyActual[i][0].getYear() + 0.01 * ( self.offPeakEnergyActual[i][0].getMonth() + 1 ) ) ]) /
                                                      self.unitCap[i][1]) *
                                                  self.unitCap[i][1] ] )
                
        HEC.setDssTsValues( self.outputDSS, self.offPeakComputedCap, self.start, "/HYDROPOWER/%s/%s//1MON/COMPUTED-CAPACITY/" % (self.facility, "OFF-PEAK-CAPACITY")
                           , 0, "MW", "POWER" )

        # EXCEL CALCULATION - Computed Capacity - On-Peak Energy

        self.onPeakComputedCap = list()
        
        for i in range(len(self.onPeakEnergyActual)):

            if self.noUnits[i][1] < 0.5:

                self.onPeakComputedCap.append( [ self.onPeakEnergyActual[i][0],
                                                  1000.0 *
                                                  self.onPeakAdj[i][1] *
                                                  self.onPeakEnergyActual[i][1] /
                                                  float(peak.onPeakHours[ str( 1900 + self.onPeakEnergyActual[i][0].getYear() + 0.01 * ( self.onPeakEnergyActual[i][0].getMonth() + 1 ) ) ]) ] )
            elif (math.ceil(1000.0 *
                  self.onPeakEnergyActual[i][1] *
                  self.onPeakAdj[i][1] /
                  float(peak.onPeakHours[ str( 1900 + self.onPeakEnergyActual[i][0].getYear() + 0.01 * ( self.onPeakEnergyActual[i][0].getMonth() + 1 ) ) ]) >
                  self.maxPossibleCap[i][1])):

                self.onPeakComputedCap.append( [ self.onPeakEnergyActual[i][0], self.maxPossibleCap[i][1]] )

            else:

                self.onPeakComputedCap.append( [ self.onPeakEnergyActual[i][0],
                                                  math.ceil(
                                                      1000.0 *
                                                      self.onPeakEnergyActual[i][1] *
                                                      self.onPeakAdj[i][1] /
                                                      float(peak.onPeakHours[ str( 1900 + self.onPeakEnergyActual[i][0].getYear() + 0.01 * ( self.onPeakEnergyActual[i][0].getMonth() + 1 ) ) ]) /
                                                      self.unitCap[i][1]) *
                                                  self.unitCap[i][1] ] )
                
        HEC.setDssTsValues( self.outputDSS, self.onPeakComputedCap, self.start, "/HYDROPOWER/%s/%s//1MON/COMPUTED-CAPACITY/" % (self.facility, "ON-PEAK-CAPACITY")
                           , 0, "MW", "POWER" )        
        
    #calculate actual pumping energy use at load center
    def pumpingEnergyAtLC(self):

        # EXCEL CALCULATION - Actual Pumping Use at Load Center - Transmission Loss

        self.transmissionLoss = list()

        for q in self.pumpingTS:

            self.transmissionLoss.append( [ q[0],
                                            float(self.characteristics.transmissionLoss[ self.months[ q[0].getMonth() ] ] ) ] )

        HEC.setDssTsValues( self.outputDSS, self.transmissionLoss, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPING-AT-LC/" % (self.facility, "PERCENT-LOSS")
                           , 0, "PERCENT", "LOSS" )
        
        # EXCEL CALCULATION - Actual Pumping Use at Load Center - Total Energy

        self.totalEnergy = list()

        for i in range(len(self.totalPumpingEnergy)):

            self.totalEnergy.append( [ self.totalPumpingEnergy[i][0],
                                       self.totalPumpingEnergy[i][1] *
                                       (1.0 + self.transmissionLoss[i][1]) ] )
            
        HEC.setDssTsValues( self.outputDSS, self.totalEnergy, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPING-AT-LC/" % (self.facility, "TOTAL-PUMPING-ENERGY")
                           , 0, "GW-Hour", "ENERGY" )

        # EXCEL CALCULATION - Actual Pumping Use at Load Center - Off Peak Energy

        self.offPeakEnergy = list()
        offPeakCost = list()
        
        for i in range(len(self.offPeakEnergyActual)):

            self.offPeakEnergy.append( [ self.offPeakEnergyActual[i][0],
                                       self.offPeakEnergyActual[i][1] * (1.0 + self.transmissionLoss[i][1]) ] )

            offPeakCost.append( [ self.offPeakEnergyActual[i][0], self.offPeakEnergy[i][1] * float(a.offPeak[ str(self.offPeakEnergyActual[i][0].getMonth() + 1) ]) ] )
               
        HEC.setDssTsValues( self.outputDSS, self.offPeakEnergy, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPING-AT-LC/" % (self.facility, "OFF-PEAK-TOTAL-PUMPING-ENERGY")
                           , 0, "GW-Hour", "ENERGY" )
        
        #HEC.setDssTsValues (self.outputDSS, offPeakCost , self.start, "/HYDROPOWER/%s/%s//1MON/ECONOMICS/" % (self.facility, "OFF-PEAK-COST"), 0, "$1,000", "COST")
        
        # EXCEL CALCULATION - Actual Pumping Use at Load Center - On Peak Energy

        self.onPeakEnergy = list()
        onPeakCost = list()

        for i in range(len(self.onPeakEnergyActual)):

            self.onPeakEnergy.append( [ self.onPeakEnergyActual[i][0],
                                       self.onPeakEnergyActual[i][1] *
                                        (1.0 + self.transmissionLoss[i][1]) ] )
            
            onPeakCost.append( [ self.pumpingTS[i][0], self.onPeakEnergyActual[i][1] *
                                 (1.0 + self.transmissionLoss[i][1]) *
                                 float(a.onPeak[ str(self.pumpingTS[i][0].getMonth() + 1) ]) ] )
            
        HEC.setDssTsValues( self.outputDSS, self.onPeakEnergy, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPING-AT-LC/" % (self.facility, "ON-PEAK-TOTAL-PUMPING-ENERGY")
                           , 0, "GW-Hour", "ENERGY" )

        HEC.setDssTsValues (self.outputDSS, onPeakCost , self.start, "/HYDROPOWER/%s/%s//1MON/ECONOMICS/" % (self.facility, "ON-PEAK-COST"), 0, "$1,000", "COST")

        # EXCEL CALCULATION - Actual Pumping Use at Load Center - Losses

        self.losses = list()

        for i in range(len(self.totalPumpingEnergy)):

            self.losses.append( [ self.totalPumpingEnergy[i][0],
                                       self.totalEnergy[i][1] - self.totalPumpingEnergy[i][1] ] )
            
        HEC.setDssTsValues( self.outputDSS, self.losses, self.start, "/HYDROPOWER/%s/%s//1MON/PUMPING-AT-LC/" % (self.facility, "LOSSES")
                           , 0, "GW-Hour", "LOSS" )
        
    #calculate capacity at load center
    def capacityAtLC(self):

        # EXCEL CALCULATION - Capacity at Load Center - Off Peak

        self.offPeakCapAtLC = list()

        for i in range(len(self.offPeakComputedCap)):

            self.offPeakCapAtLC.append( [ self.offPeakComputedCap[i][0],
                                          self.offPeakComputedCap[i][1] *
                                          (1.0 + self.transmissionLoss[i][1]) ] )
            
        HEC.setDssTsValues( self.outputDSS, self.offPeakCapAtLC, self.start, "/HYDROPOWER/%s/%s//1MON/CAPACITY-AT-LC/" % (self.facility, "OFF-PEAK-CAPACITY")
                           , 0, "MW", "POWER" )        

        # EXCEL CALCULATION - Capacity at Load Center - Off Peak

        self.onPeakCapAtLC = list()

        for i in range(len(self.onPeakComputedCap)):

            self.onPeakCapAtLC.append( [ self.onPeakComputedCap[i][0],
                                          self.onPeakComputedCap[i][1] *
                                         (1.0 + self.transmissionLoss[i][1]) ] )
            
        HEC.setDssTsValues( self.outputDSS, self.onPeakCapAtLC, self.start, "/HYDROPOWER/%s/%s//1MON/CAPACITY-AT-LC/" % (self.facility, "ON-PEAK-CAPACITY")
                           , 0, "MW", "POWER" )
