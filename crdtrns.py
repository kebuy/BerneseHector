import numpy as np
from dates import *

def xyz2latlonh(x, y, z):
    """
# Function : converts x, y, z cartesian coordinates to latitude, 
#longitude and ellipsoidal height based on datum definition from ITRF2000
#
#
# Author  : Kibrom E. Abraha
#
#          
# Inputs  : - [x, y, z]  : cartesian coordinates in meters
#
# Outputs   : - lat, lon - latitude and longitude in radians  
#           : - h - ellipsoidal height in meters
# e.g #Ex: For a GNSS station in Ethiopia (ADIS) the x, y, z coordinates (in ITRF2014 (~WGS84)) are
#x = 4913652.58051 
#y = 3945922.82577
#z = 995383.50500
# and xyz2latlonh(x, y, z) returns
#lat = 0.15769289469756903 rad (9.0351373  deg)
#lon = 0.6765996804658367 rad (38.7663061  deg)
#h = 2439.133541136004 meters
#----------------------------------------------------
    """
    #constants
    a = 6378137.0000
    ainv = 1/a
    finv = 298.257222101
    f = 1/finv
    e2 = (2 - f) * f
    ep = np.sqrt(1 - e2)
    
    #calculate Longitude
    lon = np.arctan2(y, x)
    #Distance from polar axis
    r = np.sqrt(x**2 + y**2)
    
    #
    p = r * ainv
    absz = abs(z) * ainv
    zprime = ep * absz
    u = 2 * (zprime - e2)
    v = 2 * (zprime + e2)
    p4 = 4 * p
    p2 = 2 * p
    u3 = 3 * u
    u2 = 2 * u

    if (p < 1e-16):
        # Case 0: p = 0
        t0 = 0
    elif (u >= 0):
        # Case 1: u >= 0
        t0 = (p4 + u2) / (p4 + u3 + v)
    else:
        # Case u < 0
        if (-u > p2):
            # Case 2: t_M > 1
            t0 = p / v
        else:
            # Case 3: 0 < t_M <= 1
            tm = -u / p2
            fm = tm * ( tm * tm * (tm * p + u) + v) - p
            if (fm > 0):
                # Case 3a: f(t_M) > 0
                t0 = p / v
            else:
                # Case 3b: f(t_M) <= 0
                t0 = (p4 + u2) / (p4 + u3 + v)
    # Newton Method
    tau = t0
    for i in range (20):
        fx = p * tau**4 + u * tau**3 + v * tau - p
        if (abs(fx) < 1e-15):
            break
        
        fp = p4 * tau**3 + u3 * tau**2 + v
        dtau = -fx / fp
        tau = tau + dtau
        if (abs(dtau) < 1e-8):
            break


    tau21 = 1 + tau**2
    tau21m = 1 - tau**2
    tauep2 = 2 * ep * tau

    # After Care
    lat = np.arctan2(tau21m,tauep2)
    if (z < 0):
        lat = -lat
    
    dp = np.sqrt(tau21**2 - 4 * e2 * tau**2)
    h = a * (p * tauep2 + absz * tau21m - ep * tau21) / dp

    return lat, lon, h

