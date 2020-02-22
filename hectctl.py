#-------------------------------------------
def removeoutliers_ctl(station, component):
#-------------------------------------------
    """ 
# Function : Creates Hector control file for removing outliers
#
# Author  : Original script: Bos et al., (http://segal.ubi.pt/hector/ or doi:10.1007/s00190-012-0605-0) 
#         : Modified by : Kibrom E. Abraha
#
# Inputs   : station - Station name
#          : component - coordinate component (East|North|Up)
# Outputs  : removeoutliers.ctl file
#          : 
#
#----------------------------------------------------
    """


    ctl_f = open("removeoutliers.ctl", "w")
    ctl_f.write("DataFile            {0:s}.enu\n".format(station))
    ctl_f.write("DataDirectory         ./hectorInputs/\n")
    ctl_f.write("component             {0:s}\n".format(component))
    ctl_f.write("interpolate           no\n")
    ctl_f.write("OutputFile            ./hectorResults/{0:s}_outliers_removed.mom\n".format(station+'_'+component))
    ctl_f.write("seasonalsignal        yes\n")
    ctl_f.write("halfseasonalsignal    yes\n")
    ctl_f.write("estimateoffsets       yes\n")
    ctl_f.write("estimatepostseismic   yes\n")
    ctl_f.write("estimateslowslipevent yes\n")
    ctl_f.write("ScaleFactor           1.0\n")
    ctl_f.write("PhysicalUnit          mm\n")
    ctl_f.write("IQ_factor             3\n")
    ctl_f.close()


#------------------------------------------------------
def estimatetrend_ctl (station, component, noisemodel):
#------------------------------------------------------
    """ 
# Function : Creates Hector control file for estimating trend
#
# Author  : Original script: Bos et al., (http://segal.ubi.pt/hector/ or doi:10.1007/s00190-012-0605-0) 
#         : Modified by : Kibrom E. Abraha
#
# Inputs   : station - Station name
#          : component - coordinate component (East|North|Up)
#          : noisemodel (string): GGMWN, PLWN, FNWN, RWFNWN or WN
# Outputs  : estimatetrend.ctl file
#          : 
#   Notes: If more periodic signals are requred to be estimated, uncomment the line ctl_f.write("periodicsignals ... and add more periods if needed
#          : 
#----------------------------------------------------
    """


    ctl_f = open("estimatetrend.ctl", "w")
    ctl_f.write("DataFile              {0:s}_outliers_removed.mom\n".format(station+'_'+component))
    ctl_f.write("DataDirectory         ./hectorResults/\n")
    ctl_f.write("OutputFile            ./hectorResults/{0:s}_estimated_trend.mom\n".format(station+'_'+component))
    ctl_f.write("interpolate           no\n")
    ctl_f.write("ScaleFactor           1.0\n")
    if noisemodel == 'GGMWN':
        ctl_f.write("NoiseModels           GGM White\n")
    elif noisemodel == 'FNWN':
        ctl_f.write("NoiseModels           FlickerGGM White\n")
        ctl_f.write("GGM_1mphi             6.9e-06\n")
    elif noisemodel == 'PLWN':
        ctl_f.write("NoiseModels           Powerlaw White\n")
        ctl_f.write("GGM_1mphi             6.9e-06\n")
        ctl_f.write("LikelihoodMethod      AmmarGrag\n")
    elif noisemodel == 'RWFNWN':
        ctl_f.write("NoiseModels           RandomWalkGGM FlickerGGM White\n")
        ctl_f.write("GGM_1mphi             6.9e-06\n")
    elif noisemodel == 'WN':
        ctl_f.write("NoiseModels           White\n")
    elif noisemodel == 'AR1':
        ctl_f.write("NoiseModels           ARMA\n")
        ctl_f.write("AR_p                  1\n")
        ctl_f.write("MA_q                  0\n")
    else:
        print("Unknown noise model: {0:s}".format(noisemodel))
        sys.exit()
    ctl_f.write("seasonalsignal        yes\n")
    ctl_f.write("halfseasonalsignal    yes\n")
    ctl_f.write("estimateoffsets       yes\n")
    ctl_f.write("estimatepostseismic   yes\n")
    #ctl_f.write("periodicsignals       351.2 175.6 117.06 87.80 70.24 58.53 50.17 43.9 14.72 13.67\n")
    ctl_f.write("estimateslowslipevent yes\n")
    ctl_f.write("ScaleFactor           1.0\n")
    ctl_f.write("PhysicalUnit          mm\n")
    ctl_f.close()

#-------------------------------------------
def estimatespectrum_ctl(station, component):
#-------------------------------------------
    """ 
# Function : Creates Hector control file for spectral analysis
#
# Author   : Kibrom E. Abraha
#
# Inputs   : station - Station name
#          : component - coordinate component (East|North|Up)
# Outputs  : estimatespectrum.ctl file
#          : 
#
#----------------------------------------------------
    """


    ctl_f = open("estimatespectrum.ctl", "w")
    ctl_f.write("DataFile              {0:s}_estimated_trend.mom\n".format(station+'_'+component))
    ctl_f.write("DataDirectory         ./hectorResults/\n")
    ctl_f.write("OutputFile            ./hectorResults/{0:s}_estimatedSpectrum.spectra\n".format(station+'_'+component))
    ctl_f.write("interpolate           no\n")
    ctl_f.write("firstdifference       no\n")
    ctl_f.write("ScaleFactor           1.0\n")
    ctl_f.write("WindowFunction        Parzen\n")
    ctl_f.write("Fraction              0.1\n")
    ctl_f.close()


#-------------------------------------------
def modelspectrum_ctl(station, component, noisemodel):
#-------------------------------------------
    """ 
# Function : Creates Hector control file for spectral modeling
#
# Author   : Kibrom E. Abraha
#
# Inputs   : station - Station name
#          : component - coordinate component (East|North|Up)
#          : noisemodel (string): GGMWN, PLWN, FNWN, RWFNWN or WN
# Outputs  : modelspectrum.ctl file
#          : 
#
#----------------------------------------------------
    """


    ctl_f = open("modelspectrum.ctl", "w")
    ctl_f.write("OutputFile            ./hectorResults/{0:s}_modeledSpectrum.spectra\n".format(station+'_'+component))
    if noisemodel == 'GGMWN':
        ctl_f.write("NoiseModels           GGM White\n")
    elif noisemodel == 'FNWN':
        ctl_f.write("NoiseModels           FlickerGGM White\n")
    elif noisemodel == 'PLWN':
        ctl_f.write("NoiseModels           Powerlaw White\n")
    elif noisemodel == 'RWFNWN':
        ctl_f.write("NoiseModels           RandomWalkGGM FlickerGGM White\n")
    elif noisemodel == 'WN':
        ctl_f.write("NoiseModels           White\n")
    elif noisemodel == 'AR1':
        ctl_f.write("NoiseModels           ARMA\n")
    else:
        print("Unknown noise model: {0:s}".format(noisemodel))
        sys.exit()
    ctl_f.write("PhysicalUnit          mm\n")
    ctl_f.close()
