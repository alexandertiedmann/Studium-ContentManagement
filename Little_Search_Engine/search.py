# search.py

import numpy as np


class Search:
    def __init__(self, index, pages):
        self.__index = index
        self.__pages = pages

    # Wie search() nur nach Rang der Seiten sortiert
    def searchWithRank(self, words):
        result = []  # Liste aus Links
        if len(words) > 1:
            result = self.__multipleAndSearch(words)
        else:
            result = self.__singleSearch(words[0])
        sortedResults = self.__cosineAndPagerankSort(words, result)
        return sortedResults

    # Sucht fuer eine Lsite an Woertern die Links der Seiten
    def searchWithCosine(self, words):
        result = []  # Liste aus Links
        if len(words) > 1:
            result = self.__multipleAndSearch(words)
        else:
            result = self.__singleSearch(words[0])
        sortedResults = self.__cosineSort(words, result)
        return sortedResults

    # Sortiert nach cosine similarity
    def __cosineSort(self, words, unsortResult):
        # Query Vekotr berechnen
        queryVector = self.__getQueryVector(words)
        # Cosine scores berechnen
        scores = self.__getCosineScores(queryVector, words, unsortResult)
        # sortierte ergebnisse in Liste
        results = []
        for scoreresult in scores:
            results.append(scoreresult[0].file)
        return results

    # Berechnet den Cosine-Score und gibt fuer jede Seite einen Score wieder
    # Rueckgabe Liste ([page, score][page,score])
    def __getCosineScores(self, queryVector, words, unsortedPages):
        scores = []
        for page in unsortedPages:
            site = self.__pages.getPageFromList(page)
            # Vector fuer Dokumente berechnen
            documentVector = []
            for word in words:
                documentVector.append(self.__index.calcTFIDF(word, site))
            scores.append([site, self.__index.cosineSimilarityScore(queryVector, documentVector)])
        scores = sorted(scores, key=lambda page: page[1], reverse=True)  # sort by score
        return scores

    # Berechnet aus Pagerank und cosine-Score den Total Score fuer jede Seite
    # Ausgabe: List ([page, score],[page, score])
    def __getTotalScores(self, cosinescores, pages):
        # Total_Score = 2 * (cosine - score * pagerank) / (cosine - score + pagerank)
        totalScores = []
        for page in pages:
            # Rang und Score holen
            rank = page.rank
            cosinescore = 0
            for score in cosinescores:
                if score[0] == page:
                    cosinescore = score[1]
            # Rang und Score mergen
            totalScore = 2 * (cosinescore * rank) / (cosinescore + rank)
            totalScores.append([page, totalScore])
        totalScores = sorted(totalScores, key=lambda totalScore: totalScore[1], reverse=True)  # sort by score
        return totalScores

    # Berechnet den TF-IDF-Vector des Queries
    def __getQueryVector(self, words):
        querVector = []
        for word in words:  # Fuer jedes Wort im Query
            sum = 0
            if self.__index.wordInList(word):
                tf = 0  # TF des Queries
                for i in range(len(words)):
                    if words[i] == word:
                        tf = tf + 1  # Treffer des Wortes im Query
                idf = self.__index.calcIDF(word)  # IDF des Wortes
                tfidfw = tf * idf
                querVector.append(tfidfw)
        return querVector

    # Sortiert nach Cosine Similarity UND Page Rank
    def __cosineAndPagerankSort(self, words, unsortedResults):
        # Query Vekotr berechnen
        queryVector = self.__getQueryVector(words)
        # Cosine scores berechnen
        cosineScores = self.__getCosineScores(queryVector, words, unsortedResults)
        # Pageranks und coinescores verbinden
        pageobjects = []
        for page in unsortedResults:
            pageobjects.append(self.__pages.getPageFromList(page))
        sortedresults = self.__getTotalScores(cosineScores, pageobjects)
        results = []
        for entry in sortedresults:
            results.append(entry[0].file)
        return results

    # sucht alle Links in denen das Wort vorkommt
    def __singleSearch(self, word):
        resultOb = self.wordInDoc(word)
        results = []
        for result in resultOb:
            results.append(result.file)
        return results

    # sucht alle Links in denen die Woerter vorkommen
    def __multipleAndSearch(self, words):
        # Suche
        results = []
        sites = self.wordInDoc(words[0])
        for site in sites:
            allFound = []  # auch alle anderen Woerter gefunden?
            for i in range(1, len(words)):
                word = words[i]
                sitewords = self.__index.getWordInst(word).sitewords
                searchsites = []
                for siteword in sitewords:
                    searchsites.append(siteword[0].file)
                if site.file in searchsites:
                    allFound.append(True)
                else:
                    allFound.append(False)
            if False in allFound:
                pass
            else:
                results.append(site.file)
        return results

    # Gibt eine Liste mit pages in denen das Wort vorkommt aus
    def wordInDoc(self, word):
        siteWithWord = self.__index.getWordInst(word).sitewords
        pagelist = []
        for site in siteWithWord:
            pagelist.append(site[0])
        return pagelist

    # Schreibt die Liste mit Links aus den Suchen in ein File
    def resultsToFile(self, results, filepath):
        # nach txt
        filepathTXT = filepath + '.txt'
        file = open(filepathTXT, 'w')
        for result in results:
            file.write(str(result) + '\n')
        file.close()
        print(filepath)
        for result in results:
            print(result)
