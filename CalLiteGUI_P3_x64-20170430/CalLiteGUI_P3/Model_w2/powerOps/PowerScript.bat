rem @echo off
rem This file runs ltgen.py and swpgen.py Jython scripts to calculate CVP and SWP power generation
rem Author: Taraky
rem Date: 03/01/2017

title Power Script

rem echo %1
rem pause

rem enable jython environment & run ltgen.py jython script for CVP power calculation
START/WAIT/B %~dp0..\vscript\lib\vista\jython\bin\jython  ltgen.py %1

rem enable jython environment & run swpgen.py jython script for SWP power calculation
START/WAIT/B %~dp0..\vscript\lib\vista\jython\bin\jython  swpgen.py %1