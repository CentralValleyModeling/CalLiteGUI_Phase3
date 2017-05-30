# Notes from LTGen Patrick Ho MBK Engineers
# VBA function signatures persists. Types were removed and adapted
# using Python's dynamic typing
#
# These functions derived from information provided by M. Bauer, USBR
# in spreadsheet Powerplant Performance.xls (dated 5/10/2000)
# Functions developed by J. Johannis WAPA 7/18/2000
# Spreadsheet JJPowerplant Performance.xls shows comparison to
# USBR Data (dated 7/18/2000)
# As of 7/18/2000 still need to add:
#   Lewiston Storage vs Elevation
#   San Luis Curves
# The power generation functions (Head vs. kWh/AF) were revised by
# K. Nguyen, USBR 8/28/2002 with concurrence by M. Bauer and J. Johannis.

import math, sys

######################_____CVP FACILITY RATINGS_____#######################

def Trinity_El(Storage):

    # Returns Elevation in feet above MSL
    # Input Storage in TAF
    return 2033.718037 * math.exp((math.pow((2.773304459 - math.log(Storage)), 2)) / 165.4575429)

def Trinity_TR():

    # Returns Elevation in feet above MSL

    # Trinity tailrace currently set to constant
    # 'Trinity_TR = 1902
    return 1901.5
    #Modified by K. Nguyen, 8/28/2002

def Trinity_MW_Peak( Trinity_El, Trinity_TR ):

    if Trinity_El > 2213:

        Gross_Head = Trinity_El - Trinity_TR
        # Set Maximum Unit MW for Trinity
        Max_MW = 70
        
        return min((-189.9875487 + 1.243092168 * (Gross_Head) - 0.001151612 * (math.pow(Gross_Head, 2))) / 2, Max_MW)
    
    else:
        
        return 0.0
            
def Trinity_MW_BEP(Trinity_El, Trinity_TR):
                
    Gross_Head = Trinity_El - Trinity_TR
    # 'Set Maximum Unit MW for Trinity
    Max_MW = 70

    return min( 0.746 / 1000 * math.pow(10, (-3.77151 + 5.23077 * math.log10(Gross_Head) - 0.74105 * math.pow((math.log10(Gross_Head)), 2))), Max_MW )

#Merged Trinity_EF_HH and Trinity_EF_LH as one function
#Patrick Ho, MBK Engineers June 23, 2015
def Trinity_EF(Trinity_El, Trinity_TailRace):
    
    if Trinity_El > 2213.0:
        
        if Trinity_El > 2262.0:
            return Trinity_EF_HH( Trinity_El, Trinity_TailRace )
        else:
            return Trinity_EF_LH( Trinity_El, Trinity_TailRace )
    else:
        return 0.0
            
def Trinity_EF_HH(Trinity_El, Trinity_tailRace):

    # 'Returns Unit energy in kWh/Acre-Foot
    # 'This is based on high head runner
    # 'for low head runner use Trinity_EF_LH
    
    Gross_Head = Trinity_El - Trinity_tailRace

    #Original Formula
    #'Trinity_EF_HH = _
    #    -68.9298143 + 1.06277887 * (Gross_Head) + 0.000021087245 * _
    #    (Gross_Head) ^ 2
    
    return (1.19285 * Gross_Head) - 142.1086
    #'Modified by K. Nguyen, 9/13/2005.
    
def Trinity_EF_LH(Trinity_El, Trinity_TailRace ):

    # 'Returns Unit energy in kWh/Acre-Foot

    # 'This is based on low head runner
    # 'for high head runner use Trinity_EF_HH

    Gross_Head = Trinity_El - Trinity_TailRace

    return (1.19285 * Gross_Head) - 142.1086
    # 'NOT modified due to lack of data in the 08/2001-07/2002 dataset.
    # 'K. Nguyen, 9/13/2005.

def cfs_to_taf_month( cfs ):
    # 'assumes 30 days in a month
    return 1.9835 * cfs / 1000 * 30
    
