import lxml.html
import codecs
import os
import json


class Page:
    def __init__(self, page, id):
        # initialisieren
        self.__path = './scraper/'
        self.file = ''  # Filename Format: __path/filename
        self.documentID = None
        self.links = []  # Liste mit file-names
        self.backlinks = []  # Listemit Page-Objekten
        self.rank = 0  # Pagerank (wird in PAges verwendet)

        # einfuegen
        self.documentID = id
        self.file = page
        self.__setPageLinks()

    def __setPageLinks(self):
        htmlfile = codecs.open(self.file, 'r')
        dom = lxml.html.fromstring(htmlfile.read())
        for link in dom.xpath('//a/@href'):  # select the url in href for all a tags(links)
            self.links.append(self.__path + link)

    def isLinkExistent(self, link):
        if link in self.links:
            return True
        else:
            return False


class Pages:
    def __init__(self):
        # initialisieren:
        self.pages = []
        self.__path = './scraper/'
        self.lastPageID = 0
        self.__s = 0.04  # Abbruchbedingung
        self.__t = 0.05  # teleportation
        self.__d = 1 - self.__t  # Daempfungsfaktor

        # seiten holen
        sites = []
        for file in os.listdir(self.__path):
            if file.endswith(".html"):
                sites.append(os.path.join(self.__path, file))
        # Seiten ins Array
        for page in sites:
            inst = Page(page, self.lastPageID)
            self.lastPageID = self.lastPageID + 1
            self.pages.append(inst)
        # Seiten die auf die Seite verweisen speichern
        for page in self.pages:
            page.backlinks = self.__setBacklinks(page)

    # nimmt ein Array mit neuen Ranks und setzt sie in die pages (sollte in der selben Reihenfolge wie pages sein)
    def __setNewPageRank(self, new_ranks):
        for i in range(len(self.pages)):
            page = self.pages[i]
            rank = new_ranks[i]
            page.rank = rank

    # Gibt eine List mit den PAgeranks in der Reihenfolge wie sie in self.pages sind aus
    def __getPageRanksFromSite(self):
        ranks = []
        for page in self.pages:
            ranks.append(page.rank)
        return ranks

    # Berechnet den Pagerank
    def __calcPageRanks(self):
        newRanks = []
        for i in range(len(self.pages)):
            page = self.pages[i]
            # Summe 1 der Formel
            sum1 = 0
            for site in page.backlinks:
                sum1 = sum1 + (site.rank / len(site.links))
            withoutLinks = self.__getNullLinkList()
            # Summe 2 der Formel
            sum2 = 0
            for page in withoutLinks:
                sum2 = sum2 + (page.rank / len(self.pages))
            # Zusammenrechnen
            rank = self.__d * (sum1 + sum2) + (self.__t / len(self.pages))
            newRanks.append(rank)
        return newRanks

    # Setzt fuer alle Seiten den Pagerank
    def getPageRanks(self):
        # Einen ersten Page-Rank berechnen und einsetzen
        firstRank = 1 / (len(self.pages))
        for page in self.pages:
            page.rank = firstRank
        # Vorbereitungen
        newRanks = self.__getPageRanksFromSite()
        start = False
        while newRanks != self.__getPageRanksFromSite() or not start:
            start = True
            newRanks = self.__calcPageRanks()
            # Pruefen ob unterbrochen wird
            diff = 0
            for i in range(len(newRanks)):
                diff += abs(self.__getPageRanksFromSite()[i] - newRanks[i])
            # Bei nicht Abbruch neue PAgeranks setzen
            if diff > self.__s:
                self.__setNewPageRank(newRanks)

    # gibt die Seiten aus welche einen Link auf die gegebene Seite aufweisen
    def __setBacklinks(self, page):
        backlinks = []
        for site in self.pages:
            if page.file in site.links:
                backlinks.append(site)
        return backlinks

    # Gibt alle Seiten ohne einen Link zu einer anderen Seite aus
    def __getNullLinkList(self):
        sitesWithoutLinks = []
        for page in self.pages:
            if len(page.links) == 0:
                sitesWithoutLinks.append(page)
        return sitesWithoutLinks

    # gibt die nach dem Pagerank sortierten Seiten zurueck
    def getSortedPages(self):
        return sorted(self.pages, key=lambda page: page.rank)  # sort by rank

    def ranksToFiles(self, filepath):
        list = []
        for page in self.getSortedPages():
            list.append([page.file, page.rank])
        # nach JSON
        filepathjson = filepath + '.json'
        with open(filepathjson, 'w') as outfile:
            json.dump(list, outfile)
        # nach txt
        filepathTXT = filepath + '.txt'
        file = open(filepathTXT, 'w')
        for page in self.getSortedPages():
            file.write(str(page.file) + ': ' + str(page.rank) + '\n')
        file.close()
