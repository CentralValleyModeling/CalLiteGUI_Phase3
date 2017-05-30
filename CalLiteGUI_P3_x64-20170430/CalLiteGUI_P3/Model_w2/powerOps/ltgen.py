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
import sys

# dvFile = sys.argv[1] # Gets file name as the first parameter from command line
dvFile = "../../Scenarios/DCR2015_Base_ExistingNoCC_DV.dss" 
outputDSS = os.path.basename(dvFile).split('.')[0] + "_LtGen.dss"
start = "31OCT1921 2400"
end = "30SEP2003 2400"
fPart = "2020D09E"
aPart = "CALSIM"

outputDSS = HEC.openDSS(outputDSS)

##########___POWER PLANTS___##########

CVPPowerFacilities = dict()
for fl in glob.glob("./tables/CVPFacilities/*PP.in"):
    CVPPowerFacilities[ os.path.basename(fl).split(".in")[0] ] = characteristics(fl)

trinity = powerPlant(
    facility = "trinityPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S1/STORAGE//1MON/%s/" % ( aPart, fPart ),
    release = "/%s/C1/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = Trinity_El,
    tailRace = Trinity_TR,
    energyFactor = Trinity_EF,
    unitCap = Trinity_MW_Peak,
    characteristics = CVPPowerFacilities[ "trinityPP" ],
    )

carr = powerPlant(
    facility = "carrPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S3/STORAGE//1MON/%s/" % ( aPart, fPart ),
    release = "/%s/D100/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = [Lewiston_El, Whiskeytown_El],
    energyFactor = JFCarr_EF,
    unitCap = JFCarr_MW_Peak,
    characteristics = CVPPowerFacilities[ "carrPP" ],
    )

springCreek = powerPlant(
    facility = "springCreekPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = ["/%s/S3/STORAGE//1MON/%s/" % ( aPart, fPart ),
               "/%s/S5/STORAGE//1MON/%s/" % ( aPart, fPart )],
    release = "/%s/D3/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = [Whiskeytown_El, Keswick_El],
    energyFactor = Spring_Creek_EF,
    unitCap = Spring_Creek_MW_Peak,
    characteristics = CVPPowerFacilities[ "springCreekPP" ],
    )

shasta = powerPlant(
    facility = "shastaPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S4/STORAGE//1MON/%s/" % ( aPart, fPart ),
    release = "/%s/C4/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = Shasta_El,
    tailRace = Shasta_TR,
    energyFactor = Shasta_EF,
    unitCap = Shasta_MW_Peak,
    characteristics = CVPPowerFacilities[ "shastaPP" ],
    )

keswick = powerPlant(
    facility = "keswickPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S5/STORAGE//1MON/%s/" % ( aPart, fPart ),
    release = "/%s/C5/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = Keswick_El,
    tailRace = Keswick_TR,
    energyFactor = Keswick_EF,
    unitCap = Keswick_MW_Peak,
    characteristics = CVPPowerFacilities[ "keswickPP" ],
    availCap = Keswick_MW_Flow,
    )

folsom = powerPlant(
    facility = "folsomPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S8/STORAGE//1MON/%s/" % ( aPart, fPart ),
    release = "/%s/C8/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = Folsom_El,
    tailRace = Folsom_TR,
    energyFactor = Folsom_EF,
    unitCap = Folsom_MW_Peak,
    characteristics = CVPPowerFacilities[ "folsomPP" ],
    )

nimbus = powerPlant(
    facility = "nimbusPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S9/STORAGE//1MON/%s/" % ( aPart, fPart ),
    release = "/%s/C9/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = Natoma_El,
    tailRace = Nimbus_TR,
    energyFactor = Nimbus_EF,
    unitCap = Nimbus_MW_Peak,
    characteristics = CVPPowerFacilities[ "nimbusPP" ],
    availCap = Nimbus_MW_Flow,
    )

newMelones = powerPlant(
    facility = "newMelonesPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S10/STORAGE//1MON/%s/" % ( aPart, fPart ),
    release = "/%s/C10/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = New_Melones_El,
    tailRace = New_Melones_TR,
    energyFactor = New_Melones_EF,
    unitCap = New_Melones_MW_Peak,
    characteristics = CVPPowerFacilities[ "newMelonesPP" ],
    )

