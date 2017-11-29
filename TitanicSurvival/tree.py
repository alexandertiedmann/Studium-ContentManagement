# tree.py
import pandas as pd
import storage as store
import entropy as ent


class Node:
    def __init__(self, feature, prenode):
        self.feature = feature
        self.nextNodes = []
        self.decisions = []
        self.prenode = prenode

    def setDecisions(self, decisions):
        self.decisions = decisions

    def getDecisions(self):
        return self.decisions


class Endnode:
    def __init__(self, prenode):
        self.feature = 'Survived'
        self.survived = None
        self.counted = [0, 0]
        self.prenode = prenode

    def setSurvived(self, value):
        self.survived = value


class Tree:
    dataTree = None
    featurelist = []

    def __init__(self):
        dataTree = None

    def setFeaturelist(self, features):
        self.featurelist = features

    def buildTree(self, dataStorage):
        self.setFeaturelist(store.calcFeatureOrder(dataStorage))
        self.dataTree = Node(self.featurelist[0], None)
        self.buildRec(dataStorage, self.dataTree, 0)

    def buildRec(self, dataStorage, node, position):
        if isinstance(node, Endnode):
            return  # Ende wenn Endnode
        # dataStorage: gespeicherte Daten: Feature Name, Feature Entropy, moegliche Werte, Entropien fuer moegliche Werte
        # node: Node des Trees: feature, Array - nachste Nodes, Array - decisions
        feature = store.getObject(dataStorage, self.featurelist[position])  # feature aus dem Store einlesen
        try:
            nextFeature = self.featurelist[position + 1]
        except IndexError:
            nextFeature = 'Survived'
        node.decisions = list(feature.possibleValues)  # moegliche Werte eintragen
        entropies = feature.entropies  # Entropien fuer moegliche Werte holen
        for valNr in range(0, node.decisions.__len__()):  # fuer jeden moegleichen Wert = Entscheidung
            possibleValueEntropy = entropies[valNr]  # Entropie fuer den moeglichen Wert
            if possibleValueEntropy > 0:
                if nextFeature != 'Survived':
                    nextNode = Node(nextFeature, node)  # Wenn Entropei fuer moeglichen Wert --> naechste Node bestimmen
                else:
                    nextNode = Endnode(node)  # wenn Entropie 0 --> naechste Node ist Survived (Endentscheidung)
            else:
                nextNode = Endnode(node)  # wenn Entropie 0 --> naechste Node ist Survived (Endentscheidung)
            node.nextNodes.append(nextNode)  # naechste Node an Array in der Node anfuegen
            self.buildRec(dataStorage, nextNode, position + 1)  # zur naechsten Node sprigen

    def trainTree(self, passengersTrain):
        for i in range(0, len(passengersTrain)):
            self.trainRec(self.dataTree, passengersTrain.loc[[i]])
        self.trainTreeRec(self.dataTree)

    def trainTreeRec(self, node):
        if isinstance(node, Endnode):
            if node.counted[1] > node.counted[0]:
                node.setSurvived(True)
            elif node.counted[1] < node.counted[0]:
                node.setSurvived(False)
            return
        else:
            for nextNode in node.nextNodes:
                self.trainTreeRec(nextNode)

    def trainRec(self, node, passenger):
        if isinstance(node, Endnode):
            surv = passenger['Survived'].item()
            if surv == 1:
                node.counted[1] = node.counted[1] + 1
            elif surv == 0:
                node.counted[0] = node.counted[0] + 1
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
        print(tree, node.feature)
        tree += '-'
        if isinstance(node, Endnode):
            return
        for nextNode in node.nextNodes:
            self.printTree(tree, nextNode)