def xyz2enu(x, y, z, lat, lon, radians=True):
    """
# Function : converts x, y, z cartesian coordinates to E, N, U
#
#
# Author  : Kibrom E. Abraha
#
#          
# Inputs  : - [x, y, z]  : cartesian coordinates in meters
#         : - lat, lon - latitude and longitude in radians 
#         : the function assumes lat and lon are given in radians. If they are
#           given in degrees, the variable radians=False should be used.
#
# Outputs   : [e, n, u] in meters  
#          
# e.g #Ex: For a GNSS station in Ethiopia (ADIS) the x, y, z coordinates (in ITRF2014 (~WGS84)) are
#x = 4913652.58051 
#y = 3945922.82577
#z = 995383.50500
#lat = 0.15769289469756903 rad (9.0351373  deg)
#lon = 0.6765996804658367 rad (38.7663061  deg)
#
#xyz2enu(x, y, z, lat, lon, radians=True) returns 
#e = 3274068.1842803336
#n = -3249808.592685869
#u = 4407300.600878017)
#----------------------------------------------------
    """
    #are lat and lon given in radians or degrees?
    if not radians:
        lat = lat * np.pi/180
        lon = lon * np.pi/180
        
    #initialize rotation matrix    
    Rot = np.zeros((3, 3))
    
    Rot[..., 0, 0] = -np.sin(lon)
    Rot[..., 0, 1] =  np.cos(lon)
    Rot[..., 0, 2] =  0.0
    
    Rot[..., 1, 0] = -np.sin(lat) * np.cos(lon)
    Rot[..., 1, 1] = -np.sin(lat) * np.sin(lon)    
    Rot[..., 1, 2] =  np.cos(lat)
    
    Rot[..., 2, 0] =  np.cos(lat) * np.cos(lon)
    Rot[..., 2, 1] =  np.cos(lat) * np.sin(lon)
    Rot[..., 2, 2] =  np.sin(lat)
    
    xyz = np.array([x, y, z])
    
    e, n, u = np.matmul(Rot, xyz)

    return e, n, u

def enu2xyz(n, e, u, lat, lon, radians=True):
    """
# Function : converts n, e, u coordinates to x, y, z
#
#
# Author  : Kibrom E. Abraha
#
#          
# Inputs  : - [e, n, u]  : coordinates in meters
#         : - lat, lon - latitude and longitude in radians 
#         : the function assumes lat and lon are given in radians. If they are
#           given in degrees, the variable radians=False should be used.
#
# Outputs   : [x, y, z] in meters  
#          
# e.g #Ex: For a GNSS station in Ethiopia (ADIS) the e, n, u coordinates are
#e = 3274068.1842803336
#n = -3249808.592685869
#u = 4407300.600878017)
and 
#lat = 0.15769289469756903 rad (9.0351373  deg)
#lon = 0.6765996804658367 rad (38.7663061  deg)
#
#enu2xyz(e, n, u, lat, lon, radians=True) returns 
#x = 4913652.58051 
#y = 3945922.82577
#z = 995383.50500
#----------------------------------------------------
    """
    if not radians:
        lat = lat * np.pi/180
        lon = lon * np.pi/180

    Rot = np.zeros((3, 3))
    
    Rot[..., 0, 0] = -np.sin(lon)
    Rot[..., 0, 1] =  np.cos(lon)
    Rot[..., 0, 2] =  0.0
    
    Rot[..., 1, 0] = -np.sin(lat) * np.cos(lon)
    Rot[..., 1, 1] = -np.sin(lat) * np.sin(lon)    
    Rot[..., 1, 2] =  np.cos(lat)
    
    Rot[..., 2, 0] =  np.cos(lat) * np.cos(lon)
    Rot[..., 2, 1] =  np.cos(lat) * np.sin(lon)
    Rot[..., 2, 2] =  np.sin(lat)


    neu = np.array([n, e, u])
    
    x, y, z = np.matmul(R.transpose(), neu)

    return x, y, z


def lintrend(x, y, dtrend=False):
    """
# Function : Fits 'y = mx + b' (linear) model using leastsquare 
#
#
# Author  : Kibrom E. Abraha
#
# 
# inputs ---    x : independet variable 
#               y : dependent variable
# outputs ---   default returns m and b : Coefficients of the linear fit model (slope and bias)
#               - detrended values can be printed if variable detrend=True is used
#-------------------------------------------------------------------------------  
    """
    

    m = 0
    b = 0
    
    xLen  = len(x)
    xSum  = np.sum(x)
    ySum  = np.sum(y)
    xySum = np.sum(x*y)
    xxSum = np.sum(x**2)
    det   = xLen*xxSum - xSum**2


    m = (xLen*xySum  - xSum*ySum)  / det
    b = (xxSum*ySum - xSum*xySum) / det
    
    if dtrend:
        dy = y - (m*x + b)
        return m, b, dy
    else:
        return m, b
