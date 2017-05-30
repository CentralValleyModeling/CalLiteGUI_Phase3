# Used imports for development, need to remove imports once linked with CalLite to
# avoid polluting the namespace, also, javaHecLib.dss was dumped in current
# directory. Should remove it once power simulation is working. -Ho, P MBK Engineers

import sys
import calendar

sys.path.append("../../lib")
sys.path.append("../../")
libDir = "../../lib/"
classPaths = ["hec.jar", "hecData.jar", "heclib.jar", "rma.jar"]

for classPath in classPaths:
    sys.path.append(libDir + classPath)

from hec import *
from hec.heclib import *
from hec.heclib.dss import *
from hec.heclib.util import HecTime
from hec.hecmath import  *
from hec.io import TimeSeriesContainer

import java.util.Date
import java.util.GregorianCalendar
import java.text.SimpleDateFormat


# end note

def openDSS(fl):
    HecDataManager().setMessageFile("HecFileOps.log")
    return DSS.open(fl)

def getDssTsValues(fl, path, start, end):
    fl.setTimeWindow(start, end)
    hm = fl.read(path)
    tsc = hm.getData()
    ts = []
        
    for i,val in enumerate(tsc.values):
        ts.append([])
        htime = HecTime()
        htime.set(tsc.times[i])
        gc = java.util.GregorianCalendar(htime.year(), htime.month()-1, htime.day())
        dt_yr = htime.year()-1900
        dt_mn = htime.month()-1
        dt_dy = htime.day()                   
        dt = java.util.Date(dt_yr, dt_mn, dt_dy)
        ts[i].append(dt)
        ts[i].append(val)
            
    return ts

def setDssTsValues(f1, data, tSt, path, timeUnit, units, typ):

    tsc = TimeSeriesContainer()
    hTime = HecTime()
    hTime.set(tSt)
    tm = []
    dt = []
    for i in range(len(data)):
        tm.append(data[i][0])
        dt.append(data[i][1])     
    times = []
    tsc.interval = timeUnit # default is minutes
    for value in dt:
        times.append(hTime.value())
        hTime.add(tsc.interval)    
    tsc.fullName = path
    tsc.numberValues = len(dt)
    tsc.times = times
    tsc.units = units
    tsc.type = typ
    tsc.values = dt
    f1.write(HecMath.createInstance(tsc))
    
def getDaysInMonth(JDate):
    form = java.text.SimpleDateFormat("dd")
    return form.format(JDate)

def summation(fl, paths, start, end):

    ts = getDssTsValues(fl, paths[0], start, end)
    
    for i in range(1, len(paths)):
        for j, value in enumerate(getDssTsValues(fl, paths[i], start, end)):
            ts[j][1] += value[1]
       
    return ts
    
        
    