def Whiskeytown_El(Storage):

    # 'Returns Elevation in feet above MSL
    # 'Input Storage in TAF

    # Original formula
    #'Whiskeytown_El = _
    #    (1093.967028 * Exp(((9.096229215 - math.log(1000 * Storage)) ^ 2) / _
    #    107.7871294))
    
    return 1039.624244 + (2.831353418 * Storage) - (0.03127455856 * math.pow(Storage, 2)) + (0.0001983944167 * math.pow(Storage, 3)) - (6.057016849E-07 * math.pow(Storage, 4)) + (7.021250359E-10 * math.pow(Storage, 5))
    # 'Modified by K. Nguyen, 8/28/2002 based on data from CVO-400 Lotus Water
    # 'Forecast spreadsheet by L. Peterson.  Original formula found to be
    # 'inaccurate.
    
def Shasta_El( Storage ):

    # 'Returns Elevation in feet above MSL

    return 741.1794 + 0.0002158981 * (Storage * 1000) - 9.793506E-11 * math.pow((Storage * 1000), 2) + 3.10102324E-17 * math.pow((Storage * 1000), 3) - 5.20882377E-24 * math.pow((Storage * 1000), 4) + 3.50083E-31 * math.pow((Storage * 1000), 5)

def Shasta_TR( Release_CFS ):

    # 'Returns Elevation in feet above MSL
    return 1 / ((1.97908E-14 * math.pow((Release_CFS - 40479.9296), 2) + 0.00168))


def Shasta_EF( Shasta_El, Shasta_TR ):

    # 'Returns Unit energy in kWh/Acre-Foot
    
    Gross_Head = Shasta_El - Shasta_TR

    # Original formula
    #'Shasta_EF = _
    #    65.2494654 * Exp(((2.846180871 - math.log(Gross_Head)) ^ 2) _
    #    / 5.920809539)

    if Shasta_El > 840.0:
        return 1.045 * ((0.83522 * Gross_Head) + 30.5324)
    else:
        return 0.0
    # 'Modified by K. Nguyen, 9/13/2005.
   

def Shasta_MW_BEP(Shasta_El, Shasta_TR):
               
    Gross_Head = Shasta_El - Shasta_TR
    
    # 'Set Maximum Unit MW for Shasta
    Max_MW = 143
    
    return min( 0.746 / 1000 * math.pow(10, (-8.46805 + 8.91492 * math.log10(Gross_Head) - 1.426837 * math.pow((math.log10(Gross_Head)), 2))), Max_MW)
        

def Shasta_MW_Peak(Shasta_El, Shasta_TR):
               
    Gross_Head = Shasta_El - Shasta_TR
    
    'Set Maximum Unit MW for Shasta
    Max_MW = 143

    if Shasta_El > 840.0:
        return min( -68.432781 + 0.446895 * Gross_Head, Max_MW )
    else:
        return 0.0
                
def Keswick_El(Storage):

    # 'Returns Elevation in feet above MSL
    # 'Input Storage in TAF

    return 515.4274977 * math.exp((math.pow((5.879609639 - math.log(Storage * 1000)), 2)) / 135.499882)

def Keswick_TR(Release_CFS):

    # 'Returns Elevation in feet above MSL

    return 485.0156566 * math.exp((math.pow((6.36440004 - math.log(Release_CFS)), 2)) / 447.351268)

def Keswick_EF( Keswick_El, Keswick_TR ):
    
    # 'Returns Unit energy in kWh/Acre-Foot
    
    Gross_Head = Keswick_El - Keswick_TR

    # Original formula
    # 'Keswick_EF = -23.724055303 + 1.1635101018 * (Gross_Head) - 14.7
    
    return (0.70399 * Gross_Head) + 9.4772
    # 'Modified by K. Nguyen, 9/13/2005.
            
def Keswick_MW_BEP(Keswick_El, Keswick_TR ):
    
    # 'Set Maximum Unit MW for Keswick
    Max_MW = 35

    Gross_Head = Keswick_El - Keswick_TR

    return min( 0.746 / 1000 * math.pow(10, (-641.789 + 1389.554 * math.log10(Gross_Head) - 1121.95 * math.pow((math.log10(Gross_Head)), 2) + 402.766 * math.pow((math.log10(Gross_Head)), 3) - 54.1871 * math.pow((math.log10(Gross_Head)), 4))), Max_MW)
                        
