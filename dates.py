
# leap year conditions: 1. divisibile by 4 except for century
def leapYear(year):
    """
    This functions returns if a given year is a leap year or not.
    INPUT: Year
    OUTPUT: T/F
    """
    leap = False
    if (year % 400 == 0 or year % 100 != 0 and year % 4 == 0):
        leap = True
    else:
        leap = False
    return leap

# decimal year from year and day of the year (doy)
def decimalYear1(year, doy):
    """
# Function : Calculates a decimal year
#
# Author  : Kibrom E. Abraha
#
# Inputs   : - year : e.g. 2019
#            - doy : day of year, e.g: 200
# Outputs  : - decYr  : decimal year
#          : - lastdoy : last doy of the given year
#e.g. decimalYear1(2019, 200) returns (2019.5465753424658, 365)
#----------------------------------------------------

    """

    if leapYear(year):
        lastDoy = 366
    else:
        lastDoy = 365

    decYr = year + (doy - 0.5)/lastDoy

    return decYr, lastDoy


# decimal year from year, month (moy) and day of month (dom)
def decimalYear2(year, moy, dom):
    """
# Function : Calculates a decimal year
#
# Author  : Kibrom E. Abraha
#
# Inputs   : - year : e.g. 2019
#            - moy : Month , e.g: 7 (Jul)
#            - dom : day of Month , e.g: 19 (19th of Jul)
# Outputs  : - decYr  : decimal year
#          : - lastdoy : last doy of the given year
#e.g decimalYear2(2019, 7, 19) returns (2019.5465753424658, 365)
#----------------------------------------------------
    """
    year, doy = yearmoydom2yearDoy(year, moy, dom)
    
    if leapYear(year):
        lastDoy = 366
    else:
        lastDoy = 365

    decYr = year + (doy - 0.5)/lastDoy

    return decYr, lastDoy


def decYear2yearDoy(decYear):
    """
# Function : Calculates Year and day from a decimal year
#
# Author  : Kibrom E. Abraha
#
# Inputs   : - decYear 
# Outputs  : - Year  : year
#          : - doy : doy of year
# e.g yearDoy(2019.5465753424658) returns (2019, 200)
#----------------------------------------------------
    """
    
    year = int(decYear)

    if leapYear(year):
        lastDoy = 366
    else:
        lastDoy = 365

    doy = lastDoy * (decYear - year) + 0.5
    doy = int(doy + 0.5)  # rounding it to the nearest integer
    return year, doy


def yeardoy2yearMoyDom(year, doy):
    """
# Function : Converts year, doy to year, month, dom
#
# Author  : Kibrom E. Abraha
#
# Inputs   : - Year 
#          : - doy - day of year 
# Outputs  : - year  : year
#          : - moy : month of year
#          : - dom : day of month
# e.g yeardoy2yearMoyDom(2019, 200) returns (2019, 7, 19)
#----------------------------------------------------
    """
    moy = 0
    # dic withlast day of previous month for a non-leap year
    mYear = {1: 31, 2: 59, 3: 90, 4: 120, 5: 151, 6: 181,
             7: 212, 8: 243, 9: 273, 10: 304, 11: 334, 12: 365}
    lastDoy = 365

    if leapYear(year):
        lastDoy = 366
        mYear[1] = 31
        for i in range(2, 13):
            # dic with last day of previous month for a leap year
            mYear[i] = mYear[i] + 1
# lets compute the month of year (moy) and day of month (dom)
    if doy <= 31:
        moy = 1
        dom = doy
    elif doy > lastDoy:
        print("doy out of range")
    else:
        for mnths in range(1, 12):
            if (doy <= mYear[mnths+1] and doy > mYear[mnths]):
                moy = mnths + 1
                dom = doy - mYear[mnths]
                break

    return year, moy, dom


