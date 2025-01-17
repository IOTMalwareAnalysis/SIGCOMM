import csv

# In put file		
in_file = "Path to conf.label.csv file which is obtained from step2"
# Output file
out_file = "Path to netamtefiltered.csv file which is obtained from step 3"
result_file = "Path to store result.csv file"


print("Input files are \n")
print(in_file,"\n")
print(out_file,"\n")

# List to store the resulting rows

new_rows_list = []

inFileCount = 0
outFileCount = 0
resultFileCount = 0

copyOnce = 1

# Open both the netmate and lablled files in read mode
# Have a nested loop to scan each entry and check for the first four
# columns as they have the 
# required data to match. If all of them are matching then label it as
# 'PartOfAHorizontalPortScan'. This list will be written
# to result.csv file


with open(in_file,'r') as csvinput:
    with open(out_file, 'r') as csvoutput:
        
        readerIn = csv.reader(line.replace('\0','') for line in csvinput)
        readerOut = list(csv.reader(line.replace('\0','') for line in csvoutput))
        
        #row_out = next(readerOut)
        #new_rows_list.append(row_out)
        
        for rowInput in readerIn:
            inFileCount += 1
            for rowOutput in readerOut:


                if(copyOnce):
                    # print(rowOutput)
                    rowOutput[44] = 'unknown'
                    new_rows_list.append(rowOutput)
                    outFileCount += 1
                    # print(new_rows_list)

                
                if rowInput[0] == rowOutput[0] and rowInput[1] == rowOutput[1] and rowInput[2] == rowOutput[2] and rowInput[3] == rowOutput[3]:
                    # readerOut.append('PartOfAHorizontalPortScan')

                    # Change the field and rowOutput list indexes to match the label column accordingly
					# Let us say label is 10 th column in netamte file then the field will be field[:9]

                    for field in new_rows_list:
                        if field[:9] == rowOutput[:9]:
                            field[44] = 'PartOfAHorizontalPortScan'
                            print("Voila!!! Matched the condtion.. label unknown is changed to PartOfAHorizontalPortScan \n")
                            break
                    # print(new_rows_list)
                    resultFileCount += 1


            copyOnce = 0
                    

        print("Computation is Done \n")


print("Closing the input files...\n")
csvinput.close()
csvoutput.close()


print("Write the results to - ",result_file)
print("\n")

# Do the writing
file2 = open(result_file, 'w')
writer = csv.writer(file2, lineterminator='\n')
writer.writerows(new_rows_list)
file2.close()

print("Writing is done and the file is saved\n")

print("========= File stats ============\n")
print("Number of lines in netmate file\n ", outFileCount)
print("Number of lines in port scan file \n", inFileCount)
print("Unkown labels are \n", outFileCount - resultFileCount)
print("Total number of PartOfAHorizontalPortScan attacks \n", resultFileCount)

print("Exiting!!!")
