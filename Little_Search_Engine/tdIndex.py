# tf-index.py
from bs4 import BeautifulSoup
import json
import numpy as np
import math


class Word:
    def __init__(self, word):
        self.word = word
        self.totalOccour = 0
        # Liste mit seite und vorkommen (anzahl) auf dieser Seite
        # nach: [['seite', 2],['seite', 4]]
        self.sitewords = []

    # Pruefung ob Page bereits fuer dieses Wort existiert
    def checkSiteExists(self, page):
        if len(self.sitewords) < 1:
            return False
        found = False
        for siteword in self.sitewords:
            if siteword[0].file == page.file:
                found = True
        return found

    # Gibt die Position der Seite im sitewords aus
    def __getPageForWord(self, page):
        for i in range(len(self.sitewords)):
            if self.sitewords[i][0] == page:
                return i

    def __addCount(self, pos):
        self.sitewords[pos][1] = self.sitewords[pos][1] + 1

    # zaehlt den Zaehler fuer diese Seite hoch
    def counterSiteWord(self, page):
        if self.checkSiteExists(page):
            pos = self.__getPageForWord(page)
            self.__addCount(pos)
        else:
            self.sitewords.append([page, 1])

    # String fuer das Objekt
    def toString(self):
        string = self.word
        string = string + '\n'
        for site in self.sitewords:
            string = string + site[0].file + ': ' + str(site[1]) + '\n'
        return string

    # Anzahl der Treffer vom Wort in page
    # page und Anzahl woerter fuer diese page
    def getTF(self, page, counted):
        occour = 0
        for siteword in self.sitewords:
            if page == siteword[0]:
                occour = siteword[1]
        return (occour / counted)

    # Gibt die Gesamtanzahl des Wortes in allen Dokumenten an
    def getCF(self):
        counter = 0
        for siteword in self.sitewords:
            counter = counter + siteword[1]
        return counter

    # gibt die Anzahl der Dokumente in denen das Wort vorkommt aus
    def getDF(self):
        return len(self.sitewords)


