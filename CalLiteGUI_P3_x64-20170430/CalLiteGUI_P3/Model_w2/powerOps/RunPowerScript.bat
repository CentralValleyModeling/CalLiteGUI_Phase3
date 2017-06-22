rem @echo off
rem This file calls "PowerScript" batch file from "\Model_w2\poweOps" folder  
rem Author: Taraky
rem Date: 04/03/2017

title Power Script 

rem calls the "PowerScript" batch file which runs ltgen.py and swpgen.py jython script
%~dp0PowerScript.bat "%~dp0..\..\Scenarios\DEFAULT_PowerCalculation2_DV.dss"