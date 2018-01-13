# littleSearchEngine.py
import pages as pa
import tdIndex as tdI
import json


# Aufgabe a) und b) Herunterladen der Seiten mit scrapy
# CLI in scraper
# Befehl:
#   scrapy.exe crawl dataScraper
def taskAandB():
    print('Aufgabe a)')
    print('implementieren eines Scrapers. Siehe ./scraper/ ')
    print('\n' + 'Aufgabe b)')
    print('Seiten holen mit \'scrapy.exe crawl dataScraper\' und speichern unter ./scraper/')
    pages = pa.Pages()
    return pages


# Aufgabe c)
# berechnen des Pages Ranks teleportation t = 0.05 und sigma = 0.04 . Ergebnis nach rank.txt
def taskC(pages, directory):
    print('\n' + 'Aufgabe c)')
    pages.getPageRanks()
    filepath = directory + '/rank'
    pages.ranksToFiles(filepath)
    print('ranks unter : \'./files/rank.txt\'')
    return pages


# Aufgabe d)
# tf-Index bilden aus den Woertern in den Dokumenten. Benutzung der stop_word.txt. Index im file index.txt speichern
def taskD(pages, directory):
    print('\n' + 'Aufgabe d)')
    index = tdI.Index()
    index.buildIndex(pages)
    filepath = directory + '/index'
    index.tfToFile(filepath)
    print('tf-Index unter : \'./files/rank.txt\'')
    return index


# Aufgabe e)
# search-Fuction implementieren. tf-idf gewichtung nutzen. Cosinus Similarity wie inb der Lektuere nutzen.
# Sample search mit single-word-queries: token, index, classification
# Sample seach mit two-word-query: token, classification
# Ergenisse nach tfidf search.txt
def taskE(pages):
    pass


# Aufgabe e)
# search-Fuction implementieren. tf-idf gewichtung nutzen. Cosinus Similarity wie inb der Lektuere nutzen.
# Sample search mit single-word-queries: token, index, classification
# Sample seach mit two-word-query: token, classification
# Ergenisse nach tfidf search.txt
def taskF(pages):
    pass


directory = './files'
pages = taskAandB()
pages = taskC(pages, directory)
index = taskD(pages, directory)
