#################
# Author: Patrick Ho, MBK Engineers
# Date: June 23, 2015
# Description: Implementing LTGen and SWPGen calculations in Jython
#################

from powerPlant import powerPlant
from pumpPlant import pumpPlant
from ratings import *
import HEC
import glob
import os

dvFile = "../../Scenarios/DCR2015_Base_ExistingNoCC_DV.dss"
outputDSS = os.path.basename(dvFile).split('.')[0] + "_SWPGen.dss"
start = "31OCT1921 2400"
end = "30SEP2003 2400"
fPart = "2020D09E"
aPart = "CALSIM"

##########___POWER PLANTS___##########

SWPFacilities = dict()
outputDSS = HEC.openDSS(outputDSS)

for fl in glob.glob("./tables/SWPFacilities/*.in"):
    SWPFacilities[ os.path.basename(fl).split(".in")[0] ] = characteristics(fl)

oroville = powerPlant(
    facility = "orovillePP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = ["/%s/S6/STORAGE//1MON/%s/" % ( aPart, fPart ),
               "/%s/S7/STORAGE//1MON/%s/" % ( aPart, fPart )],
    release = "/%s/C6/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = Oroville_El,
    tailRace = Thermalito_El,
    energyFactor = Hyatt_EF,
    availCap = Power_Calc,
    characteristics = SWPFacilities[ "orovillePP" ],
    )

thermalito = powerPlant(
    facility = "thermalitoPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S7/STORAGE//1MON/%s/" % ( aPart, fPart ),
    release = "/%s/C200A+C7/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = Thermalito_El,
    tailRace = ThermAB_El,
    energyFactor = Thermalito_EF,
    availCap = Power_Calc,
    characteristics = SWPFacilities[ "thermalitoPP" ],
    )

swpSanLuis = powerPlant(
    facility = "swpSanLuisPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = ["/%s/S11/STORAGE//1MON/%s/" % ( aPart, fPart ),
               "/%s/S12/STORAGE//1MON/%s/" % ( aPart, fPart ),
               "/%s/S13/STORAGE//1MON/%s/" % ( aPart, fPart ),],
    release = "/%s/C12/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    flowIn = "/%s/D805/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = San_Luis_El,
    energyFactor = San_Luis_Gen_EF,
    unitCap = San_Luis_Gen_MW,
    characteristics = SWPFacilities[ "swpSanLuisPP" ],
    )

alamoPP = powerPlant(
    facility = "alamoPP",
    dv = dvFile,
    outputDSS = outputDSS,
    release = "/%s/C876/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    availCap = Power_Calc,
    characteristics = SWPFacilities[ "alamoPP" ],
    )

mojavePP = powerPlant(
    facility = "mojavePP",
    dv = dvFile,
    outputDSS = outputDSS,
    release = "/%s/C882/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    availCap = Power_Calc,
    characteristics = SWPFacilities[ "mojavePP" ],
    )

devilCanyonPP = powerPlant(
    facility = "devilCanyonPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S25/STORAGE//1MON/%s/" % ( aPart, fPart ), 
    release = "/%s/C25/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = DCanyon_El,
    tailRace = DCanyon_TR,
    availCap = Power_Calc,
    characteristics = SWPFacilities[ "devilCanyonPP" ],
    )

warnePP = powerPlant(
    facility = "warnePP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = ["/%s/S28/STORAGE//1MON/%s/" % ( aPart, fPart ),
               "/%s/S28/STORAGE//1MON/%s/" % ( aPart, fPart )],
    release = "/%s/C892/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    tailRace = Pyramid_El,
    availCap = Power_Calc,
    characteristics = SWPFacilities[ "warnePP" ],
    )

castaicPP = powerPlant(
    facility = "castaicPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = ["/%s/S28/STORAGE//1MON/%s/" % ( aPart, fPart ),
               "/%s/S29/STORAGE//1MON/%s/" % ( aPart, fPart )],
    release = "/%s/C893/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = Pyramid_El,
    energyFactor = Castaic_EF,
    tailRace = Castaic_El,
    availCap = Power_Calc,
    characteristics = SWPFacilities[ "castaicPP" ],
    )
##########___END POWER PLANTS___##########

##########___PUMPING PLANTS___##########
SWPPumpFacilities = dict()

for fl in glob.glob("./tables/SWPFacilities/*Pump.in"):
    SWPPumpFacilities[ os.path.basename(fl).split(".in")[0] ] = characteristics(fl)

banksPump = pumpPlant(
    facility = "banksPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D419_SWP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "banksPump" ],
    )

swpSanLuisPump = pumpPlant(
    facility = "swpSanLuisPump",
    dv = dvFile,
    outputDSS = outputDSS,
    volIn = "/%s/D805/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    volOut = "/%s/C12/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ), 
    start = start,
    end = end,
    energyFactor = San_Luis_Pump_EF,
    unitCap = San_Luis_Pump_MW,
    characteristics = SWPPumpFacilities[ "swpSanLuisPump" ],
    )

swpDosAmigosPump = pumpPlant(
    facility = "swpDosAmigosPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C825/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "swpDosAmigosPump" ],
    )

buenaVistaPump = pumpPlant(
    facility = "buenaVistaPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C860/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "buenaVistaPump" ],
    )

teerinkPump = pumpPlant(
    facility = "teerinkPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C862/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "teerinkPump" ],
    )

chrismanPump = pumpPlant(
    facility = "chrismanPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C864/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "chrismanPump" ],
    )

edmonstonPump = pumpPlant(
    facility = "edmonstonPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C865/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "edmonstonPump" ],
    )

pearblossomPump = pumpPlant(
    facility = "pearblossomPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C880/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "pearblossomPump" ],
    )

buenaVistaPump = pumpPlant(
    facility = "buenaVistaPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C860/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "buenaVistaPump" ],
    )

osoPump = pumpPlant(
    facility = "osoPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C890/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "osoPump" ],
    )

southBayPump = pumpPlant(
    facility = "southBayPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D801/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "southBayPump" ],
    )

delVallePump = pumpPlant(
    facility = "delVallePump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D811/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "delVallePump" ],
    )

lasPerillasPump = pumpPlant(
    facility = "lasPerillasPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D850/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "lasPerillasPump" ],
    )

badgerHillPump = pumpPlant(
    facility = "badgerHillPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C866/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "badgerHillPump" ],
    )


##########___END___##########
outputDSS.close()
