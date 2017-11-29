# storage.py
import entropy as entrop


class Storage:
    featurename = ''
    entireEntropy = 0
    possibleValues = []
    entropies = []

    def __init__(self, feature, values, entropies, entireEntropy):
        self.featurename = feature
        self.possibleValues = values
        self.entropies = entropies
        self.entireEntropy = entireEntropy


def getFeatures(dataStorage):
    list = []
    for store in dataStorage:
        list.append(store.featurename)
    return list


def getObject(dataStorage, feature):
    storage = Storage
    for store in dataStorage:
        if feature == store.featurename:
            storage = store
    return storage


def calcFeatureOrder(dataStoage):
    featurelist = []
    ent = 0
    for storage in dataStoage:
        if storage.featurename == 'Survived':
            ent = storage.entireEntropy
        else:
            featurelist.append(entrop.calcGain(ent, storage.entireEntropy))
    featurelist.sort()
    featurelist.reverse()
    features = []
    for i in range(0, featurelist.__len__()):
        for storage in dataStoage:
            if storage.featurename != 'Survived' and (featurelist[i]) == entrop.calcGain(ent, storage.entireEntropy):
                features.append(storage.featurename)
    return features