def Keswick_MW_Peak(Keswick_El, Keswick_TR ):
    
    # 'Set Maximum Unit MW for Keswick
    Max_MW = 35

    Gross_Head = Keswick_El - Keswick_TR

    return min( 38.8356411 * math.exp((math.pow((4.768909376 - math.log(Gross_Head)), 2)) / -0.587567337), Max_MW )
                    
def Keswick_MW_Flow(Powerplant_Release_CFS, Keswick_EF, Keswick_Peak_MW, Units_Available ):

    # 'Returns total plant Megawatts (not unit)
        
    # 'Set Maximum MW for Keswick (ENTIRE PLANT)
    Max_MW = Units_Available * Keswick_Peak_MW

    # 'This formula will not be accurate for days not equal
    # 'to 24 hours (begin and end of Daylight Savings Time)

    return min( Powerplant_Release_CFS * 0.0000825 * Keswick_EF, Max_MW)
                    
def Folsom_El( Storage ):

    # 'Returns Elevation in feet above MSL
    return 245.9857615 * math.exp((math.pow((-0.586204748 - math.log(Storage)), 2)) / 87.5222842)

def Folsom_TR( Release_CFS ):

    # 'Returns Elevation in feet above MSL
    
    # 'If 0 Release, formula will bomb,
    # 'Arbitrarily set to 130 (JJ)
    
    if (Release_CFS < 0.00001):
        return 120.0
    else:
        return math.pow(10, (2.113508 - 0.035579 * math.log10(Release_CFS / 1000) + 0.04750301 * math.pow(math.log10(Release_CFS / 1000), 2)))

def Folsom_EF( Folsom_El, Folsom_TR ):

    # 'Returns Unit energy in kWh/Acre-Foot

    Gross_Head = Folsom_El - Folsom_TR

    # Original formula
    #'Folsom_EF = _
    #       105.5364316 * 1.00300427 ^ (Gross_Head)

    if Folsom_El > 331.0:
        return (0.92854 * Gross_Head) - 16.282
    else:
        return 0.0
    # 'Modified by K. Nguyen, 9/13/2005.

def Folsom_MW_BEP( Folsom_El, Folsom_TR ):
    
    Gross_Head = Folsom_El - Folsom_TR
    
    # 'Set Maximum Unit MW for Folsom
    Max_MW = 70

    return min ( 0.746 / 1000 * math.pow(10, (-57.644 + 72.016 * math.log10(Gross_Head) - 28.189 * math.pow((math.log10(Gross_Head)), 2) + 3.75149 * math.pow((math.log10(Gross_Head)), 3))) , Max_MW )
    
def Folsom_MW_Peak( Folsom_El,  Folsom_TR ):
              
    Gross_Head = Folsom_El - Folsom_TR
    
    # 'Set Maximum Unit MW for Folsom
    Max_MW = 70

    if Folsom_El > 331.0:
        return min((135.3493607 - 22262.13696 / (Gross_Head)), Max_MW)
    else:
        return 0.0
                
def Natoma_El( Storage ):

    # 'Returns Elevation in feet above MSL
    # 'Natoma is the lake behind Nimbus Dam

    # 'Input Storage in TAF

    Storage = Storage * 1000

    return 79.93400558 * math.exp((math.pow((2.89618066 - math.log(Storage)), 2)) / 85.35059107)


def Nimbus_TR( Release_CFS ):

    # 'Returns Elevation in feet above MSL

    return 81.48069123 + 0.000553075 * Release_CFS - 402.7422903 / Release_CFS

def Nimbus_EF( Natoma_El, Nimbus_TR ):
    
    # 'Returns Unit energy in kWh/Acre-Foot
    
    Gross_Head = Natoma_El - Nimbus_TR

    # Original Formula
    # 'Nimbus_EF = 0.772169467 + 0.764674945 * Gross_Head
    return (0.11191 * Gross_Head) + 29.8156
    # 'Modified by K. Nguyen, 9/13/2005.


