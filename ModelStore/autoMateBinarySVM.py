"""

Program name: autoMateBinarySVM.py
Author: Venkatesh Madi

Program to intelligently perform binary SVM modelling on different combination
of labels
E.g.: If a Dataset (.csv file) has 3 different labels 'Benign',
'MalwareActivity' and 'MalwareAttack' then the possible combinations will be
('Benign', 'MalwareActivity'), ('Benign', 'MalwareAttack') and
('MalwareActivity', 'MalwareAttack')


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

print("====================== Program started =========================\n")
print ("Start time :",datetime.now().strftime("%H:%M:%S"))
print("\n")


# If you want to include any further operations to SVM modeling
# write the logic in this function

def performSVM(train_set):
    X = train_set[:, [1,2,3,4]]
    print ("dataset: \n",X)
    Y = train_set[:,0]
    print ("labels: \n",Y)

    X_train = X
    y_train = Y


    model = svm.SVC(kernel='linear')

    print("Created linear model, started linear fit on given dataset")

    print ("**********Start time *********** :",datetime.now().strftime("%H:%M:%S"))
    print("\n")
    model.fit(X_train, y_train)
    print ("**********End time *********** :",datetime.now().strftime("%H:%M:%S"))
    print("\n")

    print("Created linear model")
    print("\n")

    y_pred = model.predict(X_train)
    print("Dataset validation report : \n" ,classification_report(y_train, y_pred))
    print("\n")


    conf_mat = confusion_matrix(y_train, y_pred)
    print("Daset validation confusion-matrix : \n",conf_mat)
    print("\n")
    print("-------------------- Done ------------------------\n")


# Input file path

inputFile = 'C:/Users/madiv/Documents/sigcom2020/AutomateSVM/testAutoMate.csv'

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
    

listCombination = list(combinations(diffLables,2))

print("\nCombinations from unique labels are \n")
print(listCombination)


# Read the file again to 
with open(inputFile,'r') as csvinput:

    # Note that reader object is present as a list so that it does not
    # exhausted when looping through the object

    readerIn = list(csv.reader(line.replace('\0','') for line in csvinput))
    
    # Get combination from the unique labels
    # Check whether this label is part of the current object
    # If present append to the list

    for item in listCombination:
        train_set = []
        for data in readerIn:
            if data[0] == item[0] or data[0] == item[1]:
                train_set.append(data)
        print("========================")
        print("Perform SVM modeling on ", item)
        print("========================\n")
        trainData = np.array(train_set)
    
        performSVM(trainData)

print("\n====================== Program Ended =========================\n")
print ("End time :",datetime.now().strftime("%H:%M:%S"))