class Index:
    def __init__(self):
        self.__indexfile = './files/index.txt'
        self.__stopwordsfile = './files/stop_words.txt'
        self.__stopwords = []  # Liste mit allen stop words
        self.__numPages = 0  # Anzahl aller Dokumente
        self.wordlist = []  # Liste mit allen Woertern die in den Dokumenten vorkommen
        self.wordslist = []  # Liste mit Word-Objekten
        self.__siteWords = []  # Liste mit Anzahl der Woerter pro Dokument ([page, anzahl], [page, anzahl])
        self.__getStopWords()

    def __getStopWords(self):
        file = open(self.__stopwordsfile, 'r')
        for line in file:
            line = line.replace('\n', '')
            line = line.replace('\'', '')
            line = line.replace(' ', '')
            line = line.rstrip(',')
            words = line.split(',')
            for word in words:
                self.__stopwords.append(word)
        file.close()

    # legt eine Datei mit den Indizes an
    def buildIndex(self, pages):
        self.__buildWordList(pages)
        self.__numPages = len(pages.pages)

    # scheibt Listen
    # 1. Liste aller Woerter in allen Dokumenten (ohne stop-words) ohne doppelte
    # 2. Liste aus Word-Objekten
    # 3. Liste aus Anzahl der Worte pro Seite
    def __buildWordList(self, pages):
        for page in pages.pages:
            cleanstring = self.__getCleanString(page)
            wordsitecounter = 0
            ## Woerter der Page auslesen
            words = cleanstring.split(' ')  # hier bilden sich 'leere' woerter
            for word in words:
                # leere woerter filtern sowie einzelne Buchstaben und Stop-words raus filtern
                if word and word not in self.__stopwords and len(word) > 1:
                    wordsitecounter = wordsitecounter + 1  # zaehlt die Woerter fuer dieses Dokument
                    word = str(word).lower()  # to lower
                    # wenn noch nicht drinn dann in Liste der Woerter einfuegen
                    if word not in self.wordlist:
                        self.wordlist.append(word)
                    if self.wordInList(word):
                        wordInst = self.getWordInst(word)
                        wordInst.counterSiteWord(page)
                    else:
                        newInst = Word(word)
                        newInst.counterSiteWord(page)
                        self.wordslist.append(newInst)
            self.__siteWords.append([page, wordsitecounter])
            self.wordlist.sort()  # wort-list sortieren

    # wirft alle HTML-Tags weg und laesst den reinen Inhalt stehen
    def __cleanHTML(self, raw):
        cleantext = BeautifulSoup(raw, "html.parser").text
        return cleantext

    # Git fuer gegebenen String einen Sauberen (ohne Sonderzeichen) zurueck
    def __cleanString(self, string):
        # leere Zeilen entfernen
        newstring = '\n'.join((line for line in string.split('\n') if line))
        # Sonderzeichen entfernen
        newstring = newstring.replace(',', ' ')
        newstring = newstring.replace('.', ' ')
        newstring = newstring.replace(':', ' ')
        newstring = newstring.replace('\n', ' ')
        return newstring

    # gibt an ob es fuer das gegebene Word bereits eine Instanz in wordslist[] gibt
    def wordInList(self, searchWord):
        found = False
        for word in self.wordslist:
            if word.word == searchWord:
                found = True
        return found

    # Gibt die Wort Instanz aus dem wordslist[] fuer das gegebene wort
    def getWordInst(self, searchWord):
        for word in self.wordslist:
            if word.word == searchWord:
                return word

    # Gibt Fuer eine Seite den Kompletten Text (ohne HTML-Tags) als einen String zurueck
    def __getCleanString(self, page):
        # Dokument lesen, Tags entfernen, String saeubern
        file = open(page.file, 'r')
        cleansite = self.__cleanHTML(file)
        file.close()
        cleanstring = self.__cleanString(cleansite)
        return cleanstring

    def tfToFile(self, filepath):
        list = []
        for word in self.wordslist:
            sitelist = []
            for site in word.sitewords:
                sitelist.append([site[0].file, site[1]])
            list.append([word.word, sitelist])
        # nach JSON
        filepathjson = filepath + '.json'
        with open(filepathjson, 'w') as outfile:
            json.dump(list, outfile)
        # nach txt
        filepathTXT = filepath + '.txt'
        file = open(filepathTXT, 'w')
        for word in self.wordslist:
            file.write(str(word.toString()))
        file.close()

    # gibt die Anzahl der Woerter auf dieser Seite an
    def __getWordsinPage(self, page):
        for arr in self.__siteWords:
            if arr[0] == page:
                return arr[1]

    def calcIDF(self, word):
        if self.wordInList(word):
            inst = self.getWordInst(word)
            df = inst.getDF()  # Anzahl der Dokumente in denen das Wort vorkommt
            n = self.__numPages  # Anzahl der Dokumente
            idf = np.log((n / (1 + df)))
            return idf
        else:
            return 0

    # Berechnet den TFIDF fuer ein Word und eine Seite
    def calcTFIDF(self, word, page):
        if self.wordInList(word):
            inst = self.getWordInst(word)
            wordsOnSite = self.__getWordsinPage(page)
            tf = inst.getTF(page, wordsOnSite)  # Treffer des Wortes auf der Seite
            idf = self.calcIDF(word)
            tfidfw = tf * idf
            return tfidfw
        else:
            return 0

    # Berechnet die cosine similarity fuer zwei Vektoren
    def cosineSimilarityScore(self, vecQuer, vecDoc):
        dotProduct = np.dot(vecQuer, vecDoc)
        normQuer = np.linalg.norm(vecQuer)
        normDoc = np.linalg.norm(vecDoc)
        return dotProduct / (normQuer * normDoc)
