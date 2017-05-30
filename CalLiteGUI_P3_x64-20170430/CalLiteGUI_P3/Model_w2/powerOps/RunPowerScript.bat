rem @echo off
rem This file runs the power module script for CVP and SWP 
rem Author: Taraky
rem Date: 03/01/2017

title Power Script

rem enable jython environment
rem jython

rem run jython power script for CVP
START/WAIT/B %~dp0..\vscript\lib\vista\jython\bin\jython ltgen.py 

rem run jython power script for SWP
START/WAIT/B %~dp0..\vscript\lib\vista\jython\bin\jython swpgen.py
