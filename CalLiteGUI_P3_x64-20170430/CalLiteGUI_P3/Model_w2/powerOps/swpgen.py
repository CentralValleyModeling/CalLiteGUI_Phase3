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
outputDSS = os.path.basename(dvFile).split('.')[0] + "_SWPGen.dss"
start = "31OCT1921 2400"		# May need to pass start time as an argument, Taraky, DWR, 2017/06/05 
end = "30SEP2003 2400"			# May need to pass end time as an argument, Taraky, DWR, 2017/06/05
fPart = "2020D09E"				# May need to pass fPart as an argument, Taraky, DWR, 2017/06/05
aPart = "CALLITE"				# May need to pass aPart as an argument, Taraky, DWR, 2017/06/05

##########___POWER PLANTS___##########

SWPFacilities = dict()
outputDSS = HEC.openDSS(outputDSS)

for fl in glob.glob("./tables/SWPFacilities/*.in"):
    SWPFacilities[ os.path.basename(fl).split(".in")[0] ] = characteristics(fl)

oroville = powerPlant(
    facility = "orovillePP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = ["/%s/S_Orovl/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S6    
               "/%s/S_Therm/STORAGE//1MON/%s/" % ( aPart, fPart )],				#changed from S7, mapped in CalLite (delta_S_Therm = - AD_Therm_Actual - E_Nimbus + I_KellyRidge_S2D)
    release = "/%s/C_Orovl/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C6
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
    storage = "/%s/S_Therm/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S7
    release = "/%s/C_Therm/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#Changed from C200A+C7A, Thermalito Generation at Diversion Dam and Forebay, mapped in CalLite, (C_Therm = C203 = C7 + C_200A)
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
    storage = ["/%s/S_SLCVP/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S11
               "/%s/S_SLSWP/STORAGE//1MON/%s/" % ( aPart, fPart ),				#changed from S12
               "/%s/S_SLEWA/STORAGE//1MON/%s/" % ( aPart, fPart ),],			#changed from S13, need to map in CalLite, created temporary dummy variable in DV.dss file
    release = "/%s/C_SLSWP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C12
    flowIn = "/%s/D_OFBSWP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#changed from D805
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
    release = "/%s/C_Alamo/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C876
    start = start,
    end = end,
    availCap = Power_Calc,
    characteristics = SWPFacilities[ "alamoPP" ],
    )

mojavePP = powerPlant(
    facility = "mojavePP",
    dv = dvFile,
    outputDSS = outputDSS,
    release = "/%s/C_MjvPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#Changed from C882, Mojave PP, mapped in CalLite (C_MjvPP = C_PearBlPP-D881_PRJ-D882_PRJ)
    start = start,
    end = end,
    availCap = Power_Calc,
    characteristics = SWPFacilities[ "mojavePP" ],
    )

devilCanyonPP = powerPlant(
    facility = "devilCanyonPP",
    dv = dvFile,
    outputDSS = outputDSS,
    storage = "/%s/S_Silverwood/STORAGE//1MON/%s/" % ( aPart, fPart ), 			#Changed from S25, mapped in CalLite (delta_S_Silverwood = D_Silverwood - I_Silverwood - E_Silverwood)
    release = "/%s/C_DvlCnynPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#Changed from C25, Devil Canyon PP, mapped in CalLite (C_DvlCnynPP = C_PearBlPP-D881_PRJ-D882_PRJ-D25_PRJ-D_Silverwood+I_Silverwood)
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
    storage = ["/%s/S_Pyramid/STORAGE//1MON/%s/" % ( aPart, fPart ),			#Changed from S28, mapped in CalLite (delta_S_Pyramid = D_Pyramid - I_Pyramid - E_Pyramid)
               "/%s/S_Pyramid/STORAGE//1MON/%s/" % ( aPart, fPart )],			#Changed from S28, mapped in CalLite (delta_S_Pyramid = D_Pyramid - I_Pyramid - E_Pyramid) **why call twice?**		
    release = "/%s/C_WarnePP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#changed from C892
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
    storage = ["/%s/S_Pyramid/STORAGE//1MON/%s/" % ( aPart, fPart ),			#Changed from S28, mapped in CalLite (delta_S_Pyramid = D_Pyramid - I_Pyramid - E_Pyramid)
               "/%s/S_Castaic/STORAGE//1MON/%s/" % ( aPart, fPart )],			#Changed from S29, mapped in CalLite (delta_S_Castaic = -AD_Castaic_S2D - E_Castaic) 
    release = "/%s/C_CastaicPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#Changed from C893, Castaic Lake PP, mapped in CalLite (C_CastaicPP = C_WarnePP-D28_PRJ-D893_PRJ-D_Pyramid+I_Pyramid)
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
    pumping = "/%s/D_Banks_SWP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),		#changed from D419_SWP
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "banksPump" ],
    )