# converts year, month, dom  to year, doy
def yearmoydom2yearDoy(year, moy, dom):
    """
# Function : converts year, month, dom  to year, doy
#
# Author  : Kibrom E. Abraha
#
# Inputs   : - year  : year
#          : - moy : month of year
#          : - dom : day of month 
#Outputs   : - Year 
#          : - doy - day of year 

# e.g yearmoydom2yearDoy(2019, 7, 19) returns (2019, 200)
#----------------------------------------------------
    """
    # dic withlast day of previous month for a non-leap year
    mYear = {1: 31, 2: 59, 3: 90, 4: 120, 5: 151, 6: 181,
             7: 212, 8: 243, 9: 273, 10: 304, 11: 334, 12: 365}
    lastDoy = 365

    if leapYear(year):
        lastDoy = 366
        mYear[1] = 31
        for i in range(2, 13):
            # dic with last day of previous month for a leap year
            mYear[i] = mYear[i] + 1
# doy
    if moy == 1:
        doy = dom
    else:
        doy = dom + mYear[moy - 1]

    return year, doy

def mjd2jd(mjd):
    """
# Function : converts MJD - Modified Julian date to Julian date
#
# Author  : Kibrom E. Abraha
#
# Inputs   : - MJD  
#          
#Outputs   : - JD 

# e.g mjd2jd(58683) returns 2458683.5
#----------------------------------------------------
    """
    jd = mjd + 2400000.5

    return jd


def jd2mjd(jd):
    """
# Function : converts JD - Julian date to MJD - Modified Julian date
#
# Author  : Kibrom E. Abraha
#
# Inputs   : - JD  
#          
#Outputs   : - MJD 

# e.g jd2mjd(2458683.5) returns 58683.0 
#----------------------------------------------------
    """
    mjd = jd - 2400000.5
    
    return mjd


def jd2date(jd):
    
    """
# Function : converts JD - Julian date to Year, month and day
#
# Author  : Kibrom E. Abraha
#
# Inputs   : - JD  
#          
# Outputs  : - year  : year
#          : - moy : month of year
#          : - dom : day of month 

# e.g jd2date(2458683.5) returns (2019, 7, 19.0)
#----------------------------------------------------
    """
    #jd = mjd2jd(mjd)
    a = int(jd + 0.5)
    b = a + 1537
    c = int((b - 122.1)/365.25)
    d = int(365.25 * c)
    e = int((b - d)/30.6001)

    f1 = jd + 0.5
    f2 = f1 - int(f1)

    dom = b - d - int(30.6001 * e) + f2
    moy = e - 1 - 12 * int(e/14)
    year = c - 4715 - int((7 + moy)/10)

    return year, moy, dom


def mjd2date(mjd):
    """
# Function : converts MJD - modified Julian date to Year, month and day
#
# Author  : Kibrom E. Abraha
#
# Inputs   : - MJD  
#          
# Outputs  : - year  : year
#          : - moy : month of year
#          : - dom : day of month 

# e.g mjd2date(58683.0) returns (2019, 7, 19.0)
#----------------------------------------------------
    """
    jd = mjd2jd(mjd)
    a = int(jd + 0.5)
    b = a + 1537
    c = int((b - 122.1)/365.25)
    d = int(365.25 * c)
    e = int((b - d)/30.6001)

    f1 = jd + 0.5
    f2 = f1 - int(f1)

    dom = b - d - int(30.6001 * e) + f2
    moy = e - 1 - 12 * int(e/14)
    year = c - 4715 - int((7 + moy)/10)

    return year, moy, dom


def date2mjd(year, moy, dom):
    """
# Function : converts Year, month and day day to MJD - modified Julian date
#
# Author  : Kibrom E. Abraha
#
#          
# Inputs  : - year  : year
#          : - moy : month of year
#          : - dom : day of month 
# Outputs   : - MJD  
# e.g date2mjd(2019, 7, 19.0) returns  58683.0
#----------------------------------------------------
    """
    if moy <= 2:
        year = year - 1
        moy = moy + 12
    mjd = int(365.25 * year) + int(30.6001 * (moy + 1)) + (dom - 679019)

    return mjd

