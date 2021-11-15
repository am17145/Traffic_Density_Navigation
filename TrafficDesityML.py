import matplotlib.pyplot as plt
import numpy
import pandas as pd
from matplotlib import pyplot
from sklearn.model_selection import train_test_split

filename = 'DatabyCities/augsburg'
columns = ['day','interval','detid','flow','occ','error','city','speed']
df = pd.read_csv(filename,header=0,names=columns)
groupedbyid = df.groupby('detid')
df_new = groupedbyid.get_group('06.X-2li')
model = numpy.poly1d(numpy.polyfit(df_new['interval'],df_new['flow'],3))
line = numpy.linspace(20,90000,175)
plt.scatter(df_new['interval'],df_new['flow'])
plt.plot(line,model(line))
plt.show()


