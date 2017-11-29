import re, operator
###################################################Funktionen###################################################
#keine Funktionen benoetigt

###################################################Aufgaben###################################################
def dictionaries():
    ##Vorgaben
    fruits = {
        'apple': 1.99,
        'orange': 2.99,
        'banana': 2.49,
        'grape': 3.99
    }
    print(fruits)
    fruits_list = [(k, fruits[k]) for k in fruits]
    print(fruits_list)
    fruits_sorted_by_price = sorted(fruits_list, key=lambda k: k[1])
    print(fruits_sorted_by_price)
    fruits_sorted_by_name = sorted(fruits_list, key=lambda k: k[0])
    print(fruits_sorted_by_name)

    with open('text1.txt', 'r') as f:
        line = f.read()
    text = re.sub('[\W]', " ", line)
    print(text)

    ##Aufgabe Loesung:
    letter_list = {
        "A" : 0,
        "B" : 0,
        "C" : 0,
        "D" : 0,
        "E" : 0,
        "F" : 0,
        "G" : 0,
        "H" : 0,
        "I" : 0,
        "J" : 0,
        "K" : 0,
        "L" : 0,
        "M" : 0,
        "N" : 0,
        "O" : 0,
        "P" : 0,
        "Q" : 0,
        "R" : 0,
        "S" : 0,
        "T" : 0,
        "U" : 0,
        "V" : 0,
        "W" : 0,
        "X" : 0,
        "Y" : 0,
        "Z" : 0,
        "Ä" : 0,
        "Ö" : 0,
        "Ü" : 0,
        "ß" : 0
        }
    for letter in text:
        letter.upper()
        for key in letter_list.keys():
            if key == letter:
                letter_list[key] = letter_list[key]+1
    print(letter_list)
    letter_list_sorted = sorted(letter_list.items(), key=operator.itemgetter(1))
    letter_list_sorted.reverse()
    print(letter_list_sorted)
    for i in range(6):
        print(letter_list_sorted[i])

def regularExpression():
    with open('text1.txt', 'r') as f:
        line = f.read()
    text = re.sub("\s\s+", " ", line)
    print(text)

###################################################Ausfuehrung###################################################
dictionaries()
regularExpression()