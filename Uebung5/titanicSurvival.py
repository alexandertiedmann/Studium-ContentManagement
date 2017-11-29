# titanicSurvival.py
from Uebung5 import entropy as ent
from Uebung5 import tree
import pandas as pd

###################Variables#####################
# Einlesen der Trainings-Datei
passengersTrain = pd.read_csv('train.csv')
# Ticket wird irgnorierd (ist nicht brauchbar)
passengersTrain = passengersTrain.drop('Ticket', 1)
passengersTrain = passengersTrain.drop('PassengerId', 1)

# Einlesen der Test-Datei
passengersTest = pd.read_csv('test.csv')  ##TODO remove comment
# Ticket wird irgnorierd (ist nicht brauchbar)
passengersTest = passengersTest.drop('Ticket', 1)


# speichern/ausgeben der Ergebnisse
def writeFiles():
    passengersResult.to_html('out.html', index=False)
    passengersResult.to_csv('out.csv', index=False)


#####################Exec#################
# features = ['Survived','PClass','Name,','Sex', 'Age', 'SibSp', 'Parch', 'Cabin', 'Fare', 'Embarked']
features = list(passengersTrain)
dataStorage = ent.getEntropys(passengersTrain, features)
tree1 = tree.Tree()
tree1.buildTree(dataStorage, passengersTrain)
# testdaten durch den baum jagen
passengersTest = passengersTest.assign(Survived=passengersTrain['Survived'])
passengersResult = passengersTest[['PassengerId', 'Survived']]
# writeFiles()
