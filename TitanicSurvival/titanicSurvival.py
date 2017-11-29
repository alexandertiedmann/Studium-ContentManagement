# titanicSurvival.py
import entropy as ent
import tree
import pandas as pd

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


#####################Exec#################
# features = ['Survived','PClass','Name,','Sex', 'Age', 'SibSp', 'Parch', 'Cabin', 'Fare', 'Embarked']
print('1/5 calculate Entropies')
features = list(passengersTrain)
dataStorage = ent.getEntropys(passengersTrain, features)  # berechnen der Entropien

print('2/5 build tree')
tree1 = tree.Tree()
tree1.buildTree(dataStorage)  # Baum erstellen mit den berechneten Entropien in dataStorage

print('3/5 train Tree')
passengersTrain = tree1.normalizePassenger(passengersTrain)  # Passagiere normalisieren
tree1.trainTree(passengersTrain)  # mit normalisierten Passagieren den Baum trainieren
#tree1.printTree('', tree1.dataTree)

print('4/5 categorize test-data')
passengersTest = tree1.normalizePassenger(passengersTest)
passengersTest = tree1.categorize(passengersTest)

print('5/5 save results in html and csv-file')
passengersResult = passengersTest[['PassengerId', 'Survived']]
writeFiles(passengersResult)