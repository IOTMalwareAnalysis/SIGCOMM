"""

Program name: predictLabelBinarySVM.py
Author: Venkatesh Madi

Program to intelligently perform binary SVM modelling on different combination
of labels
E.g.: If a Dataset (.csv file) has 3 different labels 'Benign',
'MalwareActivity' and 'MalwareAttack' then the possible combinations will be
('Benign', 'MalwareActivity'), ('Benign', 'MalwareAttack') and
('MalwareActivity', 'MalwareAttack')

For each combination SVM modelling is performed and the predicted label
is appended in each iteration.

"""

import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import csv
from itertools import combinations 
from sklearn.preprocessing import MinMaxScaler
from pandas.plotting import scatter_matrix
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import itertools


print("====================== Program started =========================\n")
print ("Start time :",datetime.now().strftime("%H:%M:%S"))
print("\n")


# List to store the all the rows present in the input data set
outList = []

# List to store the rows after performing SVM modelling
new_rows_list = []

# If you want to include any further operations to SVM modeling
# write the logic in this function

def performSVM(train_set, index):
    X = train_set[:, [1,2,3,4,5,6,7,8]]
    inputValue = X.tolist()
    #print ("dataset: \n",X)
    Y = train_set[:,0]
    #print ("labels: \n",Y)

    X_train = X
    y_train = Y


    model = svm.SVC(kernel='linear',probability=True)

    print("Created linear model, started linear fit on given dataset")

    print ("**********Start time *********** :",datetime.now().strftime("%H:%M:%S"))
    print("\n")
    model.fit(X_train, y_train)
    print ("**********End time *********** :",datetime.now().strftime("%H:%M:%S"))
    print("\n")

    print("Created linear model")
    print("\n")

    y_pred = model.predict(X_train)
    labelPre = y_pred.tolist()
    
    y_probability = model.predict_proba(X_train)
    probability = y_probability.tolist()
    print("------------------")
    print(probability)
    
    for num in range(len(labelPre)):
        compareIndex = inputValue[num]
        Label = labelPre[num]
        probIndex = probability[num]
        
        for field in outList:
            if compareIndex[0] == field[1] and compareIndex[1] == field[2] and compareIndex[2] == field[3] and compareIndex[3] == field[4] and \
                compareIndex[4] == field[5] and compareIndex[5] == field[6] and compareIndex[6] == field[7] and compareIndex[7] == field[8]:
                    field[index] = Label
                    field[index+1] = probIndex
                    new_rows_list.append(field)
                    break
    
    print("Dataset validation report : \n" ,classification_report(y_train, y_pred))
    print("\n")


    conf_mat = confusion_matrix(y_train, y_pred)
    print("Daset validation confusion-matrix : \n",conf_mat)
    print("\n")
    print("-------------------- Done ------------------------\n")


# Input file path

# Assumption is that the input file has "Label" as the first column followed by
# 4 different packet lengths. Also, 3 other columns should be present to
# append the predicted labels

inputFile = 'C:/Users/madiv/Documents/sigcom2020/AutomateSVM/masterDataSet.csv'

# Result file path

result_file = 'C:/Users/madiv/Documents/sigcom2020/AutomateSVM/logProbability.csv'

# List to store unique labels
diffLables = []

# List to store combinations generated from unique labels
listCombination = []


# Open the input file. Append the unique labels to 'diffLables'
with open(inputFile,'r') as csvinput:
    readerIn = csv.reader(line.replace('\0','') for line in csvinput)
    
    # Get unique labels out of the input csv file
    
    for rowInput in readerIn:
        if rowInput[0] != 'Label' and rowInput[0] not in diffLables:
            diffLables.append(rowInput[0])

    print("\nUnique labels present in the data set are \n")
    print(diffLables)

# print(outList)

listCombination = list(combinations(diffLables,2))

print("\nCombinations from unique labels are \n")
print(listCombination)

# Read the file again to 
with open(inputFile,'r') as csvinput:

    # Note that reader object is present as a list so that it does not
    # exhausted when looping through the object

    readerIn = list(csv.reader(line.replace('\0','') for line in csvinput))
    
    # By default every predicted column will be "NA" before prediction

    for rowInput in readerIn:
        rowInput[9] = rowInput[11] = rowInput [13] = rowInput [15] = "NA"
        outList.append(rowInput)
    
    #print(outList)
    
    # Get combination from the unique labels
    # Check whether this label is part of the current object
    # If present append to the list
    
    Index = int(9)

    for item in listCombination:
        train_set = []
        for data in readerIn:
            if data[0] == item[0] or data[0] == item[1]:
                train_set.append(data)
        print("========================")
        print("Peform SVM modeling on ", item)
        print("========================\n") 
        trainData = np.array(train_set)
    
        performSVM(trainData, Index)
        Index += 2

    for data in readerIn:
        #print("@@@@@@@@@@@@22222")
        #print(data)
        if data[0] != 'Label':
            train_set.append(data)
        #Index += 1 
        trainData = np.array(train_set)
    print("===================================")
    print("Peform SVM modeling on all the data")
    print("===================================\n")
    performSVM(trainData, 15)

print("\n====================== Program Ended =========================\n")
print ("End time :",datetime.now().strftime("%H:%M:%S"))


print("Closing the input file...\n")
csvinput.close()

# Remove the duplicates rows which would be created during the prediction

new_rows_list.sort()
new = list(new_rows_list for new_rows_list,_ in itertools.groupby(new_rows_list))

for item in new:
    #print(item)
    benign = mattack = mactivity = 0

    for i in range(9,16):
        if i%2 != 0:
            if item[i] == 'Benign':
                benign += 1
            elif item[i] == 'MalwareActivity':
                mactivity += 1
            elif item[i] == 'MalwareAttack':
                mattack += 1

    if benign >= 2:
        item[17] = 'Benign'
    elif mactivity >= 2:
        item[17] = 'MalwareActivity'
    elif mattack >= 2:
        item[17] = 'MalwareAttack'

#outList = my_function(outList)

# header  = ["Label","mean_fpktl","std_fpktl","mean_bpktl","std_bpktl","fpro","fvar","bpro","bvar","Predicted Label Model Benign vs Malware Attack","Probability Benign vs Malware Attack","Predicted Label Model Benign vs Activity","Probability Benign vs Activity","Predicted Label Model Malware Attack vs Activity","Probability Malware Attack vs Activity","Predict All","Probability All","Majority"]

#finalList = header + new

#print(finalList)

print("Write the results to - ",result_file)
print("\n")

# Do the writing
file2 = open(result_file, 'w')
writer = csv.writer(file2, lineterminator='\n')
writer.writerows(new)
file2.close()