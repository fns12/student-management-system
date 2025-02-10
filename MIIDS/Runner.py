import numpy as np
import csv
import pandas as pd
from tabulate import tabulate

class Subject:
    def __init__(self,name,abbrev,teacher,credit_hrs):
        self.name = name
        self.abbrev = abbrev
        self.teacher = teacher
        self.credit_hrs = credit_hrs

def open_csvfile():
    data= []
    with open('studentInfo.csv','r') as csvfile:
        file_reader = csv.reader(csvfile,delimiter=',') #, represents next column
        for row in file_reader:
            data.append(row)
    data = np.array(data)
    return data

def data_to_CSV():
   global data
   #OPTION 1 :use numpy array
   np.savetxt('studentInfo.csv', data, delimiter=',', fmt='%s', comments="")
   print("data saved")

   # OPTION 2:Convert NumPy array to pandas DataFrame
   # df = pd.DataFrame(data)

   # Save DataFrame to CSV
   # df.to_csv('studentInfo.csv', index=False, header=True)


def getRollNumber():
    global data
    roll_No = int(input("Enter Roll no:")) 
    found = False
    for i in range(1,len(data)):
        if int(data[i][0]) == roll_No:
            found = True
            return i
    if not found:
        return -1  

def getSubject():
        found = False
        subj = input("Enter subject: ")
        for subject in Subject_list:
            if subject.name== subj or subject.abbrev == subj :
                subj = subject
                found =  True
                return subj
        if not found:
            print("Invalid subject name.")
            return -1
        
def marksAddded():
    global data
    subj = getSubject()
    while subj==-1:
        subj = getSubject()
    
    try:
       for i in range(10):
            if data[0][i]== subj.name or data[0][i]== subj.abbrev:
                return i

    except IndexError:
            print("subject marks not added.")
            return -1
    
def isValid(subj):
    global data
    try:
       for i in range(10):
            if data[0][i]== subj.name or data[0][i]== subj.abbrev:
                return (subj,i)

    except IndexError:
            return -1
    
def studentDetails():
    global data
    index = getRollNumber()
    if index == -1:
        print("INVALID ROLL NUMBER.")
        studentDetails()
    else:
        headers = [str(x) for x in data[0][1:]]
        #print(headers)
        print(tabulate([data[index]], headers=headers, tablefmt='grid'))
        # print("name",data[index][1])


def updateMarks(index): 
    column= marksAddded()
    if column!=-1:
        uMarks = input("Enter updated marks: ")
        data[index][column]= uMarks
        #print(data)
    data_to_CSV()

def calculateAverage():
    global data
    index = marksAddded()
    if index != -1:
        try:
            # Convert the column to integers (excluding the header row)
            marks = data[1:, index].astype(float)  # Convert strings to floats
            average = np.mean(marks)  # Calculate the average
            print(f"AVERAGE MARKS FOR {data[0][index]}: {average}")
            #print(data)
        except ValueError:
            print("Error: Non-numeric values found in the column.")

def calGPA():
    global data
    indexes = []
    for subject in Subject_list:
        index = isValid(subject)
        if index != -1:
            indexes.append(index)
        else:
            print(f"{subject.name} marks not added")

    if len(indexes) == len(Subject_list):
        credit_sum = 0
        credit_list = []
        
        for subject in Subject_list:
            credit_list.append(subject.credit_hrs)
            credit_sum += subject.credit_hrs
            
        scalars = np.array(credit_list)

        # Select only rows with student scores (excluding headers) and specific subject columns
        scores = data[1:, [idx[1] for idx in indexes]].astype(float)
        scores = (scores / 100)*4
      
        # Multiply by the credit hours (scalars) and calculate GPA
        weighted_scores = scores * scalars

        total_weighted_scores = np.sum(weighted_scores, axis=1)
        total_weighted_scores = total_weighted_scores.reshape(-1,1)
        
        gpas = total_weighted_scores/ credit_sum
        gpas = np.round(gpas,2)
        
        gpas = gpas.reshape(-1,1)
        gpas_header = np.array([['GPA']])  # Create a header for the GPA column
        gpas_with_header = np.vstack([gpas_header, gpas])  # Stack header with GPA values

        #print(gpas_with_header)

      # Add GPA column to the data (ignoring first row header of data)
        data = np.hstack((data, gpas_with_header))

       # Print the final data with GPA
        #print(data)
        data_to_CSV()
       
def deleteRow():
     global data
     roll_no = getRollNumber()
     index = data[roll_no][0]
     if roll_no !=-1:
         data = np.delete(data,roll_no,axis=0)
         print(f"DATA FOR {index} deleted.")
         
     else:
         print("Invalid Roll number.")
         deleteRow()

def deleteColumn():
    global data
    index = False
    column = input("Enter column name: ")
    for i in range(len(data[0])):
        if column == data[0][i]:
            index = i
            break
    if not index:
        print(f"{column}does not exist.")
        deleteColumn()
    else:
        data = np.delete(data,index,axis=1)
        print(f"{column} DELETED.")
        #print(data)    

def deleteRC():
    global data
    choice = int(input("Do you want to delete:\n1) ROW\n2) COLUMN: "))
    if choice == 1:
        deleteRow()

    elif choice==2:
        deleteColumn()
    else:
        print("Invalid input.")
        deleteRC()
    data_to_CSV()

def ranking():       
    global data
    found = False
    for i in range(len(data[0])):
        if data[0][i] == "GPA" or  data[0][i] == "gpa":
            index = i
            found = True
            break
    if not found:
        print("GPA NOT CALCULATED YET.")
    else:
        sorted_data = data[data[:, index].argsort()[::-1]]
        #print(sorted_data)
        #print("TOP THREE",sorted_data[1:4])
        for i in range(1,4):
            print(f"Name:{sorted_data[i][1]},GPA:{sorted_data[i][index]}")          
    
#---------------------------------------------------------------
def menu():
   
#------------------------------------------------------------------------
    print("1) VIEW STUDENT DETAILS\n2) UPDATE MARKS\n3) CALCULATE GPA\n4) CALCULATE SUBJECT AVERAGE\n5) DELETE ROW OR COLUMN\n6) RANKING\n7) EXIT")
    choice = int(input("ENTER: "))

    if choice == 1:
       studentDetails()

    elif choice==2:
      index = getRollNumber()
      while index==-1:
        print("INVALID ROLL NUMBER.")
        index = getRollNumber()
      updateMarks(index)

    elif choice==3:
       calGPA()

    elif choice==4:
       calculateAverage()

    elif choice==5:
       deleteRC()

    elif choice==6:
      ranking()

    elif choice==7:
       SystemExit

    else:
       print("Invalid input.Try again")
    choice2 = 0
    if choice!=7:
     while choice2!=1 or choice2!=2:
       print("--------------------------------------------")
       choice2 = int(input("1) BACK\n2) EXIT\nEnter:"))
       
       if choice2==1:
          menu()
          break
       elif choice2==2:
          SystemExit
          break
       else:
           print("invalid input")
LA = Subject("Linear Algebra","LA","Dr.Adeel Ahmed",3)
DB = Subject("Database Systems","DB","Haseeb ur Rehman",4)
PAI = Subject("Programming for AI","PAI","Dr.Madiha",3)
CN = Subject("Computer Network","CN","Dr.Maryam Akbar",4)
Stats = Subject("Stastics and Probability Theory","Stats","Ms.Mudassrah",3)
Subject_list = [LA,DB,PAI,CN,Stats]
data = open_csvfile()
menu()



       