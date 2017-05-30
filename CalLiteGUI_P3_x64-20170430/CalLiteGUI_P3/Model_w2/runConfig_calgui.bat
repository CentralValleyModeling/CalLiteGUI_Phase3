echo on

IF [%1]==[] (
	echo ==================================
	echo # Error: Config file path Missing
	echo ==================================
	pause
	
	)

set ScenarioName=%2
set ConfigFilePath=%1
set ConfigFilePath=%ConfigFilePath:/=\%

for %%F in (%ConfigFilePath%) do set dirname=%%~dpF
set RunDir=%dirname%run\


echo on

:-------------------------------------------------------:
: dir for sty file generation (read by groundwater.dll) :
:-------------------------------------------------------:  

set temp_wrims2=%dirname%run\

:------------------:
: wrims2 lib jars  :
:------------------:
set JarDir=%~dp0\lib
set VistaLibDir=%~dp0\vscript\lib\vista\lib
set AppJars=%JarDir%\WRIMSv2.jar
set AppJars=%AppJars%;%JarDir%\gurobi.jar
set AppJars=%AppJars%;%VistaLibDir%\heclib.jar
set AppJars=%AppJars%;%JarDir%\jnios.jar
set AppJars=%AppJars%;%JarDir%\jpy.jar
set AppJars=%AppJars%;%JarDir%\misc.jar
set AppJars=%AppJars%;%JarDir%\pd.jar
set AppJars=%AppJars%;%VistaLibDir%\vista.jar
set AppJars=%AppJars%;%JarDir%\lpsolve55j.jar
set AppJars=%AppJars%;%JarDir%\commons-io-2.1.jar
set AppJars=%AppJars%;%JarDir%\javatuples-1.2.jar
set AppJars=%AppJars%;%JarDir%\guava-11.0.2.jar
set AppJars=%AppJars%;%JarDir%\XAOptimizer.jar
set AppJars=%AppJars%;%JarDir%\log4j-1.2.17.jar
set AppJars=%AppJars%;%~dp0..\bin
set AppJars=%AppJars%;%~dp0..\calgui.jar


:---------------------------------:
: user defined java class and dll :
:---------------------------------:
set ExternalDir=%RunDir%External

:------------:
: class path :
:------------:
set CLASSPATH=-classpath "%ExternalDir%;%AppJars%"

:------------:
: dll path   :
:------------:
set PATH=%ExternalDir%;%JarDir%;%VistaLibDir%


: --------------------------------------------------------------------------------------:
: Write the full java run string to last_singleton.bat for debugging if needed :
:---------------------------------------------------------------------------------------:

echo %temp_wrims2%/../../../../jre8/bin/java -Xmx1000m -Xss1280K -Djava.library.path=%PATH% %CLASSPATH% gov.ca.water.calgui.batch.Singleton -config="%configFilePath%" > last_singleton.bat

:-------------------------------------------------------:
: call java to run ControllerBatch class                :
:-------------------------------------------------------:

start /min /wait "CalLiteRun%ScenarioName%" %temp_wrims2%/../../../../jre8/bin/java -Xmx1000m -Xss1280K -Djava.library.path=%PATH% %CLASSPATH% gov.ca.water.calgui.batch.Singleton -config="%configFilePath%"

exit