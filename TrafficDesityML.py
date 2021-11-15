import matplotlib.pyplot as plt
import numpy
import pandas as pd
from matplotlib import pyplot
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
def createmodel(id, city):
    filename = 'DatabyCities/'+city
    columns = ['day','interval','detid','flow','occ','error','city','speed']
    df = pd.read_csv(filename,header=0,names=columns)
    groupedbyid = df.groupby('detid')
    df_new = groupedbyid.get_group(id)
    flow = df_new['flow']
    time = []
    x = 0
    for row in df_new.itertuples():
        if row.day == '2017-05-06':
            time.append(row.interval)
        else:
            temp = row.interval + (86100 * x)
            time.append(temp)
        x+=1
    model = numpy.poly1d(numpy.polyfit(time, flow, 9))
    line = numpy.linspace(10, 1722000, 300)
    plt.scatter(time, flow)
    plt.plot(line, model(line))
    plt.show()


createmodel('06.X-2r','augsburg')
