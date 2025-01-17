'''
Program name : stats_calculation.py
Author : Manjunath R B

This program Calcutes the statistics and generate statistical features.
The program calculates statistics per class per feature basis.
The program accepts three command line arguments
1. input file name
2. output file name
3. Quartile step value

The stats are calculated with and without duplicates.
'''

import pandas as pd
import numpy as np
import  sys
import matplotlib.pyplot as plt

#filename ='C:\\Users\\manjuna\\Desktop\\netmate_files\\CTU-files_9\\csv_files\\42-1\\CTU-IoT-Malware-Capture-42-1.csv'

in_filename = sys.argv[1]
out_filename = sys.argv[2]
perc_step = int(sys.argv[3])
# Reading data from CSV(ignore columns such as srcip,srcport,dstip,dtsport,proto)
df = pd.read_csv(in_filename, index_col=0, usecols=lambda column: column not in ['srcip', 'srcport ', 'dstip ', 'dstport ', 'proto '])

newList = list(range(0, 100, perc_step))
perc = [i/100 for i in newList]
print(perc)
print("Printing the shape of the dataset\n")
print(df.shape)
print("Printing the index columns\n")
print(df.columns)
print("printing Classes from the CSV\n")
print(df['local-label'].unique().tolist())

#separate out data based on per class basis
dict_of_classes = dict(tuple(df.groupby("local-label")))

# for calculating statistics per class per feature with duplicates per column.
per_class_data_with_dup=pd.DataFrame()
for key,value in dict_of_classes.items():
    per_class_stats_data_with_dup = pd.DataFrame(value)
    i = 0
    while i < len(per_class_stats_data_with_dup.columns) -2:
        #get per column stats using iloc and store with column name as index     
        per_class_data_with_dup[per_class_stats_data_with_dup.columns[i]]=per_class_stats_data_with_dup.iloc[:,i].describe(percentiles = perc)
        per_class_data_with_dup.loc['range',per_class_stats_data_with_dup.columns[i]] = per_class_data_with_dup.loc['max',per_class_stats_data_with_dup.columns[i]] - per_class_data_with_dup.loc['min',per_class_stats_data_with_dup.columns[i]]
        per_class_data_with_dup.loc['midrange',per_class_stats_data_with_dup.columns[i]] = (per_class_data_with_dup.loc['max',per_class_stats_data_with_dup.columns[i]] + per_class_data_with_dup.loc['min',per_class_stats_data_with_dup.columns[i]])/2
        if per_class_data_with_dup.loc['mean',per_class_stats_data_with_dup.columns[i]] != 0:
            per_class_data_with_dup.loc['coefVar',per_class_stats_data_with_dup.columns[i]] = per_class_data_with_dup.loc['std',per_class_stats_data_with_dup.columns[i]] / per_class_data_with_dup.loc['mean',per_class_stats_data_with_dup.columns[i]]
        else:
            per_class_data_with_dup.loc['coefVar',per_class_stats_data_with_dup.columns[i]] = 0
        per_class_data_with_dup.loc['count_of_min-(mean-sd)',per_class_stats_data_with_dup.columns[i]]= np.count_nonzero(per_class_stats_data_with_dup.iloc[:,i].between(per_class_data_with_dup.loc['min',per_class_stats_data_with_dup.columns[i]], (per_class_data_with_dup.loc['mean',per_class_stats_data_with_dup.columns[i]]- per_class_data_with_dup.loc['std',per_class_stats_data_with_dup.columns[i]])).values)
        per_class_data_with_dup.loc['count_of_(mean-sd)-mean',per_class_stats_data_with_dup.columns[i]]= np.count_nonzero(per_class_stats_data_with_dup.iloc[:,i].between((per_class_data_with_dup.loc['mean',per_class_stats_data_with_dup.columns[i]]- per_class_data_with_dup.loc['std',per_class_stats_data_with_dup.columns[i]]),per_class_data_with_dup.loc['mean',per_class_stats_data_with_dup.columns[i]]).values)
        per_class_data_with_dup.loc['count_of_mean-(mean+sd)',per_class_stats_data_with_dup.columns[i]]= np.count_nonzero(per_class_stats_data_with_dup.iloc[:,i].between(per_class_data_with_dup.loc['mean',per_class_stats_data_with_dup.columns[i]], (per_class_data_with_dup.loc['mean',per_class_stats_data_with_dup.columns[i]] + per_class_data_with_dup.loc['std',per_class_stats_data_with_dup.columns[i]])).values)
        per_class_data_with_dup.loc['count_of_std-max',per_class_stats_data_with_dup.columns[i]]= np.count_nonzero(per_class_stats_data_with_dup.iloc[:,i].between(per_class_data_with_dup.loc['std',per_class_stats_data_with_dup.columns[i]], per_class_data_with_dup.loc['max',per_class_stats_data_with_dup.columns[i]]).values)
        i = i +1
    # add label column at the end
    per_class_data_with_dup['label'] = key
    per_class_data_with_dup.to_csv(out_filename, mode='a')