def Nimbus_MW_BEP( Natoma_El, Nimbus_TR ):
    
    # 'Set Maximum Unit MW for Nimbus
    # 'Need to check this value
    Max_MW = 8

    Gross_Head = Natoma_El - Nimbus_TR

    return min( 0.746 / 1000 * math.pow(10, (0.657282 + 2.6831 * math.log10(Gross_Head) - 0.452155 * math.pow((math.log10(Gross_Head)), 2))), Max_MW)
                        
def Nimbus_MW_Peak( Natoma_El, Nimbus_TR ):

    # 'Set Maximum Unit MW for Nimbus
    # 'Need to check this value
    Max_MW = 8

    Gross_Head = Natoma_El - Nimbus_TR

    return min( (1 / (0.00053599 * math.pow(((Gross_Head) - 41.51103725), 2) + 0.124222776)), Max_MW)
                        

def Nimbus_MW_Flow(Powerplant_Release_CFS, Nimbus_EF, Nimbus_Peak_MW, Units_Available):

    # 'Returns total plant Megawatts (not unit)
    #'Same Formula as Keswick

    # 'Set Maximum MW for Nimbus (ENTIRE PLANT)
    Max_MW = Units_Available * Nimbus_Peak_MW

    # 'This formula will not be accurate for days not equal
    # 'to 24 hours (begin and end of Daylight Savings Time)

    return min ( Powerplant_Release_CFS * 0.0000825 * Nimbus_EF, Max_MW )
                   

def New_Melones_El( Storage ):

    # 'Returns Elevation in feet above MSL

    return 681.39045407 * math.exp((math.pow((2.518594889 - math.log(Storage)), 2)) / 59.38930509)

def New_Melones_TR( Release_CFS ):

    # 'Returns Elevation in feet above MSL

    return 498 + (1 / (6.4599389E-11 * math.pow((Release_CFS - 63433.09636), 2) - 0.06036419))

def New_Melones_EF( New_Melones_El, New_Melones_TR ):

    # 'Returns Unit energy in kWh/Acre-Foot
    
    Gross_Head = New_Melones_El - New_Melones_TR

    # Original formula
    #'New_Melones_EF = _
    #    619.8115877 * Exp((((Gross_Head) - 855.1501661) ^ 2) _
    #    / -356386.5665)

    if New_Melones_El > 808.0:
        return (0.62455 * Gross_Head) + 142.3077
    else:
        return 0.0
    #'Modified by K. Nguyen, 9/13/2005.

def New_Melones_MW_BEP( New_Melones_El, New_Melones_TR ):
    
    Gross_Head = New_Melones_El - New_Melones_TR
    
    # 'Set Maximum Unit MW for New_Melones
    Max_MW = 190
    
    return min ( 0.746 / 1000 * math.pow(10, (-61.9481 + 68.8018 * math.log10(Gross_Head) - 23.7438 * math.pow((math.log10(Gross_Head)), 2) + 2.77249 * math.pow((math.log10(Gross_Head)), 3))) , Max_MW )
    
def New_Melones_MW_Peak( New_Melones_El, New_Melones_TR ):
    
    Gross_Head = New_Melones_El - New_Melones_TR
    
    # 'Set Maximum Unit MW for New_Melones
    Max_MW = 190

    if New_Melones_El > 808.0:
        return min( 0.030149853 * math.pow((Gross_Head), 1.493121708) / 2, Max_MW)
    else:
        return 0.0
                
def Tulloch_El( Storage ):

    # 'Returns Elevation in feet above MSL
    # 'Note need to check this equation
    # 'Added 11/13/01 by J. Johannis

    return 0.8119 * Storage + 455.64

def ONeill_El( Storage ):

    # 'Returns Elevation in feet above MSL
    # 'Currently set to constant
    # 'Need to develop equation or table
    # 'Storage not currently used

    return 225
        
def San_Luis_El( SL_Storage, ONL_Storage ):

    # 'Returns Elevation above MSL
    # 'Input Storage in TAF
    
    SL_Storage = SL_Storage * 1000
    
    return ONeill_El(ONL_Storage) + 83.37535633 * math.exp((math.pow((2.317314477 - math.log(SL_Storage / 1000)), 2)) / 20.95955205)

