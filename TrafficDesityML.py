import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import pyplot
filename = 'DatabyCities/augsburg'
columns = ['day','interval','detid','flow','occ','error','city','speed']
df = pd.read_csv(filename,header=0,names=columns)
plt.plot(df['interval'],df['flow'],color='red',marker='o')
detid = []
for
plt.show()