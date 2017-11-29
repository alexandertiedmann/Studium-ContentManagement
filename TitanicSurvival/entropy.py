# entropy.py
import pandas as pd
import math as mat
import storage as store


def calcGain(entropy, featureEntropy):
    return entropy - featureEntropy


def calcEntropy(m, values):
    # ent=-(s1/m)*mat.log((s1/m),2)-(s2/m)*mat.log((s2/m),2)
    ent = 0
    for s in values:
        if s == 0:
            ent = ent - 0
        else:
            ent = ent - (s / m) * mat.log((s / m), 2)
    return ent


def checkPossibleValues(items):
    ray = []
    for p in items:
        if p not in ray:
            ray.append(p)
    return ray


def callTotalEntropy(item, possibleValues):
    # Anzahl der moeglichen Werte
    countPossibleValues = list(possibleValues)
    for i in range(0, countPossibleValues.__len__()):
        countPossibleValues[i] = 0
    for i in range(0, len(possibleValues)):
        zaehler = 0
        for passe in item:
            if possibleValues[i] == passe:
                zaehler = zaehler + 1
        countPossibleValues[i] = zaehler
        # Entropy mit den zahlen berechnen
    sumEntropy = calcEntropy(item.count(), countPossibleValues)
    numObjcts = item.count()
    return sumEntropy


def calcFeatureEntropy(data, possibleValues, survived):
    # noetige Arrays erstellen
    numberValues = list(possibleValues)
    for i in range(0, numberValues.__len__()):
        numberValues[i] = 0
    entropyValues = list(possibleValues)
    for i in range(0, numberValues.__len__()):
        numberValues[i] = 0
    entropyValues = list(possibleValues)

    # berechnungen
    for i in range(0, entropyValues.__len__()):
        entropyValues[i] = 0
    # Entropy fuer jeden Wert
    for i in range(0, len(possibleValues)):
        val = possibleValues[i]
        # Zaehlen der Vorkommen bei survived und not survived
        # survived
        arr = [0, 0]
        zaehler = 0
        for j in range(0, len(data)):
            if val == data[j] and survived[j] == 1:
                zaehler = zaehler + 1
        arr[0] = zaehler
        # not survived
        zaehler = 0
        for j in range(0, len(data)):
            if val == data[j] and survived[j] == 0:
                zaehler = zaehler + 1
        arr[1] = zaehler
        # berechnung der Entropy fuer diesen Wert
        entropy = calcEntropy(sum(arr), arr)
        numberValues[i] = arr
        entropyValues[i] = entropy

    # erg = ((5/14)*0.971)+((4/14)*0.0)+((5/14)*0.971)
    # print(erg)
    # numberValues=[[3,2], [4,0], [2,3]]
    # entropyValues=[0.971, 0.0, 0.971]
    # print(entropyValues)
    # print(numberValues)
    # neues Array zum aufsummieren
    nums = list(numberValues)
    for i in range(0, nums.__len__()):
        nums[i] = sum(numberValues[i])
    numObjects = sum(nums)
    # GesamtEntropy fuer das feature
    sumEntropy = 0
    for i in range(0, len(entropyValues)):
        # print(entropyValues[i])
        if entropyValues[i] == 0:
            sumEntropy = sumEntropy + 0
        else:
            sumEntropy = sumEntropy + ((nums[i] / numObjects) * entropyValues[i])
    return sumEntropy, entropyValues


def pclassValues(pclass):
    possibleValues = []
    possibleValues = checkPossibleValues(pclass)
    possibleValues.sort()
    return possibleValues


def nameValues(name):
    possibleValues = []
    for name in name:
        temp = name.split(',')
        tmp = temp[1].split('.')
        name = tmp[0]
        name = name.replace(' ', '')
        possibleValues.extend([name])
    name = pd.DataFrame.from_dict(possibleValues)
    name[0] = name[0].replace(['Ms', 'Mlle'], 'Miss')
    name[0] = name[0].replace('Mme', 'Mrs')
    name[0] = name[0].replace(['Jonkheer', 'Don', 'Major', 'Col', 'Dr', 'Rev', 'Master'], 'Mr')
    name = name[0]
    possibleValues.sort()
    possibleValues = checkPossibleValues(name)
    return possibleValues, name