def San_Luis_Gen_EF( SL_Storage, ONL_Storage ):

    # 'Returns Unit energy in kWh/Acre-Foot
    # 'Use Rotor Speed 120 below head 195
    # 'Use Rotor Speed 150 above/equal head 195
    
    # 'Input Storage in TAF
      
    Gross_Head = San_Luis_El(SL_Storage, 0) - ONeill_El(ONL_Storage)
    
    if (Gross_Head < 195):

        return max( 296.0158035 - 7572.401144 / Gross_Head - 2773670.223 / (math.pow(Gross_Head , 2)), 0.0)
            
    else:

        return max ( 375.4941448 + 7287.699523 / Gross_Head - 11026204.24 / (math.pow(Gross_Head, 2)), 0.0 )
                      

def San_Luis_Gen_MW( SL_Storage, ONL_Storage ):

    # 'Returns Unit energy in kWh/Acre-Foot
    # 'Use Rotor Speed 120 below head 195
    # 'Use Rotor Speed 150 above/equal head 195
    
    # 'Input Storage in TAF
    
    Gross_Head = San_Luis_El(SL_Storage, 0) - ONeill_El(ONL_Storage)
    
    
    if (Gross_Head < 195) :
        return max ( -207.2183354 + 44.03002131 * math.log(Gross_Head), 0.0 )

    else:
        return max( 68.70218999 + 0.079510176 * Gross_Head - 13805.01994 / Gross_Head, 0.0 )
   

def San_Luis_Pump_EF( SL_Storage, ONL_Storage ): 

    # 'Returns Unit energy in kWh/Acre-Foot
    # 'Use Rotor Speed 120 below head 195
    # 'Use Rotor Speed 150 above/equal head 195
    
    # 'Input Storage in TAF
        
    Gross_Head = San_Luis_El(SL_Storage, 0) - ONeill_El(ONL_Storage)
    
    if (Gross_Head < 195):
        return 1 / (-0.000000355 * math.pow((Gross_Head - 119.2003765), 2) + 0.006298141)
    else:
        return 242.7856439 * math.exp((math.pow((5.124621702 - math.log(Gross_Head)), 2)) / 0.983372355)

def San_Luis_Pump_MW( SL_Storage, ONL_Storage ):

    # 'Returns Unit energy in kWh/Acre-Foot
    # 'Use Rotor Speed 120 below head 195
    # 'Use Rotor Speed 150 above/equal head 195
    
    # 'Input Storage in TAF
          
    Gross_Head = San_Luis_El(SL_Storage, 0) - ONeill_El(ONL_Storage)
    
    if (Gross_Head < 195):
    
        return 0.703815078 * Gross_Head / (math.pow(1.009743961, Gross_Head))
    else:
        return 0.660160387 * Gross_Head / (math.pow(1.0050363, Gross_Head))

def Trinity_Trans_Loss():
    # 'This uses a western's polynomial fit to 2948a loss tables for Northern System
    # function body is empty? Ho, Patrick
    pass


def JFCarr_EF( Lewiston_El, Whiskeytown_El ):

    # 'Returns Unit energy in kWh/Acre-Foot

    Gross_Head = Lewiston_El - Whiskeytown_El

    # Original formula
    # 'JFCarr_EF = 366.8115638 * 1.000433765 ^ (Gross_Head)
    return 551.7494
    # 'Modified by K. Nguyen, 9/13/2005.

def JFCarr_MW_BEP( Lewiston_El, Whiskeytown_El ):
       
    # 'Set Maximum Unit MW for JF Carr
    Max_MW = 77

    Gross_Head = Lewiston_El - Whiskeytown_El

    return min( 0.001070868 * math.pow((Gross_Head), 1.809768908) / 2, Max_MW)
                            

def JFCarr_MW_Peak( Lewiston_El, Whiskeytown_El ):
        
    # 'Set Maximum Unit MW for JF Carr
    Max_MW = 77

    Gross_Head = Lewiston_El - Whiskeytown_El

    return min( 0.001928427 * math.pow((Gross_Head), 1.722128852) / 2, Max_MW)
                           

