import urllib
tempsurl = "http://www.wrh.noaa.gov/pqr/climate/PDXtemp.txt"
#assign a name for the file on hard drive
temps_fn = "temperatures.txt"
#create file
urllib.urlretrieve(tempsurl, filename=temps_fn)
#open file into python
temps = open(temps_fn)
#read each line into a list
temps = temps.readlines()
#remove header Note: Only know this from examining file
temps = temps[7:]
#Most of the file is space dl, except the first and second column run together in some
#case. Need to add a space after the year in order to sep
def insert_space(string, integer):
    return string[0:integer] + ' ' + string[integer:]
#apply to list    
for i in range(len(temps)):
    temps[i] = insert_space(temps[i], 4)

import pandas as pd
from pandas import DataFrame
from pandas import Series
#a lot of trial and error went into this next section. Q: Not totally sure what's happening. 
#This helped: http://stackoverflow.com/questions/17116814/pandas-how-do-i-split-text-in-a-column-into-multiple-columns
temps = Series(temps)
#get rid of the underlines
temps = temps.drop(temps.index[[1]])
#create a data frame with one column
temps = DataFrame(temps, columns=['col'])
#create an object with a list of list (Q: Why does this return list of list? Can this be done with values?) for first row
col_n=list(temps.ix[0].str.split())
#split columns of dataframe and make col_n the column indexes
temps = pd.DataFrame(list(temps.col.str.split()), columns=names[0])
#drop the duplicate column name row
temps = temps.drop(temps.index[0])
#this would strip white space, but I think it's unnecessary: temps.apply(lambda x: x.str.strip())
#Change Ms to missing values
import numpy as np
temps.replace('M', np.nan, inplace=True)
#create a column with TX vs TN, change MO so is actually Month
temps['Lvl'] = Series(temps['MO']).str[-2:]
temps['MO'] = Series(temps['MO']).str[:-2]
#make year and month indexes (Q: Added Lvl as well does this shape make sense?)
temps = temps.set_index(['YR','MO','Lvl'])

#Let's try graphing!
import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