# for calculating statistics per class per feature after removing duplicates per column.
per_class_data_without_dup = pd.DataFrame()
for key,value in dict_of_classes.items():
    per_class_stats_data_without_dup = pd.DataFrame(value)
    i = 0
    while i < len(per_class_stats_data_without_dup.columns) -2:
        #get per column stats using iloc and store with column name as index   
        per_class_data_without_dup[per_class_stats_data_without_dup.columns[i]]=per_class_stats_data_without_dup.iloc[:,i].drop_duplicates().describe(percentiles = perc)
        per_class_data_without_dup.loc['range',per_class_stats_data_without_dup.columns[i]] = per_class_data_without_dup.loc['max',per_class_stats_data_without_dup.columns[i]] - per_class_data_without_dup.loc['min',per_class_stats_data_without_dup.columns[i]]
        per_class_data_without_dup.loc['midrange',per_class_stats_data_without_dup.columns[i]] = (per_class_data_without_dup.loc['max',per_class_stats_data_without_dup.columns[i]] + per_class_data_without_dup.loc['min',per_class_stats_data_without_dup.columns[i]])/2
        if per_class_data_without_dup.loc['mean',per_class_stats_data_without_dup.columns[i]] != 0:
            per_class_data_without_dup.loc['coefVar',per_class_stats_data_without_dup.columns[i]] = per_class_data_without_dup.loc['std',per_class_stats_data_without_dup.columns[i]] / per_class_data_without_dup.loc['mean',per_class_stats_data_without_dup.columns[i]]
        else:
            per_class_data_without_dup.loc['coefVar',per_class_stats_data_without_dup.columns[i]] = 0		
        per_class_data_without_dup.loc['count_of_min-(mean-sd)',per_class_stats_data_without_dup.columns[i]]= np.count_nonzero(per_class_stats_data_without_dup.iloc[:,i].drop_duplicates().between(per_class_data_without_dup.loc['min',per_class_stats_data_without_dup.columns[i]], (per_class_data_without_dup.loc['mean',per_class_stats_data_without_dup.columns[i]]- per_class_data_without_dup.loc['std',per_class_stats_data_without_dup.columns[i]])).values)
        per_class_data_without_dup.loc['count_of_(mean-sd)-mean',per_class_stats_data_without_dup.columns[i]]= np.count_nonzero(per_class_stats_data_without_dup.iloc[:,i].drop_duplicates().between((per_class_data_without_dup.loc['mean',per_class_stats_data_without_dup.columns[i]]- per_class_data_without_dup.loc['std',per_class_stats_data_without_dup.columns[i]]),per_class_data_without_dup.loc['mean',per_class_stats_data_without_dup.columns[i]]).values)
        per_class_data_without_dup.loc['count_of_mean-(mean+sd)',per_class_stats_data_without_dup.columns[i]]= np.count_nonzero(per_class_stats_data_without_dup.iloc[:,i].drop_duplicates().between(per_class_data_without_dup.loc['mean',per_class_stats_data_without_dup.columns[i]], (per_class_data_without_dup.loc['mean',per_class_stats_data_without_dup.columns[i]] + per_class_data_without_dup.loc['std',per_class_stats_data_without_dup.columns[i]])).values)
        per_class_data_without_dup.loc['count_of_std-max',per_class_stats_data_without_dup.columns[i]]= np.count_nonzero(per_class_stats_data_without_dup.iloc[:,i].drop_duplicates().between(per_class_data_without_dup.loc['std',per_class_stats_data_without_dup.columns[i]], per_class_data_without_dup.loc['max',per_class_stats_data_without_dup.columns[i]]).values)
        i = i +1
    # add label column at the end
    per_class_data_without_dup['label'] = key
    per_class_data_without_dup.to_csv(out_filename, mode='a')
print("DONE\n")