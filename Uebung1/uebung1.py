from urllib import request
from bs4 import BeautifulSoup

###################################################Funktionen###################################################
def get_Value(names):
    erg=0
    i=1
    for i in range(len(names)):
        name = names[i]
        sumLetter=0
        for letter in (name):
            sumLetter = sumLetter + (ord(letter) - ord('A') + 1)
        erg = erg + (sumLetter * (i+1))
    print(erg)

def dec(p):
    s = p
    erg=""
    for letter in p:
        num = ord(letter)
        ceasar = chr(num-1)
        erg+=str(ceasar)
    s=erg
    # Here: modify s to get the desired result
    return s


###################################################Aufgaben###################################################
def ProjEulerProb22():
    print('Project Euler Problem 22')
    with open('p022_names.txt', 'r') as f:
        line = f.read()
    names = line.replace('"', '').split(',')
    names.sort()
    print(names)
    get_Value(names)
    print('\n\n')

def spiegelminus():
    print('Spiegel Minus')
    url = 'http://www.spiegel.de/spiegel/lidl-gruender-dieter-schwarz-der-koenig-von-heilbronn-a-1143420.html'
    f = request.urlopen(url)
    content = str(f.read(), 'utf-8')
    soup = BeautifulSoup(content, 'lxml')
    obf = soup.find_all('p', {'class': 'obfuscated'})
    for p in obf:
        print (p.text)

    f = open('workfile', 'w')
    f.write('0123456789abcdef')

###################################################Ausfuehrung###################################################
ProjEulerProb22()
spiegelminus()
print('bcde -->',dec('bcde'))