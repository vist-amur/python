import os
from ftplib import FTP
from datetime import datetime, timedelta
import zipfile
from xml.dom import minidom

class funcSpider():
    def __init__(self, pLocation, pLogin, pPass, pCatalogLoad):
        self.pLocation = pLocation
        self.pLogin = pLogin
        self.pPass = pPass
        self.pCatalogLoad = pCatalogLoad

    def pingLocation(self):
        try:
            ftp = FTP()
            HOST = self.pLocation
            PORT = 21

            ftp.connect(HOST, PORT)
            ftp.login(self.pLogin, self.pPass)
            ftp.quit()
            ftp.close()
            return True
        except:
            return False

    def startFTP(self):
        try:
            ftp = FTP()
            HOST = self.pLocation
            PORT = 21

            ftp.connect(HOST, PORT)
            ftp.login(self.pLogin, self.pPass)
            return ftp
        except:
            return False

    def getListRegions43FZ(self):
        pFTP = self.startFTP()
        if not pFTP:
            return []
        pFTP.sendcmd('CWD fcs_regions')
        pRegList = []
        #print(pFTP.retrlines('LIST'))
        # with open(self.pCatalogLoad + r'\regions.txt', 'wb') as f:
        pFTP.retrbinary("RETR regions.txt", pRegList.append)
        pFTP.quit()
        pFTP.close()
        return pRegList

    def goToTheCatalogs(self, pList):
        for x in pList:
            a = x.decode('UTF-8')
            aSPL = a.split()

        pFTP = self.startFTP()
        if not pFTP:
            return []
        pFTP.sendcmd('CWD fcs_regions')
        for x in aSPL:
            pFTP.sendcmd(f'CWD {x}')
            pRegList = []
            pFTP.sendcmd(f'CWD notifications/currMonth')
            pLzip = pFTP.nlst()
            dateP = datetime.now()
            dateMinus = datetime.now() - timedelta(1)
            date2 = dateP.strftime("%Y%m%d")
            dateMinus = dateMinus.strftime("%Y%m%d_")
            dateTotal = dateMinus + date2

            listDownloads = [x for x in pLzip if x.find(date2) > 0]
            #print(pFTP.retrlines('LIST'))
            # with open(self.pCatalogLoad + r'\regions.txt', 'wb') as f:
            for x in listDownloads:
                with open(self.pCatalogLoad + fr'\{x}', 'wb') as f:
                    pFTP.retrbinary(f"RETR {x}", f.write)
            pFTP.cwd('/fcs_regions')

            os.chdir(self.pCatalogLoad + r'\temp')

            for x in listDownloads:
                pZipFile = self.pCatalogLoad + fr'\{x}'
                z = zipfile.ZipFile(pZipFile, 'r')
                z.extractall()
                pFiles = os.listdir(self.pCatalogLoad + r'\temp')
                for s in pFiles:
                    if s[-3::] == 'xml':
                        pdoc = minidom.parse(s)
                        items = pdoc.getElementsByTagName('postAddress')

        pFTP.quit()
        pFTP.close()

        return aSPL


g = funcSpider('ftp.zakupki.gov.ru', 'free', 'free', r'C:\ftpload')

pL = g.getListRegions43FZ()
g.goToTheCatalogs(pL)