def Spring_Creek_EF( Whiskeytown_El, Keswick_El ):

    # 'Returns Unit energy in kWh/Acre-Foot

    Gross_Head = Whiskeytown_El - Keswick_El

    # Original formula
    # 'Spring_Creek_EF = _
    #412.8920175 * Exp(((6.192010818 - Log(Gross_Head)) ^ 2) / 0.37933801)

    return (1.96704 * Gross_Head) - 717.1694
    # 'Modified by K. Nguyen, 9/13/2005.
            
def Spring_Creek_MW_Peak( Whiskeytown_El, Keswick_El ):
            
    Gross_Head = Whiskeytown_El - Keswick_El
    # 'Set Maximum Unit MW for Spring Creek
    Max_MW = 100

    return min( 0.006098238 * math.pow((Gross_Head), 1.607333778) / 2, Max_MW)
            
def Spring_Creek_MW_BEP( Whiskeytown_El, Keswick_El ):

     # 'Set Maximum Unit MW for Spring Creek
    Max_MW = 100

    Gross_Head = Whiskeytown_El - Keswick_El

    return min( 0.746 / 1000 * math.pow(10, (-3.36379 + 4.59468 * math.log10(Gross_Head) - 0.56425 * math.pow((math.log10(Gross_Head)), 2))), Max_MW )
    

def Lewiston_El( Storage ):

    # 'Returns Elevation in feet above MSL
    # 'Currently set to constant
    # 'Need to develop equation or table
    # 'Input Storage in TAF (to be consistant)

    # Original value
    # 'Lewiston_El = 1900.95
    return 1901.5

    # 'Modified by K. Nguyen, 8/28/2002.  Same as the Trinity Tailwater
    # 'elevation.
    
def Lewiston_TR( Lewiston_El ):
    # 'Dummy function made by Jami Nelson 2-6-02
    # 'In feet
    return 1500

def Lewiston_MW_Peak( Lewiston_El, Lewiston_TR ):
  
    # 'Modified by J. Johannis on 4/18 to approximate
    # 'actual Lewiston Performance.
    # 'Actual equation still needs to be developed  

    # 'Set Maximum Unit MW for Lewiston
    Max_MW = 0.35

    Gross_Head = Lewiston_El - Lewiston_TR

    # 'JJ - Temporary Eqn as of 4/18/02
    return Max_MW
    

def Lewiston_EF( Lewiston_El, Lewiston_TR ):
 
    # 'Returns Unit energy in kWh/Acre-Foot
    # 'Modified by J. Johannis on 4/18 to approximate
    # 'actual Lewiston Performance.
    # 'Actual equation still needs to be developed
    
    Gross_Head = Lewiston_El - Lewiston_TR

    # 'JJ - Temporary Eqn as of 4/18/02
    
    return 42.35
    

def ONiell_EF( ONiell_El ):
 
    # 'Returns Unit energy in kWh/Acre-Foot
        
   return 35
   # 'Modified by K. Nguyen, 9/13/2005.
            
def ONeill_MW_Flow( Powerplant_Release_CFS, ONeill_EF, ONeill_Peak_MW, Units_Available ):

    # 'Returns total plant Megawatts (not unit)
    # 'Same Formula as Keswick
               
    # 'Set Maximum MW for Nimbus (ENTIRE PLANT)
    Max_MW = Units_Available * ONeill_Peak_MW

    # 'This formula will not be accurate for days not equal
    # 'to 24 hours (begin and end of Daylight Savings Time)

    return min( Powerplant_Release_CFS * 0.0000825 * ONeill_EF, Max_MW)
         
def San_Felipe_EF( SL_Storage ):
    # 'This function is from the CVP Power program accompanying PROSIM
    # 'Jami Nelson 2-25-02
   
    # 'Set coefficients
    
    sfc1 = 0.00004
    sfc2 = -0.2414
    sfc3 = 452.2
    
    return sfc1 * math.pow((SL_Storage), 2) + sfc2 * (SL_Storage) + sfc3