def sexValues(sex):
    possibleValues = []
    possibleValues = checkPossibleValues(sex)
    possibleValues.sort()
    return possibleValues


def ageValues(age):
    mean = pd.DataFrame.mean(age)
    max = pd.DataFrame.max(age)
    min = pd.DataFrame.min(age)
    # moegliche Werte
    bins = [-1, 0, 5, 12, 18, 25, 35, 60, 120]
    groups = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
    age = pd.cut(age, bins, labels=groups)
    possibleValues = []
    possibleValues = checkPossibleValues(age)
    return possibleValues, age


def sibSpValues(sibSp):
    possibleValues = []
    possibleValues = checkPossibleValues(sibSp)
    possibleValues.sort()
    return possibleValues


def parchValues(parch):
    possibleValues = []
    possibleValues = checkPossibleValues(parch)
    possibleValues.sort()
    return possibleValues


def cabinValues(cabin):
    cabi = pd.DataFrame.copy(cabin)
    for i in range(0, len(cabi)):
        bin = cabi[i]
        if pd.isnull(bin):
            bin = 'N'
        cabi[i] = bin[0]
    possibleValues = []
    possibleValues = checkPossibleValues(cabi)
    return possibleValues, cabi


def fareValues(fare):
    mean = pd.DataFrame.mean(fare)
    max = pd.DataFrame.max(fare)
    min = pd.DataFrame.min(fare)
    bins = [-1, 0, 10, 25, 31, 1000]
    groups = ['unk.', '1', '2', '3', '4']
    fare = pd.cut(fare, bins, labels=groups)
    possibleValues = []
    possibleValues = checkPossibleValues(fare)
    #possibleValues.sort()
    return possibleValues, fare


def embarkedValues(embarked):
    embarked = embarked.fillna('S')  # leere mit 'S' <-- 2 stueck
    possibleValues = []
    possibleValues = checkPossibleValues(embarked)
    return possibleValues


def getEntropys(passengersTrain, features):
    entropyStorage = None
    dataStorage = []  # Array aus entropyStorages
    entropyArr = list(features)
    passengers = passengersTrain.copy()
    for i in range(0, len(features)):
        feature = features[i]
        passenger = passengers[feature]
        if feature == 'Survived':
            possibleValues = checkPossibleValues(passenger)
            entropyGesamt = callTotalEntropy(passenger, possibleValues)
            entropyArr[i] = entropyGesamt
        elif feature == 'Pclass':
            possibleValues = pclassValues(passenger)
        elif feature == 'Name':
            possibleValues, passenger = nameValues(passenger)
        elif feature == 'Sex':
            possibleValues = sexValues(passenger)
        elif feature == 'Age':
            possibleValues, passenger = ageValues(passenger)
        elif feature == 'SibSp':
            possibleValues = sibSpValues(passenger)
        elif feature == 'Parch':
            possibleValues = parchValues(passenger)
        elif feature == 'Cabin':
            possibleValues, passenger = cabinValues(passenger)
        elif feature == 'Fare':
            possibleValues, passenger = fareValues(passenger)
        elif feature == 'Embarked':
            possibleValues = embarkedValues(passenger)
        if feature != 'Survived':
            sumEntropy, entropyValues = calcFeatureEntropy(passenger, possibleValues, passengersTrain['Survived'])
            entropyStorage = store.Storage(feature, possibleValues, entropyValues, sumEntropy)  # Datenhaltung fuer ein Feature
        else:
            entropyValues = [0, 0]
            entropyStorage = store.Storage(feature, possibleValues, entropyValues, entropyGesamt)
        dataStorage.append(entropyStorage)  # Datenhaltung der daten fuer alle Features
    return dataStorage
