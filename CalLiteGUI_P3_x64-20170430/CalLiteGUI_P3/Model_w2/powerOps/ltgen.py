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
import sys 						#Taraky, DWR, 2017/06/05

dvFile = sys.argv[1] 			#Gets file name as the first parameter from command line, Taraky, DWR, 2017/06/05 
#dvFile = "../../Scenarios/DEFAULT_PowerCalculation2_DV.dss" 					#Commented out when DV file name can be passed as an argument, Taraky, DWR, 2017/06/05 
outputDSS = os.path.basename(dvFile).split('.')[0] + "_LtGen.dss"
start = "31OCT1921 2400"		# May need to pass start time, Taraky, DWR, 2017/06/05 
end = "30SEP2003 2400"			# May need to pass end time, Taraky, DWR, 2017/06/05
fPart = "2020D09E"				# May need to pass fPart, Taraky, DWR, 2017/06/05
aPart = "CALLITE"				# May need to pass aPart, Taraky, DWR, 2017/06/05

outputDSS = HEC.openDSS(outputDSS)

##########___POWER PLANTS___##########

CVPPowerFacilities = dict()
for fl in glob.glob("./tables/CVPFacilities/*PP.in"):
    CVPPowerFacilities[ os.path.basename(fl).split(".in")[0] ] = characteristics(fl)

trinity = powerPlant(
    facility = "trinityPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S_Trnty/STORAGE//1MON/%s/" % ( aPart, fPart ), 				#changed from S1, Taraky, DWR, 2017/06/05 
    release = "/%s/C_Trnty/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ), 			#changes from C1, Taraky, DWR, 2017/06/05
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
    storage = "/%s/S_Wkytn/STORAGE//1MON/%s/" % ( aPart, fPart ), 				#changed from S3, Taraky, DWR, 2017/06/05
    release = "/%s/D_ClearTu/FLOW-TUNNEL//1MON/%s/" % ( aPart, fPart ), 		#changed from D100, changed from FLOW-DELIVERY to FLOW-TUNNEL, Taraky, DWR, 2017/06/05
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
    storage = ["/%s/S_Wkytn/STORAGE//1MON/%s/" % ( aPart, fPart ), 				#changed from S3, Taraky, DWR, 2017/06/05
               "/%s/S_Kswck/STORAGE//1MON/%s/" % ( aPart, fPart )],				#changed from S5, mapped in CalLite (delta_S_Kswck = - AD_Kswck_Actual - E_Kswck), Taraky, DWR, 2017/06/05
    release = "/%s/D_Spring/FLOW-TUNNEL//1MON/%s/" % ( aPart, fPart ), 			#changed from D3, changed from FLOW-DELIVERY to FLOW-TUNNEL, Taraky, DWR, 2017/06/05
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
    storage = "/%s/S_Shsta/STORAGE//1MON/%s/" % ( aPart, fPart ), 				#changed from S4, Taraky, DWR, 2017/06/05
    release = "/%s/C_Shsta/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C4, Taraky, DWR, 2017/06/05
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
    storage = "/%s/S_Kswck/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S5, mapped in CalLite (delta_S_Kswck = - AD_Kswck_Actual - E_Kswck), Taraky, DWR, 2017/06/05
    release = "/%s/C_Kswck/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C5, Taraky, DWR, 2017/06/05
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
    storage = "/%s/S_Folsm/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S8, Taraky, DWR, 2017/06/05
    release = "/%s/C_Folsm/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C8, Taraky, DWR, 2017/06/05
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
    storage = "/%s/S_Nimbus/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S9, mapped in CalLite (delta_S_Nimbus = - AD_Nimbus_Actual + I_Nimbus_S2D - E_Nimbus), Taraky, DWR, 2017/06/05
    release = "/%s/C_Nimbus/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C9, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    elevation = Natoma_El,
    tailRace = Nimbus_TR,
    energyFactor = Nimbus_EF,
    unitCap = Nimbus_MW_Peak,
    characteristics = CVPPowerFacilities[ "nimbusPP" ],
    availCap = Nimbus_MW_Flow,
    )
# Data available only when dynamic SJR is turned on
# newMelones = powerPlant(
    # facility = "newMelonesPP",
    # dv = dvFile,
    # outputDSS = outputDSS,
    # storage = "/%s/S_Melon/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S10, Taraky, DWR, 2017/06/05
    # release = "/%s/C_Melon/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#changed from C10, Taraky, DWR, 2017/06/05
    # start = start,
    # end = end,
    # elevation = New_Melones_El,
    # tailRace = New_Melones_TR,
    # energyFactor = New_Melones_EF,
    # unitCap = New_Melones_MW_Peak,
    # characteristics = CVPPowerFacilities[ "newMelonesPP" ],
    # )

