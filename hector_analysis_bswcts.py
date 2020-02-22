#!/usr/bin/env python3
import sys
import os
import shutil
from dates import *
from crdtrns import *
from hectctl import *

#
# run program as hector_analysis_bswcts.py station_list Noise_model spectral_analysis_condition
#
#--- Read command line arguments

if (len(sys.argv)<4 or len(sys.argv)>4):
    print('\n')
    print ('>> Nope! :( run it correctly \n ')
    print('>> Check your input parameters. Use Script as follows: \n ')
    print('>> hector_analysis_bswcts.py station_list Noise_model spectral_analysis_condition \n')
    print('>> Noise model examples: GGMWN, PLWN, FNWN ... (see estimatetrend_ctl function)\n')
    print('>> Spectral_analysis_condition is "YES" or "NO". if "YES", spectrum will be estimated') 
    print (' and modeled for each station and  coordinate conponent.') 
    print (' Enter "NO" if you would like to estimate the trend and periodicities only \n')
    sys.exit()
else:
    stnlist    = sys.argv[1]
    noisemodel = sys.argv[2]
    Spectral = sys.argv[3]

#read station list
stations = []
try:
    f = open(stnlist, 'r')
except FileNotFoundError:
    print ("There is no station list file \n")
    sys.exit(0)

for lines in f:
    stations.append(lines.split()[0])

f.close()

#coordinate componets to analyze
components = ['East', 'North', 'Up']

#Hector inputs
enu_files = './hectorInputs/'

#Check if a directory is available for hector results
#Create it if not available

hectorResults = './hectorResults/'
if not os.path.isdir(hectorResults):
    os.mkdir(hectorResults)


print ("\n")
print ("Hector based GNSS time series Analysis --- Begins")
print ("=================================================")

for stns in stations:
    if os.path.isfile(enu_files + stns + ".enu"):
        print ("Station:  " + stns)
        for cmpts in components:
            print ("    " + cmpts + " Component")
            removeoutliers_ctl(stns, cmpts)
            estimatetrend_ctl(stns, cmpts, noisemodel)
            estimatespectrum_ctl(stns, cmpts)
            modelspectrum_ctl(stns, cmpts, noisemodel)


            os.system("removeoutliers removeoutliers.ctl > outliersRemoved.out")
            shutil.copyfile("./outliersRemoved.out", "./hectorResults/" + stns +'_'+ cmpts + "_outliersRemoved.out")
            os.remove('./outliersRemoved.out')
            #os.remove('./removeoutliers.ctl')
            print ("                --- Outliers removed" )

            os.system("estimatetrend estimatetrend.ctl > trendEstimated.out")
            shutil.copyfile("./trendEstimated.out", "./hectorResults/" + stns +'_'+ cmpts + "_trendEstimated.out")
            os.remove('./trendEstimated.out')
            #os.remove('./estimatetrend.ctl')

            print ("                --- Trend estimated" )

            if Spectral.upper() == 'YES':
                os.system("estimatespectrum estimatespectrum.ctl > spectrumEstimated.out")
                shutil.copyfile("./spectrumEstimated.out", "./hectorResults/" + stns +'_'+ cmpts + "_spectrumEstimated.out")
                os.remove('./spectrumEstimated.out')
             #   os.remove('./estimatespectrum.ctl')
                print ("                --- Spectrum estimated" )

                ##prepare inputs (modelspectrum.inp) to model spectrum (see hector1.7.2 manual page 15)

                ff = open('./hectorResults/' + stns +'_'+ cmpts + '_trendEstimated.out', 'r')
                
                tmp = []
                for i, lines in enumerate(ff):
                    tmp.append(lines)

                ff.close()

                
                for i, lines in enumerate(tmp):
                    if lines[0:25] == 'STD of the driving noise:':
                        stdv_noise = float(tmp[i].split()[5])
                        
                    if lines[0:9] == 'Powerlaw:':
                        PL_fraction = float(tmp[i+1].split()[2])
                        PL_d = float(tmp[i+3].split()[2])

                    if lines[0:6] == 'White:':
                        WL_fraction = float(tmp[i+1].split()[2])
                
                ff2 = open('./hectorResults/' + stns +'_'+ cmpts + '_spectrumEstimated.out', 'r')

                for lines in ff2:
                    if lines[0:6] =='freq0:':
                        freq0 = float(lines.split()[1])
                    if lines[0:6] =='freq1:':
                        freq1 = float(lines.split()[1])
                ff2.close()

                sampling = 24
                linear_or_log = 2

                sf = open('./modelspectrum.inp', 'w')

                sf.write("{}\n".format(stdv_noise))
                sf.write("{}\n".format(sampling))
                sf.write("{}\n".format(PL_fraction))
                sf.write("{}\n".format(WL_fraction))
                sf.write("{}\n".format(PL_d))
                sf.write("{}\n".format(linear_or_log))
                sf.write("{} {} \n".format(freq0, freq1))

                sf.close()

                os.system("modelspectrum  <  modelspectrum.inp > spectrumModeled.out")
                shutil.copyfile("./spectrumModeled.out", "./hectorResults/" + stns +'_'+ cmpts + "_spectrumModeled.out")
                os.remove('./spectrumModeled.out')
               # os.remove('./modelspectrum.inp')
                print ("                --- Spectrum modeled" )


    else:
        print ("File {} does not exist \n".format(stns+".enu"))

print ("\n Hector based GNSS time series Analysis --- Ends")
print ("=============================================== \n")


