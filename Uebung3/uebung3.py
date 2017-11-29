import pprint
from bs4 import BeautifulSoup
from urllib import request, parse
import os
import sqlite3
###################################################Funktionen###################################################
#keine Funktionen benoetigt

###################################################Aufgaben###################################################
def scraping():
    ##Vorgaben
    base = 'http://xkcd.com'
    archive = parse.urljoin(base, 'archive')
    archive_page = request.urlopen(archive)
    archive_html = BeautifulSoup(archive_page.read(), 'lxml')
    print(archive_html)
    middleContainer = archive_html.find(id='middleContainer')
    anchors = middleContainer.find_all('a')
    pprint.pprint(anchors)
    comic_a = anchors[0]
    comic_url = parse.urljoin(base, comic_a['href'])
    print(comic_url)

def moduleOS():
    ##Vorgaben
    print(os.name)
    print(os.getcwd())
    os.makedirs('xkcd', exist_ok=True)

def sqlite():
    ##Vorgabe
    with sqlite3.connect('xkcd_db.db') as con:
        cur = con.cursor()
        cur.execute('DROP TABLE IF EXISTS xkcd')
        cur.execute('CREATE TABLE xkcd (url TEXT, alt TEXT)')
    cur.execute("insert into xkcd values ('some title', 'fake url')")
    con.commit()


###################################################Ausfuehrung###################################################
scraping()
#moduleOS()
#sqlite()