cvpSanLuis = powerPlant(
    facility = "cvpSanLuisPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = ["/%s/S11/STORAGE//1MON/%s/" % ( aPart, fPart ),
               "/%s/S12/STORAGE//1MON/%s/" % ( aPart, fPart ),
               "/%s/S13/STORAGE//1MON/%s/" % ( aPart, fPart ),], 
    release = "/%s/C11/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    flowIn = "/%s/D703/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    elevation = San_Luis_El,
    energyFactor = San_Luis_Gen_EF,
    unitCap = San_Luis_Gen_MW,
    characteristics = CVPPowerFacilities[ "cvpSanLuisPP" ],
    )

oNeilPP = powerPlant(
    facility = "oNeilPP",
    dv = dvFile,
    outputDSS = outputDSS,
    release = "/%s/C705/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    flowIn = "/%s/C702/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    energyFactor = ONiell_EF,
    availCap = ONeill_MW_Flow,
    characteristics = CVPPowerFacilities[ "oNeilPP" ],
    )

##########___END POWER PLANTS___##########

##########___PUMPING PLANTS___##########

CVPPumpFacilities = dict()

for fl in glob.glob("./tables/CVPFacilities/*Pump.in"):
    CVPPumpFacilities[ os.path.basename(fl).split(".in")[0] ] = characteristics(fl)

tracyPump = pumpPlant(
    facility = "tracyPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D418/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "tracyPump" ],
    )

cvpBanksPump = pumpPlant(
    facility = "cvpBanksPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D419_CVP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "cvpBanksPump" ],
    )

cvpBanksPump = pumpPlant(
    facility = "cvpBanksPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D419_CVP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "cvpBanksPump" ],
    )

contraCostaPump = pumpPlant(
    facility = "contraCostaPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = ["/%s/D408/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
               "/%s/D416/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),],
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "contraCostaPump" ],
    )

oNeillPump = pumpPlant(
    facility = "oNeillPump",
    dv = dvFile,
    outputDSS = outputDSS,
    volIn = "/%s/C702/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    volOut = "/%s/C705/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ), 
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "oNeillPump" ],
    )

cvpSanLuisPump = pumpPlant(
    facility = "cvpSanLuisPump",
    dv = dvFile,
    outputDSS = outputDSS,
    volIn = "/%s/D703/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    volOut = "/%s/C11/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ), 
    start = start,
    end = end,
    energyFactor = San_Luis_Pump_EF,
    unitCap = San_Luis_Pump_MW,
    characteristics = CVPPumpFacilities[ "cvpSanLuisPump" ],
    )

sanFelipePump = pumpPlant(
    facility = "sanFelipePump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D11/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    energyFactor = San_Felipe_EF,
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "sanFelipePump" ],
    )

cvpDosAmigosPump = pumpPlant(
    facility = "cvpDosAmigosPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = ["/%s/C834/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
               "/%s/D419_CVC/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),],
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "cvpDosAmigosPump" ],
    )

folsomPump = pumpPlant(
    facility = "folsomPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D8/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    energyFactor = Folsom_PP_EF,
    characteristics = CVPPumpFacilities[ "folsomPump" ],
    )

corningPump = pumpPlant(
    facility = "corningPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D171/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "corningPump" ],
    )

redBluffPump = pumpPlant(
    facility = "redBluffPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = ["/%s/D171/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),
               "/%s/C171/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),],
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "redBluffPump" ],
    )

dmcIntertiePump = pumpPlant(
    facility = "dmcIntertiePump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C700A/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "dmcIntertiePump" ],
    )

sanLuisOtherPump = pumpPlant(
    facility = "sanLuisOtherPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C832/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "sanLuisOtherPump" ],
    )

dmcOtherPump = pumpPlant(
    facility = "dmcOtherPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C705/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "dmcOtherPump" ],
    )

tcOtherPump = pumpPlant(
    facility = "tcOtherPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C171/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "tcOtherPump" ],
    )

##########___END___##########
outputDSS.close()
