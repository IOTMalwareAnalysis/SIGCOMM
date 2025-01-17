import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns

import matplotlib.pyplot as plt
%matplotlib inline


in_filename = sys.argv[1]
#in_filename = 'UniqueDataSet.csv'
list_columns = ['mean_fpktl ', 'std_fpktl ', 'mean_bpktl ', 'std_bpktl ', 'Label']
list_classes = ['MalwareActivity', 'MalwareAttack', 'Benign']
df = pd.read_csv(in_filename)

#df1 = df.loc[:, ['mean_fpktl ','std_fpktl ', 'mean_bpktl ', 'std_bpktl ', 'Label ']]
df.head()
print(df.head())
#separate out data based on per class basis

a = df.loc[df['Label'] !='Label']

print("printing Classes from the CSV\n")
print(a['Label'].unique().tolist())

subset1 = df[df.Label == 'MalwareActivity']
subset2 = df.loc[df['Label'] == 'MalwareAttack']
subset3 = df.loc[df['Label'] == 'Benign']

print("printing subsets")
labellist = [subset1, subset2, subset3]
for ele, category in zip(labellist, list_classes):
    print(ele)
    series = ele.iloc[:, 0:4].values
    my_title = "Elbow Method for K-means clustering for {}".format(category) 
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(1,10), title=my_title)

    visualizer.fit(series)        # Fit the data to the visualizer
    visualizer.show()        # Finalize and render the figure
    





