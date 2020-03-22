#!/usr/bin/env python
# coding: utf-8

def cts2df(inputfile, notrend=True):
    """
# Function : Creates Pandas Dataframe from a .cts file 
#            (.cts file must be in a format created by readGPSESToutput().
#
#
#
# Author  : Kibrom E. Abraha
#
#
#Inputs: inputfile -- file name (including the file path) 
#        Defalut returns df with detrended N, E, U values
#        if the trend is needed in the df, notrend=False shall be used
#
#Outputs: pandas Dataframe
#-------------------------------------------------------------------------------
    """
    cts = open(inputfile, 'r')

    station = os.path.basename(inputfile)
    stname = station[0:4]
    
    decYr, mjd, year, moy, dom, n, e, u, dn, de, du = [
        [] for i in range(11)]
    list1 = [decYr, year, moy, dom, n, e, u, dn, de, du]
    columns = ['decY', 'year', 'moy', 'dom', 'N', 'E', 'U',
               'dN', 'dE', 'dU']
    df = pd.DataFrame(columns=columns)
    
    dy, lastDoy = [0 for i in range(2)]
    
    for lines in cts:
        if lines[0:1] != '#':
            try:
                ctsdata = lines.split()
                year.append(float(ctsdata[1]))
                moy.append(float(ctsdata[2]))
                dom.append(float(ctsdata[3]))

                n.append(float(ctsdata[16]) * 1000) #mm
                e.append(float(ctsdata[17]) * 1000)
                u.append(float(ctsdata[18]) * 1000)

                dn.append(float(ctsdata[19]) * 1000)
                de.append(float(ctsdata[20]) * 1000)
                du.append(float(ctsdata[21]) * 1000)

                dy, lastDoy = decimalYear2(float(ctsdata[1]),float(ctsdata[2]),float(ctsdata[3]))
                decYr.append(dy)
            except:
                continue   

    for dfi, ls in zip(df.columns, list1):
        df[dfi] = ls
    
    cts.close()
    
    if notrend:
        mn, bn, dn  = lintrend(df.decY, df.N, dtrend=True)
        me, be, de  = lintrend(df.decY, df.E, dtrend=True)
        mu, bu, du  = lintrend(df.decY, df.U, dtrend=True)
        df = pd.DataFrame(list(zip(df.decY, dn, de, du, df.dN, df.dE, df.dU)), 
                          columns=['decY', 'N', 'E', 'U', 'dN', 'dE', 'dU'])
        return df
    else:
        return df



def HectorNEU2df(inputfile, notrend=True):
    """
# Function : Creates Pandas Dataframe from a Hector Input files (.enu) file 
#            (.enu file must be in a format created by readGPSESToutput().
#
#
#
# Author  : Kibrom E. Abraha
#
#
#Inputs: inputfile -- file name (including the file path) 
#        Defalut returns df with detrended N, E, U values
#        if the trend is needed in the df, notrend=False shall be used 
#
#Outputs: pandas Dataframe
#-------------------------------------------------------------------------------
    """
    cts = open(inputfile, 'r')

    station = os.path.basename(inputfile)
    stname = station[0:4]
    
    decYr, mjd, n, e, u = [ [] for i in range(5)]
    list1 = [decYr, mjd, n, e, u]
    columns = ['decY', 'mjd', 'N', 'E', 'U']
    df = pd.DataFrame(columns=columns)
    
    dy, lastDoy = [0 for i in range(2)]
    
    for lines in cts:
        if lines[0:1] != '#':
            try:
                ctsdata = lines.split()
                mjd.append(float(ctsdata[0]))
                n.append(float(ctsdata[2])) 
                e.append(float(ctsdata[1]))
                u.append(float(ctsdata[3]))

                year, moy, dom = mjd2date(float(ctsdata[0]))
                dy, lastDoy = decimalYear2(year, moy, dom)
                decYr.append(dy)
            except:
                continue   

    for dfi, ls in zip(df.columns, list1):
        df[dfi] = ls
    
    cts.close()
    
    if notrend:
        mn, bn, dn  = lintrend(df.decY, df.N, dtrend=True)
        me, be, de  = lintrend(df.decY, df.E, dtrend=True)
        mu, bu, du  = lintrend(df.decY, df.U, dtrend=True)
        df = pd.DataFrame(list(zip(df.decY, dn, de, du)), columns=['decY', 'N', 'E', 'U'])
        return df
    else:
        return df
