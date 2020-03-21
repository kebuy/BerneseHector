#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import glob
import re
from dates import *
from crdtrns import *
from hectctl import *


"""
# Purpose : reads GPSEST output file from Bernese and creates .cts and .enu files
#
#
# Author  : Kibrom E. Abraha
#
#
#Inputs: stnlist -- a file with list of stations
#        yyyy -- starting year
#        m -- starting month
#        d -- starting day
#        yyyy2 -- ending year
#        m2 -- ending month
#        d2 -- ending day
#        offsetfile -- A file with offets information in IGS disconinuity file file format
#
#        soltype -- solution type, e.g. "PPP" or "DD" or any kind.
#                    This string variable will be  used as part of the
#                    file name of the .cts file
#Outputs: .cts and .enu (hector input) files for all stations in stnlist.txt
#        Example:
#        readGPSESToutput(stnlist.dat, 2018, 1, 25, 2018, 12, 31, offsetfile.dat, "PPP_CODE"):
#-------------------------------------------------------------------------------
#
#Notes:#
#
#   - GPSESToutput files have a a sepcific filename format, Example: F1_132580.OUT -- this is
#    a GPSEST output file of solution type (sol) = F1_, year 2013 (two character year ID - 13),
#    day of year =  258 and session = 0. The sol, and session (s) are usually common and are
#    defined variables which must be changed if the output file has a different naming convension.
#
#    - make sure the GPSESTinput files are all in one directory called GPSEST_files.
#    The GPSEST_output directly should be in the same path with  this script

"""

if (len(sys.argv)<10 or len(sys.argv)>10):
    print('\n')
    print ('>> Nope! :( run it correctly \n ')
    print('>> Check your input parameters. Use Script as follows: \n ')
    print('>> read_GPSEST_output stnlist.txt 2018 1 25 2019 12 31 offsetfile.txt "PPP_CODE"): \n')
    print('>> Noise model examples: GGMWN, PLWN, FNWN ... (see estimatetrend_ctl function)\n')
    print('>> Spectral_analysis_condition is "YES" or "NO". if "YES", spectrum will be estimated')
    print (' and modeled for each station and  coordinate conponent.')
    print (' Enter "NO" if you would like to estimate the trend and periodicities only \n')

    sys.exit()
else:
    stnlist = sys.argv[1]
    yyyy    = int(sys.argv[2])
    m       = int(sys.argv[3])
    d       = int(sys.argv[4])
    yyyy2   = int(sys.argv[5])
    m2      = int(sys.argv[6])
    d2      = int(sys.argv[7])
    offsetf = sys.argv[8]
    soltype = sys.argv[9]


#common file variables
sol = 'F1_'
ss = int(0)
ext = '.OUT'
#The GPSEST_output files path must be defined here
gpsest_files = './GPSEST_files/'

# .enu files will be stored in
enu_files = './hectorInputs/'
if not os.path.isdir(enu_files):
    os.mkdir(enu_files)

# .cts files will be stored in
cts_files = './bswCTS_files/'
if not os.path.isdir(cts_files):
    os.mkdir(cts_files)
#
allyears = np.arange(yyyy, yyyy2 + 1, 1)

#read station list
stnid = []
try:
    f2 = open(stnlist, 'r')
except FileNotFoundError:
    print ("There is no station list file \n")
    sys.exit(0)

for lines in f2:
    stnid.append(lines.split()[0])

f2.close()

#read offsets file
offsets = []
try:
    of = open(offsetf, 'r')
except FileNotFoundError:
    print ("There is no offset file \n")
    sys.exit(0)

for lines in of:
    offsets.append(lines)

of.close()


for stns in stnid:
    stnout = cts_files + stns + '_' + soltype + '.cts'

    if os.path.exists(stnout):
        os.remove(stnout)
        f3 = open(stnout, 'a+')
    else:
        f3 = open(stnout, 'a+')

    f3.write("#Solution type:- {}\n".format(soltype))
    f3.write("#MJD    Year   Mn  Day       X(m) \
    Y(m)          Z(m)          dX(m)    dY(m)    dZ(m)  Lat(deg) Lon(deg)\
    H(m) dLat(deg) dLon(deg)  dH(m)  North(m)      East(m)         Up(m)   dN(m)   dE(m)  dU(m) \n")
    f3.close()


    stnenu = enu_files + stns + '.enu'

    if os.path.exists(stnenu):
        os.remove(stnenu)
        fhect = open(stnenu, 'a+')
    else:
        fhect = open(stnenu, 'a+')

    fhect.write('# sampling period 1.0 \n')

    for oflines in offsets:
        if oflines[0:4] == stns:
            yy = float(oflines[10:14])
            mm = float(oflines[15:17])
            dd = float(oflines[18:20])
            offset_mjd = date2mjd(yy, mm, dd)
            for i in range(3):
                fhect.write("# offset {} {}\n".format(offset_mjd, i))
    fhect.close()



#find a midfile which will be used to grep coordinates (mean coordinate) of all stations which will be used to reduce the coordinates
#what if a station is not available that day?????
allfiles = sorted(list(glob.iglob(gpsest_files + '*.OUT')))
midfile = allfiles[int(len(allfiles)/2)]

mf = open(midfile, 'r')
line = mf.readline()