swpSanLuisPump = pumpPlant(
    facility = "swpSanLuisPump",
    dv = dvFile,
    outputDSS = outputDSS,
    volIn = "/%s/D_OFBSWP/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#changed from D805
    volOut = "/%s/C_SLSWP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ), 			#changed from C12
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
    pumping = "/%s/C_DosAmigosPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),	#Changed from C825, SWP Dos Amigos on the CA Aquaduct, mapped in CalLite (C_DosAmigosPP = C_SWPJU+D_CVPJUSWP-D824_PRJ)
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "swpDosAmigosPump" ],
    )

buenaVistaPump = pumpPlant(
    facility = "buenaVistaPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_BnVstPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#Changed from C860, Buena Vista PP, mapped in CalLite (C_BnVstPP = C_CVC+I _Kern-D859_PRJ)
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "buenaVistaPump" ],
    )

teerinkPump = pumpPlant(
    facility = "teerinkPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_WhlrPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#Changed from C862, Wheeler Ridge PP, mapped in CalLite (C_WhlrPP = C_CVC+I _Kern-D859_PRJ-D862_PRJ)
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "teerinkPump" ],
    )

chrismanPump = pumpPlant(
    facility = "chrismanPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_ChrisPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#changed from C864
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "chrismanPump" ],
    )

edmonstonPump = pumpPlant(
    facility = "edmonstonPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_ChrisPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#changed from C865, (C865 = C684)
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "edmonstonPump" ],
    )

pearblossomPump = pumpPlant(
    facility = "pearblossomPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_PearBlPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#changed from C880
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "pearblossomPump" ],
    )

buenaVistaPump = pumpPlant(
    facility = "buenaVistaPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_BnVstPP/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#Changed from C860, Buena Vista PP, mapped in CalLite (C_BnVstPP = C_CVC+I _Kern_S2D-D859_PRJ)
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "buenaVistaPump" ],
    )

osoPump = pumpPlant(
    facility = "osoPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_Oso/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),			#changed from C890
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "osoPump" ],
    )

southBayPump = pumpPlant(
    facility = "southBayPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D_SBay/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),			#changed from D801
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "southBayPump" ],
    )

delVallePump = pumpPlant(
    facility = "delVallePump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D_DelValle/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),		#changed from D811
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "delVallePump" ],
    )

lasPerillasPump = pumpPlant(
    facility = "lasPerillasPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/C_CoastAqdct/FLOW-CHANNEL//1MON/%s/" % ( aPart, fPart ),		#changed from D850, Changed form FLOW-DELIVERY to FLOW-CHANNEL
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "lasPerillasPump" ],
    )

badgerHillPump = pumpPlant(
    facility = "badgerHillPump",
    dv = dvFile,
    outputDSS = outputDSS,
    pumping = "/%s/D_CoastAqdct/FLOW-DELIVERY//1MON/%s/" % ( aPart, fPart ),	#changed from C866, Changed form FLOW-CHANNEL to FLOW-DELIVERY 
    start = start,
    end = end,
    characteristics = SWPPumpFacilities[ "badgerHillPump" ],
    )


##########___END___##########
outputDSS.close()
