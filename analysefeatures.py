from __future__ import division
import numpy as np
import csv
from matplotlib import pylab as plt
from sklearn.linear_model import LogisticRegression

def getInput(filename):
    indexMod = 0;
    if filename == "test.csv":
        indexMod = 1;

    file = open(filename)
    csv_f= csv.reader(file, delimiter = ',')
    surv=[]
    age=[]
    fr=1
    sclass=[]
    fare=[]
    gender=[]
    for row in csv_f:  
        if fr==1:
            fr=200
            continue
        print row
        surv.append(row[1-indexMod])
        #gender
        if row[4-indexMod]=="female" :
            gender.append('1')
        elif row[4-indexMod]=="male":
            gender.append('0')
            print row[4-indexMod]
        #age         
        if row[5-indexMod] is '':
            word = row[3-indexMod].split()
            if 'Master.' in word or 'Miss.' in word:
                row[5-indexMod]='5'
            elif 'Mrs.' in word or 'Mr.' in word:
                row[5-indexMod]='35'
            else:
                row[5-indexMod]='40'
        if '0.' in row[5-indexMod]:
            row[5-indexMod]='0'
        if '.' in row[5-indexMod]:
            a=row[5-indexMod]
            a=a[0:2]
            row[5-indexMod]=a
        y=float(int(row[5-indexMod]))
        age.append(y)
        #class
        if row[2-indexMod]=='1':
            sclass.append('1')
        elif row[2-indexMod]=='2':
            sclass.append('2')
        elif row[2-indexMod]=='3':
            sclass.append('3')
        #fare
        if row[-3] =='':  
            fare.append('0')
        else:
            fare.append(row[-3])
            
    age=map(float,age)
    gender=map(float,gender)
    sclass=map(float,sclass)
    surv= map(float,surv)
    fare = map(float, fare)
    #checking percentage of children survivors
    tAge=1
    tAAge=1
    sAAge=0
    sAge=0
    tHighFare=1
    sHighFare=0
    tLowFare=1
    sLowFare=0
    if indexMod==0:
        tAge=0;
        tAAge=0;
        tHighFare=0;
        tLowFare=0;
        for i in age:
            if i<15:
                tAge+=1
                if surv[age.index(i)]==1:
                    sAge+=1;
            else:
                tAAge+=1;
                if surv[age.index(i)]==1:
                    sAAge+=1;
         #checking the number of survivors that paid higher fare
        for j in fare:
             if j>75:
                 tHighFare+=1;
                 if surv[fare.index(j)]==1:
                     sHighFare+=1;
             else:
                 tLowFare +=1;
                 if surv[fare.index(j)]==1:
                     sLowFare+=1;
    print ("Ratio of survived children to the the total number of children =")
    print sAge/tAge
    print ("Ratio of survivied adults to the total number of adults =")
    print sAAge/tAAge
    print("Ratio of people who paid high fare and survived = ")
    print sHighFare/tHighFare
    print("Ratio of people who paid low fare and survived = ")
    print sLowFare/tLowFare
    genHistograms(age,20,"age",1)
    genHistograms(gender,25,"gender",2)
    genHistograms(sclass,20,"class",3)
    genHistograms(fare,50,"fare",4)
    
    X = np.column_stack((gender,sclass,age,fare))
    Y=np.array(surv)
    
    return (X,Y)


def trainModel(trainX,trainY):
    model= LogisticRegression()
    model = model.fit(trainX,trainY)
    print model.score(trainX,trainY)
    return model

def testModel(testX):
    return model.predict(testX)

def genHistograms(field,binVal,label,i):
    print label
    plt.hist(field,binVal)
    plt.show()
    plt.savefig("plot"+str(i)+".jpg")
    plt.clf()


# Action Code    
(trainX,trainY) = getInput("train.csv")
(testX,garbage) = getInput("test.csv")
model = trainModel(trainX,trainY)
prediction = testModel(testX)

with open("prediction.txt","w") as textfile:
    for ele in prediction:
        textfile.write(str(ele)+"\n")
        
#print prediction
