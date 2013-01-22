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
import lxml.html

class Downloader2(QObject):
    done = Signal()

    def __init__(self,times,foln,foln2,urlList, parent = None):
        super(Downloader2, self).__init__(parent)
        self.urlList = urlList
        self.foln = foln
        self.foln2 = foln2
        self.time = times
        self.counter = 0        

        self.ctimer = QTimer()
        self.connect(self.ctimer, SIGNAL("timeout()"), self.save)
        self.page = QWebPage(self)      
        #self.page.loadFinished.connect(self.save)
        #self.connect(self, SIGNAL('loadFinished(bool)'), self.save) 
        self.page.mainFrame().load(self.currentUrl())
        time.sleep(1)
        self.startNext()
	

    def currentUrl(self):
        return self.urlList[self.counter][0]

    def currentFilename(self):
        return self.urlList[self.counter][1]

    def startNext(self):
        print "Downloading %s..."%self.currentUrl()
        self.page.mainFrame().load(self.currentUrl())
        self.ctimer.start(self.time)

    def save(self, ok=True):
        if ok:            
            #time.sleep(10)
            data = self.page.mainFrame().toHtml()
            with codecs.open(self.foln+self.currentFilename()+".html", encoding="utf-8", mode="w") as f:
                f.write(data)
            wt = open(self.foln2+self.currentFilename()+".csv","w")
            doc = lxml.html.fromstring(data) 
            table = doc.xpath('//*[@class="grid smallSpaceGrid"]')
            for row in table:
				for col in row:
					for x in col:
						for y in x:
							wt.write(y.text_content().encode('utf-8').strip('\n'))
							wt.write(";")

						wt.write("\n")
            wt.close()

            print "Saving %s to %s."%(self.currentUrl(), self.currentFilename())            
        else:
            print "Error while downloading %s\nSkipping."%self.currentUrl()
        self.counter += 1
        if self.counter < len(self.urlList):            
            self.startNext()
        else:
            self.done.emit()

class Downloader1(QObject):
    done = Signal()

    def __init__(self,filen, urlList, parent = None):
        super(Downloader1, self).__init__(parent)
        self.urlList = urlList
        self.filen = filen
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
            fil1 = open(w[0:w.rfind('.')]+".txt","w")
            d = fromstring(data)
            sel = CSSSelector("td[class=dog] a")
            for e in sel(d):
				fil1.write(e.get('href')+"\n")
            fil1.close()
            with codecs.open(self.currentFilename(), encoding="utf-8", mode="w") as f:
                f.write(data)
            print "Saving %s to %s."%(self.currentUrl(), self.currentFilename())            

            w = self.currentFilename()
            self.filename1 = w[0:w.rfind('.')]+".txt"
            self.foln = "output"
            self.foln = "./"+foln+"/"
            self.foln2 = "csvout"
            self.foln2 = "./"+self.foln2+"/"
            self.ht = open(self.filename1,"r")
            inp = [x.strip() for x in self.ht.readlines()]
            self.urlList = [(x,x.split('=')[1]) for x in inp ]
            #app2 = QApplication(sys.argv)
            downloader2 = Downloader2(5000,self.foln,self.foln2,self.urlList)
            #downloader2.done.connect(app.quit)
#web = QWebView()
#web.setDisabled(True) 
#web.setPage(downloader.page)
#web.show()
        #app2.exec_()
        else:
            print "Error while downloading %s\nSkipping."%self.currentUrl()



        self.counter += 1
        if self.counter < len(self.urlList):            
            self.startNext()
        else:
            self.done.emit()
if __name__ == '__main__' :
	filename = "him.txt"
	foldername = "proj1"
	foldername = "./"+foldername+"/"
	ht = open(filename,"r")
	inp = [x.strip() for x in ht.readlines()]
	print inp
	urlList = [(x,foldername+x.split('=')[1].split('&')[0]+"-"+x.split('=')[2].split('&')[0]+".html") for x in inp ]
	print urlList

	app = QApplication(sys.argv)
	downloader = Downloader1("old",urlList)
	downloader.done.connect(app.quit)
	sys.exit(app.exec_())