cvpSanLuis = powerPlant(
    facility = "cvpSanLuisPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = ["/%s/S_SLCVP/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S11, Taraky, DWR, 2017/06/05
               "/%s/S_SLSWP/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S12, Taraky, DWR, 2017/06/05
               "/%s/S_SLEWA/STORAGE//1MON/%s/" % ( aPart, fPart ),],			#changed from S13, need to map in CalLite, created temporary dummy variable in DV.dss file, Taraky, DWR, 2017/06/05
    release = "/%s/C_SLCVP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C11, Taraky, DWR, 2017/06/05
    flowIn = "/%s/D_OFBCVP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#changed from D703, Taraky, DWR, 2017/06/05
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
    release = "/%s/D_CVPJU_LDMC/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),	#changed from C705, changed from FLOW-CHANNEL to FLOW-DELIVERY, Taraky, DWR, 2017/06/05
    flowIn = "/%s/C_UpDMC/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C702, Taraky, DWR, 2017/06/05
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
    pumping = "/%s/D_Jones/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#changed from D418, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "tracyPump" ],
    )

cvpBanksPump = pumpPlant(
    facility = "cvpBanksPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D_Banks_CVP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),		#changed from D419_CVP, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "cvpBanksPump" ],
    )

cvpBanksPump = pumpPlant(
    facility = "cvpBanksPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D_Banks_CVP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),		#changed from D419_CVP *** Why call same facility twice?***, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "cvpBanksPump" ],
    )

contraCostaPump = pumpPlant(
    facility = "contraCostaPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = ["/%s/D_CCWDVCOR/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),		#changed from D408, Taraky, DWR, 2017/06/05
               "/%s/D_CCWDINTK/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),],	#changed from D416, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "contraCostaPump" ],
    )

oNeillPump = pumpPlant(
    facility = "oNeillPump",
    dv = dvFile,
    outputDSS = outputDSS,
    volIn = "/%s/C_UpDMC/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C702, Taraky, DWR, 2017/06/05
    volOut = "/%s/D_CVPJU_LDMC/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),		#changed from C705, Changed from FLOW-CHANNEL to FLOW-DELIVERY, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "oNeillPump" ],
    )

cvpSanLuisPump = pumpPlant(
    facility = "cvpSanLuisPump",
    dv = dvFile,
    outputDSS = outputDSS,
    volIn = "/%s/D_OFBCVP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#changed from D703, Taraky, DWR, 2017/06/05
    volOut = "/%s/C_SLCVP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C11, Taraky, DWR, 2017/06/05
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
    pumping = "/%s/D_SLCVP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#changed from D11, Taraky, DWR, 2017/06/05
    energyFactor = San_Felipe_EF,
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "sanFelipePump" ],
    )

cvpDosAmigosPump = pumpPlant(
    facility = "cvpDosAmigosPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = ["/%s/C834/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#California Aqueduct Joint-use from CVP contractors (Dos Amigos Pumping Plant), mapped in CalLite(C834 = C_CVPJU-D833-D834), Taraky, DWR, 2017/06/05
               "/%s/D_Banks_CVC/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),], 	#changed from D419_CVC, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "cvpDosAmigosPump" ],
    )

folsomPump = pumpPlant(
    facility = "folsomPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D_Folsm/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#changed from D8, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    energyFactor = Folsom_PP_EF,
    characteristics = CVPPumpFacilities[ "folsomPump" ],
    )

corningPump = pumpPlant(
    facility = "corningPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D171/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#no change needed, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "corningPump" ],
    )

redBluffPump = pumpPlant(
    facility = "redBluffPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = ["/%s/D171/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#no change needed, Taraky, DWR, 2017/06/05
               "/%s/C_TCCnl/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),],		#Tehama-Colusa Relift and Red Bluff Pumping Plant, mapped in CalLite (C_TCCnl = D112-D171), Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "redBluffPump" ],
    )

dmcIntertiePump = pumpPlant(
    facility = "dmcIntertiePump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_Intrti/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C700A, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "dmcIntertiePump" ],
    )

sanLuisOtherPump = pumpPlant(
    facility = "sanLuisOtherPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_CVPJU/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#Changed from C832, San Luis Relift Pumping plant, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "sanLuisOtherPump" ],
    )

dmcOtherPump = pumpPlant(
    facility = "dmcOtherPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D_CVPJU_LDMC/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),	#changed from C705, changed from FLOW-CHANNEL to FLOW-DELIVERY, Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "dmcOtherPump" ],
    )

tcOtherPump = pumpPlant(
    facility = "tcOtherPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_TCCnl/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			# mapped in CalLite from CalSim (C_TCCnl = D112 - D171), Taraky, DWR, 2017/06/05
    start = start,
    end = end,
    characteristics = CVPPumpFacilities[ "tcOtherPump" ],
    )

##########___END PUMPING PLANTS___##########
outputDSS.close()
