# titanicSurvival.py
from random import randint
from random import shuffle
from numpy import arange
import pandas as pd
import entropy as ent
import storage as store
import tree

###################Variables#####################
# Einlesen der Trainings-Datei
passengersTrain = pd.read_csv('train.csv')
# Ticket wird irgnorierd (ist nicht brauchbar)
passengersTrain = passengersTrain.drop('Ticket', 1)
passengersTrain = passengersTrain.drop('PassengerId', 1)

# Einlesen der Test-Datei
passengersTest = pd.read_csv('test.csv')
# Ticket wird irgnorierd (ist nicht brauchbar)
passengersTest = passengersTest.drop('Ticket', 1)


# speichern/ausgeben der Ergebnisse
def writeFiles(passengersResult):
    passengersResult.to_html('out.html', index=False)
    passengersResult.to_csv('out.csv', index=False)


def splitTrainData(passengerTest):
    countPassengersToDel = randint(200, 500)
    passengerlist = passengerTest.copy()
    # Array leer machen aber Header behalten
    for i in range(0, countPassengersToDel):
        toDel = randint(0, len(passengerlist))
        passengerlist = passengerlist.drop(passengerlist.index[toDel - 1])
    index = range(0, len(passengerlist))
    passengerlist = passengerlist.reset_index(drop=True)
    passengerlist.reindex(index)
    # print(len(passengerlist))
    return passengerlist


def randomize(featurelist):
    # featurelist.remove('Survived')
    x = arange(len(featurelist))
    shuffle(x)
    returnarray = []
    for i in range(0, len(featurelist)):
        y = x[i]
        returnarray.append(featurelist[y])
    if returnarray[0] == 'Survived':
        returnarray = randomize(returnarray)
    # returnarray.append('Survived')
    return returnarray


#####################Exec#################
numTrees = randint(20, 25)  # Anzahl der Random Trees bestimmen
print('number of RandomTrees: ', numTrees)  # Anzahl der Baeume ausgeben
# features = ['Survived','PClass','Name,','Sex', 'Age', 'SibSp', 'Parch', 'Cabin', 'Fare', 'Embarked']
print('1/5 calculate entropies')  # berechnen der Entropien
features = list(passengersTrain)  # Liste der genutzten Features

# Erstellen der PassagierTestListe
randomPassengersLists = []
randomPassengersLists.append(passengersTrain.copy())
for i in range(1, numTrees):
    randomPassengersLists.append(splitTrainData(passengersTrain.copy()))

# Vorbereitung fuer Random Forest
dataStorage1 = ent.getEntropys(randomPassengersLists[0], features.copy())
randomDataStorages = []
randomDataStorages.append(dataStorage1)
for i in range(1, numTrees):
    # zufaellig gesplittete Daten aus den Trainingsdaten
    # Entropien fuer gesplittete Daten
    randomDataStorages.append(ent.getEntropys(randomPassengersLists[i], features.copy()))

print('2/5 build trees')
tree1 = tree.Tree()
tree1.buildTree(randomDataStorages[0], store.calcFeatureOrder(randomDataStorages[0]))
randomTrees = []
randomTrees.append(tree1)
randomfeatures = features.copy()
for i in range(1, numTrees):
    randomTrees.append(tree.Tree())
    randomTrees[i].buildRandomTree(randomDataStorages[i], randomize(randomfeatures.copy()))

print('3/5 train trees')
for i in range(0, numTrees):
    passenger = randomPassengersLists[i]
    normpassengers = randomTrees[i].normalizePassenger(passenger)
    randomTrees[i].trainTree(normpassengers)

print('4/5 categorize test-data')
passengersToTest = randomTrees[0].normalizePassenger(passengersTest)
# mit Random Forest klassifizieren
classifiedPassengers = []
for i in range(0, numTrees):
    classifiedPassengers.append(randomTrees[i].categorize(passengersToTest))

# PassagierNummern
list = classifiedPassengers[0]
pasNums = classifiedPassengers[0]['PassengerId']

passengersEnd = pd.DataFrame(columns=['PassengerId', 'Survived'])

for num in pasNums:
    survived = [0, 0, 0]  # [0, 1, NONE] = [Anzahl not survieved, Anzahl survived, Anzahl NONE]
    for i in range(0, len(classifiedPassengers)):
        passengerNum = 0
        for j in range(0, len(classifiedPassengers[i])):
            passengerNum = classifiedPassengers[i].iloc[j]['PassengerId']
            passengerSurv = classifiedPassengers[i].iloc[j]['Survived']
            if num == passengerNum:
                if passengerSurv == 0:
                    survived[0] = survived[0] + 1
                elif passengerSurv == 1:
                    survived[1] = survived[1] + 1
                elif passengerSurv == 'NONE':
                    survived[2] = survived[2] + 1
    maxVal = max(survived)
    if maxVal == 0:
        for i in range(0, len(survived) - 1):
            print('nicht zuordbar')
            survived[i] = randint(1, 10)
            maxVal = max(survived)
    maxIndex = survived.index(maxVal)
    surv = None
    if maxIndex == 0:
        surv = 0
    elif maxIndex == 1:
        surv = 1
    elif maxIndex == 2:
        if survived[0] != 0 and survived[1] != 0:
            if survived[0] > survived[1]:
                surv = 0
            elif survived[1] > survived[0]:
                surv = 1
            else:
                survived = 0
        elif survived[0] != 0 and survived[1] == 0:
            surv = 0
        elif survived[0] == 0 and survived[1] != 0:
            surv = 1
        else:
            surv = 1
    if surv == None:
        surv = 0
    newDataFrame = pd.DataFrame({'PassengerId': [num], 'Survived': [surv]})
    passengersEnd = passengersEnd.append(newDataFrame)
print('5/5 save results in html and csv-file')
passengersResult = passengersEnd[['PassengerId', 'Survived']]
writeFiles(passengersResult)