while (line):
    if (line[0:26] == ' Station name          Typ'):
        madress = mf.tell()
    line = mf.readline()

midallstations = []
mf.seek(madress)
line = mf.readline()
line = mf.readline()
while (line[0:24] != ' Troposphere parameters:'):
    midallstations.append(line)
    line = mf.readline()
mf.close()

midcts = {}
for stns in stnid:
    tmplist0 = stns.split('\n')[0] + 'stn0'
    print (tmplist0)
    tmplist0 = []


    for i, lines in enumerate (midallstations):
        if lines[1:5] == stns:
            for j in range (8): #print the next 8 lines
                tmplist0.append(midallstations[i + j])


    for lines in tmplist0:
        if lines[23:24] == 'X':
            X = float(lines[45:60])
        elif lines[23:24] == 'Y':
            Y = float(lines[45:60])
        elif lines[23:24] == 'Z':
            Z = float(lines[45:60])
    midcts[stns] = [X, Y, Z]

for i, yrs in enumerate(allyears):

    yy = str(yrs)[2:4]

    if yyyy == yyyy2:
        year1, firstdoy = yearmoydom2yearDoy(yyyy, m, d)
        year2, lastdoy = yearmoydom2yearDoy(yyyy2, m2, d2)
    else:
        if i == 0:
            year1, firstdoy = yearmoydom2yearDoy(yyyy, m, d)
            if leapYear(yrs):
                lastdoy = 366
            else:
                lastdoy = 365
        if i > 0 and i < (len(allyears) - 1):
            firstdoy = 1
            if leapYear(yrs):
                lastdoy = 366
            else:
                lastdoy = 365
        elif i == (len(allyears) - 1):
            firstdoy = 1
            year1, lastdoy = yearmoydom2yearDoy(yyyy2, m2, d2)

    alldoys = np.arange(firstdoy, lastdoy + 1, 1)

    for doy in alldoys:

        if doy < 10:
            zz = '00'
        elif doy >= 10 and doy < 100:
            zz = '0'
        else:
            zz = ''


        bswf = gpsest_files + '{}{}{}{}{}{}'.format(sol, yy, zz, doy, ss, ext)

        yr, moy, dom = yeardoy2yearMoyDom(yrs, doy)
        mjd = date2mjd(yr, moy, dom)


        if os.path.isfile(bswf):
            f = open(bswf, 'r')
            line = f.readline()
        else:
            print ("File {} does not exist \n".format(bswf))
            continue

        while (line):
            if (line[0:26] == ' Station name          Typ'):
                adress = f.tell()
            line = f.readline()

        allstations = []
        f.seek(adress)
        line = f.readline()
        line = f.readline()
        while (line[0:24] != ' Troposphere parameters:'):
            allstations.append(line)
            line = f.readline()
        f.close()

        for stns in stnid:
            tmplist = stns.split('\n')[0] + 'stn'
            tmplist = []


            for i, lines in enumerate (allstations):
                if lines[1:5] == stns:
                    for j in range (8): #print the next 8 lines
                        tmplist.append(allstations[i + j])


            if tmplist:  #only if the station is available (which means tmplist is not empty
                for lines in tmplist:
                    if lines[23:24] == 'X':
                        stname = lines[0:15]
                        X = float(lines[45:60])
                        dX = float(lines[80:88])
                    elif lines[23:24] == 'Y':
                        Y = float(lines[45:60])
                        dY = float(lines[80:88])
                    elif lines[23:24] == 'Z':
                        Z = float(lines[45:60])
                        dZ = float(lines[80:88])

                    elif lines[23:24] == 'N':
                        Lat = float(lines[45:60])
                        dLat = float(lines[80:88])

                    elif lines[23:24] == 'E':
                        Lon = float(lines[45:60])
                        dLon = float(lines[80:88])

                    elif lines[23:24] == 'U':
                        H = float(lines[45:60])
                        dH = float(lines[80:88])
            #mid coordinates
                x0 = midcts[stns][0]
                y0 = midcts[stns][1]
                z0 = midcts[stns][2]

                E, N, U = xyz2enu(X - x0, Y - y0, Z - z0, Lat, Lon, radians=False)
                dE, dN, dU = xyz2enu(dX, dY, dZ, Lat, Lon, radians=False)


                stnout = cts_files + stns + '_' + soltype + '.cts'
                f3 = open(stnout, 'a+')
                f3.write("{0:6.1f} {1:4.1f} {2:2.1f} {3:2.1f} {4:12.6f} {5:12.6f} {6:12.6f}	{7:2.6f} {8:2.6f} {9:2.6f} {10:6.6f} {11:6.6f} {12:6.6f} {13:2.6f} {14:2.6f} {15:2.6f} {16:12.6f} {17:12.6f}{18:12.6f} {19:2.6f} {20:2.6f} {21:2.6f}\n".format(mjd, yrs, moy, dom, X, Y, Z, dX, dY, dZ, Lat, Lon, H, dLat, dLon, dH, N, E, U, dN, dE, dU))
            #hector output file (in mm)
                stnenu = enu_files + stns + '.enu'
                fhect = open(stnenu, 'a+')
                fhect.write("{0:6.1f} {1:12.6f} {2:12.6f} {3:12.6f} \n".format(mjd, E*1000, N*1000, U*1000))
