# tree.py
import pandas as pd
import Uebung5.storage as store
import Uebung5.entropy as ent


class Node:
    def __init__(self, feature):
        self.feature = feature
        self.nextNodes = []
        self.decisions = []

    def setDecisions(self, decisions):
        self.decisions = decisions

    def getDecisions(self):
        return self.decisions


class Tree:
    dataTree = None
    featurelist = []

    def __init__(self):
        dataTree = None

    def setFeaturelist(self, features):
        self.featurelist = features

    def buildTree(self, dataStorage, passengersTrain):
        self.setFeaturelist(store.calcFeatureOrder(dataStorage))
        self.dataTree = Node(self.featurelist[0])
        self.buildRec(dataStorage, self.dataTree, 0)
        passengersTrain = self.normalizePassenger(passengersTrain)
        self.trainTree(passengersTrain)
        #self.printTree('', self.dataTree)

    def buildRec(self, dataStorage, node, position):
        # dataStorage: gespeicherte Daten: Feature Name, Feature Entropy, moegliche Werte, Entropien fuer moegliche Werte
        # node: Node des Trees: feature, Array - nachste Nodes, Array - decisions
        # position: Position in der Featureliste(Array) welches Feature gerade bearbeitet wird
        if node.feature == 'Survived':
            node.setDecisions([0, 0])  # setzt Array erst mal auf nicht ueberlebt (wird spaeter anhand der Daten gefuellt)
            return
        feature = store.getObject(dataStorage, self.featurelist[position])  # feature aus dem Store einlesen
        try:
            nextFeature = self.featurelist[position + 1] # wenn moeglich naechstes Feature auslesen
        except (IndexError):
            nextFeature = 'Survived' # wenn Array zu kurz fuer naechste Node --> Ende also Survived Node
        node.decisions = list(feature.possibleValues)  # moegliche Werte eintragen
        entropies = feature.entropies # Entropien fuer moegliche Werte holen
        for valNr in range(0, node.decisions.__len__()): # fuer jeden moegleichen Wert = Entscheidung
            possibleValueEntropy = entropies[valNr] # Entropie fuer den moeglichen Wert
            if possibleValueEntropy > 0:
                nextNode = Node(nextFeature) # Wenn Entropei fuer moeglichen Wert --> naechste Node bestimmen
                #nextNode.setDecisions(store.getObject(dataStorage, nextFeature).possibleValues) #und Entscheidungen eintragen
            else:
                nextNode = Node('Survived') # wenn Entropie 0 --> naechste Node ist Survived (Endentscheidung)
            node.nextNodes.append(nextNode) # naechste Node an Array in der Node anfuegen
            try:
                self.buildRec(dataStorage, nextNode, position + 1)  # naechsten node und zur naechsten Node sprigen
            except (IndexError):
                self.buildRec(dataStorage, nextNode, 0)  # nur bei 'Survived' Nodes # zur letzten Node wenn keine uebrig gebliebenen Features

    def trainTree(self, passengersTrain):
        for i in range(0, len(passengersTrain)):
            self.trainRec(self.dataTree, passengersTrain.loc[[i]])
        self.trainTreeRec(self.dataTree)

    def trainTreeRec(self, node):
        if node.feature == 'Survived':
            survived = node.decisions[1]
            notSurvived = node.decisions[0]
            if survived > 0 and notSurvived > 0:
                print(node.decisions)
            if survived == 0 and notSurvived == 0:
                print(node.feature, node.decisions)
            if survived > notSurvived:
                node.decisions = 'survived'
            elif survived < notSurvived:
                node.decisions = 'dead'
            else:
                node.decisions = 'FAILED'
            return
        else:
            for nextNode in node.nextNodes:
                self.trainTreeRec(nextNode)

    def trainRec(self, node, passenger):
        if node.feature == 'Survived':
            surv = passenger['Survived'].item()
            if surv == 1:
                node.decisions[1] = node.decisions[1] + 1
            else:
                node.decisions[0] = node.decisions[0] + 1
            return
        for i in range(0, len(node.decisions)):
            comp = passenger.iloc[0][node.feature]
            decision = node.decisions[i]
            if decision == comp:
                nextNode = node.nextNodes[i]
                self.trainRec(nextNode, passenger)
            elif i == len(node.decisions):
                return

    def normalizePassenger(self, passengersTrain):
        features = list(passengersTrain)
        for i in range(0, len(features)):
            feature = features[i]
            passenger = passengersTrain[feature]
            if feature == 'Name':
                possibleValues, tmppass = ent.nameValues(passenger)
                passengersTrain.__delitem__(feature)
                passengersTrain = passengersTrain.assign(Name=tmppass)
            elif feature == 'Age':
                possibleValues, tmppass = ent.ageValues(passenger)
                passengersTrain.__delitem__(feature)
                passengersTrain = passengersTrain.assign(Age=tmppass)
            elif feature == 'Cabin':
                possibleValues, tmppass = ent.cabinValues(passenger)
                passengersTrain.__delitem__(feature)
                passengersTrain = passengersTrain.assign(Cabin=tmppass)
            elif feature == 'Fare':
                possibleValues, tmppass = ent.fareValues(passenger)
                passengersTrain.__delitem__(feature)
                passengersTrain = passengersTrain.assign(Fare=tmppass)
        return passengersTrain

    def printTree(self, tree, node):
        # print(tree, node.feature, node.decisions, len(node.nextNodes))
        # tree += '-'
        if node.feature == 'Survived':
            print(node.decisions)
        for nextNode in node.nextNodes:
            self.printTree(tree, nextNode)