def Folsom_PP_EF( Folsom_Storage ):

    # 'This function is from the CVP Power program accompanying PROSIM
    # 'Threshold is TAF
    # 'Jami Nelson 2-25-02
    
    # 'Dim fol1 As Double
    # 'Dim fol2 As Double
    # 'Dim fol3 As Double
    # 'Dim Threshold As Double
    # 'Set coefficients
    
    # 'fol1 = 0.0002
    # 'fol2 = -0.3135
    # 'fol3 = 101.57
    # 'Threshold = 450
    
    # 'Folsom_PP_EF = (fol1 * ((RMIN(Folsom_Storage, Threshold)) ^ 2)) + (fol2 * (RMIN(Folsom_Storage, Threshold))) + (fol3)


    # '**********************************************************************************
    # 'PROSIM function given above is considered obsolete and is superseded from the one
    # 'given below which was developed by M. Bauer in documented in, "Project Use Power_
    # 'Judgement, San Juan Surbuban Lawsuit", K. Nguyen, 01/13/2003
            
    Folsom_Storage = Folsom_Storage * 1000
    
    return math.pow(10, (398.408965953241 - 221.846267920264 * math.log10(Folsom_Storage) + 41.4087903495005 * math.pow((math.log10(Folsom_Storage)), 2) -  2.57740125017695 * math.pow((math.log10(Folsom_Storage)), 3)))

######################_____END CVP RATINGS_____#######################

######################_____SWP FACILITY RATINGS_____#######################

#'Oroville elevation based on storage
def Oroville_El(Storage):
    
  if Storage < 846.367:
    return 656.6 * math.pow((Storage / 1000), 0.1876)
  else:
    return -17.207 * math.pow((Storage / 1000), 2) + 172.37 * (Storage / 1000) + 508.61


#'Thermalito elevation based on storage
def Thermalito_El(StorageI):

    #Storage = StorageI
    #if Storage > 13.715:
    #    Storage = 13.715
  
    #if Storage < 0.1:
    #    Storage = 0.1

    Storage = min(max(StorageI, 0.1), 13.715)

    if Storage >= 0.746:
        return -0.0012 * math.pow(Storage, 4) + 0.0458 * math.pow(Storage, 3) - 0.6553 * math.pow(Storage, 2) + 6.0187 * Storage + 193.91
    else:
        return 3.6295 * math.log(Storage) + 198.85
  
#'Thermalito afterbay elevation
def ThermAB_El():
  return 130

#'Hyatt power plant energy factor; function of elevation head
def Hyatt_EF(Orov_Elev, ThermFB_Elev):
  
  Gross_Head = Orov_Elev - ThermFB_Elev
  if Gross_Head < 505:
    A = 8096.1
    B = -1.28
    C = 100
  elif Gross_Head >= 505 and Gross_Head < 555:
    A = 2930.2226
    B = -1.13794
    C = 48
  elif Gross_Head >= 555:
    A = 398.667
    B = -0.84085
    C = -15
  
  return 1000 / ((A * math.pow((Gross_Head + C), B)))

# 'Maximum theoretical power production, based on plant efficiency
def Power_Calc(H, Q, e):
  #'specific weight is 62.4 lb / ft3, head is in feet, flow in cfs, dividing by 550 gives horsepower,
  #'multiplying by 0.7457 converts to kilowatts, dividing by 1000 converts to megawatts
  return 62.4 * H * Q * e * 0.7457 / 550.0 / 1000.0

#'Minimum theoretical power consumption, based on plant efficiency
def Consume_Calc(Head, Flow, efficiency):
  #'specific weight is 62.4 lb / ft3, head is in feet, flow in cfs, dividing by 550 gives horsepower,
  #'multiplying by 0.7457 converts to kilowatts, dividing by 1000 converts to megawatts
  return 62.4 * Head * Flow / efficiency * 0.7457 / 550 / 1000

#'Maximum flow based on pumping plant load (MW) rating and all other plant characteristics
def Flow_Calc(Static_Head, MW, effic):
#  'specific weight is 62.4 lb / ft3, head is in feet, MW is plant capacity in MEGAWATTS, dividing by 550 gives horsepower,
#  'multiplying by 0.7457 converts to kilowatts, dividing by 1000 converts to megawatts
  return (550 * effic * MW / (62.4 * Static_Head)) * (1000 / 0.7457)

