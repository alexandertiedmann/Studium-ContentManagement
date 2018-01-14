# littleSearchEngine.py
import pages as pa
import tdIndex as tdI
import search as search
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
    print('ranks unter : ' + filepath + '.txt\'')
    return pages


# Aufgabe d)
# tf-Index bilden aus den Woertern in den Dokumenten. Benutzung der stop_word.txt. Index im file index.txt speichern
def taskD(pages, directory):
    print('\n' + 'Aufgabe d)')
    index = tdI.Index()
    index.buildIndex(pages)
    filepath = directory + '/index'
    index.tfToFile(filepath)
    print('tf-Index unter : ' + filepath + '.txt\'')
    return index


# Aufgabe e)
# search-Fuction implementieren. tf-idf gewichtung nutzen. Cosinus Similarity wie inb der Lektuere nutzen.
# Sample search mit single-word-queries: token, index, classification
# Sample seach mit two-word-query: token, classification
# Ergenisse nach tfidf search.txt
def taskE(pages, index, directory):
    print('\n' + 'Aufgabe e)')
    searcher = search.Search(index, pages)
    # Single search
    result1 = searcher.searchWithCosine(['tokens'])
    result2 = searcher.searchWithCosine(['index'])
    result3 = searcher.searchWithCosine(['classification'])
    # Multiple Search (and)
    result4 = searcher.searchWithCosine(['tokens', 'classification'])
    results = [result1, result2, result3, result4]
    filepath = directory + '/tfidf-search'
    searcher.resultsToFile(results, filepath)
    print('Suchergebnisse unter : ' + filepath + '.txt\'')
    return searcher


# Aufgabe f)
# Suche wie in e) nur mit Cosine-Similarity und PageRank
# Ergenisse nach pageranke_search.txt
def taskF(searcher, directory):
    print('\n' + 'Aufgabe f)')
    # Single search
    result1 = searcher.searchWithRank(['tokens'])
    result2 = searcher.searchWithRank(['index'])
    result3 = searcher.searchWithRank(['classification'])
    # Multiple Search (and)
    result4 = searcher.searchWithRank(['tokens', 'classification'])
    results = [result1, result2, result3, result4]
    filepath = directory + '/pageranke_search'
    searcher.resultsToFile(results, filepath)
    print('Suchergebnisse unter : ' + filepath + '.txt\'')


directory = './files'
pages = taskAandB()
pages = taskC(pages, directory)
index = taskD(pages, directory)
# TODO: Tokenization einbauen (Zusatz da nicht in Aufgabe)
# TODO: Mit Tokenization sollten in der Suche (['tokens', 'classification']) weitere pages aufgelistet werden
searcher = taskE(pages, index, directory)
taskF(searcher, directory)
