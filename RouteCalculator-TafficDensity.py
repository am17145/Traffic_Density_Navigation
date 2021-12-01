import math
import sys
from datetime import datetime
import numpy as np
import pandas as pd
from libpysal.weights import lat2W
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

#This creates a new column know as new id to help simplify the traversal aspect ex. detid 06.X-2li -> 1
filename = 'DatabyCities/augsburg'
columns = ['day', 'interval', 'detid', 'flow', 'occ', 'error', 'city', 'speed']
df = pd.read_csv(filename, header=0, names=columns)
newIds = []
temp = pd.unique(df.detid)
prefix = ''
offset = 0
p1 = 0
p2 = 0
for j in df.detid:
    if temp[p1] == j:
        p2 += 1
    else:
        p1 += 1
    newIds.append(prefix + str(p1 + offset))
df['newIds'] = newIds

#This creates an adjacency list of a grid of points our traffic pattern is a simple grid
grid = math.ceil(math.sqrt(len(pd.unique(df.detid))))
g = lat2W(grid,grid)

#This method gets the flow(repersents traffic density) to use as the weight for the tree search
def GetFlow(id,currentinteval):
    #This creates a temporary dataframe only using the data from the selected detector (id)
    groupedbyid = df.groupby('newIds')
    df_new = groupedbyid.get_group(str(id))
    flow = []
    interval = []
    count = 0
    for row in df_new.itertuples():
        interval.append(row.interval + (86100 * count))
        flow.append(row.flow)
        count+=1

    #This is the formula for sinusoidal equations
    def sinfunction(x, A, B, C, D):
        y = A * np.sin(B * x + C) + D
        return y

    #This finds the values needed in order to best fit the our model
    initial = (15, 100000, 5, 20)
    popt, pcov = curve_fit(sinfunction, interval, flow,initial)

    #This calculates the weight using of the selected id at the current moment and the sinusoidal regression
    weight = popt[0]*np.sin(popt[1]*currentinteval+popt[2])+popt[3]
    return weight

#This gets the current system time and coverts it to seconds(interval) to match the data used in the data-set
def GetCurrentInterval():
    time = datetime.now().strftime('%H:%M:%S')
    hh, mm, ss = time.split(':')
    CurrentInterval = (int(hh) * 3600 + int(mm) * 60 + int(ss))
    return CurrentInterval

#This is a tree search to selected the path with the least traffic density
def TreeSearch(startID,endID):
    path = []
    currentID = int(startID)
    path.append(startID)
    while currentID != endID:
        neighbors = [key for key, value in g[currentID].items()]
        min = float('inf')
        for x in neighbors:
            if (x == endID) or (GetFlow(x,GetCurrentInterval()) < min):
                min = GetFlow(x,GetCurrentInterval())
                currentID = x
        path.append(currentID)
    return path
#Launch using the two command line prompts for the start and end ids
print(TreeSearch(int(sys.argv[1]),int(sys.argv[2])))
