import pandas as pd
import numpy as np
import sys
import os

#
def computeCTSdiff(file1, file2):
    """
# Function : Computes coordinate differences between two hector input (.enu) files
#            which are created by cts2hector. This function should be modified if input file format is different.
#
#
#
# Author  : Kibrom E. Abraha
#
#
#Inputs: file1, file2 -- file names (including the file path) of the two files res
#                      - The first file (file1) will be used as a reference
#                        when cts differences are computed computed.
#
#Outputs: Coordinate differences and statistics of the differences
#
#-------------------------------------------------------------------------------
    """
#define variables
    dicts = {}

# time series difference files and differenced statistics will be stored
    enu_diffs = './ctsDifferences/'
    if not os.path.isdir(enu_diffs):
        os.mkdir(enu_diffs)

    #compute differences
    for i, files in enumerate((file1, file2)):
        station = os.path.basename(files)
        stndf = station[0:4] + str(i)


        try:
            f = open(files, 'r')
        except FileNotFoundError:
            print ("There is no {} file \n".format(files))
            sys.exit(0)


        mjd, e, n, u = [[] for i in range(4)]
        columns = ['mjd', 'E-', 'N-', 'U-']
        lst = [mjd, e, n, u]
        dfs = pd.DataFrame(columns=columns)

        for lines in f:
            if lines[0:1] != '#':
                try:
                    ctsdata = lines.split()

                except:
                    continue

                for i, lt in enumerate(lst):
                    lt.append(float(ctsdata[i]))

        for dfi, ls in zip(dfs.columns, lst):
            dfs[dfi] = ls
        dicts[stndf] = dfs

        f.close()

    for keys in dicts.keys():
        df1 = dicts[keys]

    suffix = list(dicts.keys())

    df1, df2 = [dicts[keys] for keys in dicts.keys()]
    mdf = pd.merge(df1, df2, how='outer', on='mjd', validate='many_to_one',
                   suffixes=suffix)

    mdf['e_diff'] = mdf['E-'+suffix[0]] - mdf['E-'+suffix[1]]
    mdf['n_diff'] = mdf['N-'+suffix[0]] - mdf['N-'+suffix[1]]
    mdf['u_diff'] = mdf['U-'+suffix[0]] - mdf['U-'+suffix[1]]

    diffdf = mdf[['e_diff', 'n_diff', 'u_diff']]
    mdfstat = diffdf.describe()

    #drop NaN values (unmatched lines will have NaNs)
    mdf.dropna(inplace=True)
    mdf.to_csv(enu_diffs + suffix[0] + '_' + suffix[1] + '_ctsdiff.csv', sep='\t')
    mdfstat.to_csv(enu_diffs + suffix[0] + '_' + suffix[1] + '_ctsdiff_statistics.csv', sep='\t')

##Main program begins here

# .enu files are stored in
# all .enu files for cts differences can be stored in one directory.
#Multiple directories can be used,
#or example, if cts differences are to be computed between the same stations of different solution types


if (len(sys.argv)<3 or len(sys.argv)>3):
    print('\n')
    print ('>> Nope! :( run it correctly \n ')
    print('>> Check your input parameters. Use Script as follows: \n ')
    print('>> compute_timeseries_differences stnlist1 stnlist2 \n')

    sys.exit()
else:
    stnlist1 = sys.argv[1]
    stnlist2 = sys.argv[2]

enu_files1 = './hectorInputs/'
enu_files2 = './hectorInputs/'


#read station list file1
stn_list1 = []

try:
    f1 = open(stnlist1, 'r')
except FileNotFoundError:
    print ("There is no {} file \n".format(stnlist1))
    sys.exit(0)

for lines in f1:
    stn_list1.append(lines.split()[0])

f1.close()

#read station list file1
stn_list2 = []

try:
    f2 = open(stnlist2, 'r')
except FileNotFoundError:
    print ("There is no {} file \n".format(stnlist2))
    sys.exit(0)

for lines in f2:
    stn_list2.append(lines.split()[0])

f2.close()

#compute cts differences between stations in station list files
for allstns1 in stn_list1:
    for allstns2 in stn_list2:

        stn1 = enu_files1 + allstns1 + '.enu'
        stn2 = enu_files2 + allstns2 +'.enu'

        if os.path.isfile(stn1) and os.path.isfile(stn2):
            print ("Computing cts differences between {} and {} stations".format(allstns1, allstns2))
            computeCTSdiff(stn1, stn2)
        else:
            if not os.path.isfile(stn1):
                print ("File {} is not available".format(stn1))
                print ("cts difference between {} and {} stations is not computed".format(allstns1, allstns2))
            if not os.path.isfile(stn2):
                print ("File {} is not available".format(stn2))
                print ("cts difference between {} and {} stations is not computed \n".format(allstns1, allstns2))
