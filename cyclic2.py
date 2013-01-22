#! /usr/bin/python
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
import lxml.html
import sys
import codecs
import time
class Downloader(QObject):
    done = Signal()

    def __init__(self,times,foln,foln2,urlList, parent = None):
        super(Downloader, self).__init__(parent)
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
							if y.text_content().encode('utf-8').strip('\n').find(',')!=-1 :
								wt.write('"'+y.text_content().encode('utf-8').strip('\n')+'"')
							else:
								wt.write(y.text_content().encode('utf-8').strip('\n'))
							wt.write(",")

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

filename = sys.argv[1]
foln = "output"
foln = "./"+foln+"/"
foln2 = "csvout"
foln2 = "./"+foln2+"/"
ht = open(filename,"r")
inp = [x.strip() for x in ht.readlines()]
urlList = [(x,x.split('=')[1]) for x in inp ]
w = filename
app = QApplication(sys.argv)
downloader = Downloader(5000,foln,foln2,urlList)
downloader.done.connect(app.quit)
#web = QWebView()
#web.setDisabled(True) 
#web.setPage(downloader.page)
#web.show()
sys.exit(app.exec_())