#'Thermalito power plant energy factor; function of elevation head
def Thermalito_EF(ThermFB_El, ThermAF_El):
  Gross_Head = ThermFB_El - ThermAF_El
  return -0.0132 * math.pow(Gross_Head, 2) + 3.4256 * Gross_Head - 126.39

#'San Luis water surface elevation as a function of storage
#'(from SWRI CVP power model)
def San_Luis_El(SL_Storage, ONL_Storage):
  #'Returns Elevation above MSL
  #'Input Storage in TAF
  SL_Storage = SL_Storage
  return ONeill_El(ONL_Storage) + 83.37535633 * math.exp((math.pow((2.317314477 - math.log(SL_Storage)), 2)) / 20.95955205)

#'Oneill water surface elevation assumed to be constant
#'(from SWRI CVP power model)
def ONeill_El(Storage):
  #'Returns Elevation in feet above MSL
  #'Currently set to constant
  #'Need to develop equation or table
  #'Storage not currently used
  return 225
   
#'Energy factor for San Luis pumping plant; a function of head
#'(from SWRI CVP power model)
def San_Luis_Pump_EF(SL_Storage, ONL_Storage):
  #'Returns Unit energy in kWh/Acre-Foot
  #'Use Rotor Speed 120 below head 195
  #'Use Rotor Speed 150 above/equal head 195
  #'Input Storage in TAF
  
    Gross_Head = San_Luis_El(SL_Storage, 0) - ONeill_El(ONL_Storage)
    if (Gross_Head < 195):
        return 1 / (-0.000000355 * math.pow((Gross_Head - 119.2003765), 2) + 0.006298141)
    else:
        return 242.7856439 * math.exp((math.pow((5.124621702 - math.log(Gross_Head)), 2)) / 0.983372355)
    
  
#'San Luis power requirement based on head to be generated by the pumps
#'(from SWRI CVP power model)
def San_Luis_Pump_MW(SL_Storage, ONL_Storage): 
  #'Returns Unit energy in kWh/Acre-Foot
  #'Use Rotor Speed 120 below head 195
  #'Use Rotor Speed 150 above/equal head 195
  #'Input Storage in TAF
  
  Gross_Head = San_Luis_El(SL_Storage, 0) - ONeill_El(ONL_Storage)
  
  if (Gross_Head < 195):
    return 0.703815078 * Gross_Head / (math.pow(1.009743961, Gross_Head))
  else:
    return 0.660160387 * Gross_Head / (math.pow(1.0050363, Gross_Head))
  
#'Pyramid Lake water surface elevation as a function of storage
def Pyramid_El(Storage):
  if (Storage / 1000) > 0.05:
    return -1932.8 * math.pow((Storage / 1000), 2) + 1473.1 * (Storage / 1000) + 2385.1
  else:
    return -32770 * math.pow((Storage / 1000), 2) + 4217 * (Storage / 1000) + 2323.1
  
#'Castaic Lake water surface elevation as a function of storage
def Castaic_El(Storage):

  if (Storage / 1000) > 0.03:
    return -17231 * math.pow((Storage / 1000), 4) + 16744 * math.pow((Storage / 1000), 3) - 6531.9 * math.pow((Storage / 1000), 2) + 1730.6 * (Storage / 1000) + 1260.6
  else:
    return -66667 * math.pow((Storage / 1000), 2) + 5666.7 * (Storage / 1000) + 1200
  
#'Castaic Power Plant energy factor as a function of water surface elevation
def Castaic_EF(elev, tailRace):
    Castaic_Head = elev - tailRace
    return 0.99097 * Castaic_Head - 92.9883

#'Devil canyon power plant
#'C. Hsu, USBR 8/28/2003 with elevation and storage information from CALSIM
def DCanyon_El(Storage):
#'Input Storage in TAF
    if Storage < 44.94:
        return 3058.9 + 68.961 * math.log(Storage)
    else:
        return 63.548 * math.log(Storage) + 3078.3

#' Tair race for Devil Canyon
def DCanyon_TR():
    return 1917.0

######################_____END SWP RATINGS_____#######################

class characteristics:
    def __init__(self, fl):
        import csv
        fl = open(fl, "rb")
        csvFile = csv.reader(fl)
        i = 1
        index = []
        for row in csvFile:
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
        
