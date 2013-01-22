#! /usr/bin/python
from lxml.cssselect import CSSSelector
from lxml.html import fromstring
from lxml.html import parse
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
import sys
import codecs
import time

class Downloader(QObject):
    done = Signal()

    def __init__(self,fol1,fol2, urlList, parent = None):
        super(Downloader, self).__init__(parent)
        self.urlList = urlList
        self.fol1 = fol1
        self.fol2 = fol2
        self.counter = 0        
        self.page = QWebPage(self)      
        self.page.loadFinished.connect(self.save)
        self.startNext()

    def currentUrl(self):
        return self.urlList[self.counter][0]

    def currentFilename(self):
        return self.urlList[self.counter][1]

    def startNext(self):
        print "Downloading %s..."%self.currentUrl()
        self.page.mainFrame().load(self.currentUrl())

    def save(self, ok):
        if ok:            
            time.sleep(1)
            data = self.page.mainFrame().toHtml()
            w = self.currentFilename()
            fil1 = open(self.fol2+w[0:w.rfind('.')]+".txt","w")
            d = fromstring(data)
            sel = CSSSelector("td[class=dog] a")
            for e in sel(d):
				fil1.write(e.get('href')+"\n")
            fil1.close()
            with codecs.open(self.fol1+self.currentFilename()+".html", encoding="utf-8", mode="w") as f:
                f.write(data)
            print "Saving %s to %s."%(self.currentUrl(), self.currentFilename())            
        else:
            print "Error while downloading %s\nSkipping."%self.currentUrl()
        self.counter += 1
        if self.counter < len(self.urlList):            
            self.startNext()
        else:
            self.done.emit()

filename = "him.txt"
foln1 = "proj1"
foln1 = "./"+foln1+"/"
foln2 = "proj2"
foln2 = "./"+foln2+"/"
ht = open(filename,"r")
inp = [x.strip() for x in ht.readlines()]
print inp
urlList = [(x,x.split('=')[1].split('&')[0]+"-"+x.split('=')[2].split('&')[0]+".html") for x in inp ]
print urlList

app = QApplication(sys.argv)
downloader = Downloader(foln1,foln2,urlList)
downloader.done.connect(app.quit)
sys.exit(app.exec_())
