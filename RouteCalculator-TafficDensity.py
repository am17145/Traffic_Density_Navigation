import math
from datetime import datetime

import numpy as np
import pandas as pd
from libpysal.weights import lat2W
from scipy.optimize import leastsq, curve_fit

filename = 'DatabyCities/augsburg'
columns = ['day', 'interval', 'detid', 'flow', 'occ', 'error', 'city', 'speed']
df = pd.read_csv(filename, header=0, names=columns)
newIds = []
temp = pd.unique(df.detid)
prefix = 's '
offset = 1
p1 = 0
p2 = 0
for j in df.detid:
    if temp[p1] == j:
        p2 += 1
    else:
        p1 += 1
    newIds.append(prefix + str(p1 + offset))
df['newIds'] = newIds
gridsize = math.sqrt(len(pd.unique(df.detid)))
gridsize += 1
g = lat2W(4,4)
g.neighbors

def GetFlow(id,currentinteval):
    groupedbyid = df.groupby('newIds')
    df_new = groupedbyid.get_group(id)
    flow = []
    interval = []
    count = 0
    for row in df_new.itertuples():
        interval.append(row.interval)
        flow.append(row.flow)
        count+=1

    def function(x, A, b, phi, c):
        y = A * np.sin(b * x + phi) + c
        return y

    popt, pcov = curve_fit(function, interval, flow)
    weight =  popt[0]*np.sin(popt[1]*currentinteval+popt[2])+popt[3]
    return weight

def GetCurrentInterval():
    time = datetime.now().strftime('%H:%M:%S')
    hh, mm, ss = time.split(':')
    CurrentInterval = (int(hh) * 3600 + int(mm) * 60 + int(ss))
    return CurrentInterval
GetFlow('s 1',GetCurrentInterval())
