import os
from ftplib import FTP
from datetime import datetime, timedelta
import zipfile
from xml.dom import minidom


class FuncSpider:
    def __init__(self, p_location, p_login, p_pass, p_catalog_load):
        self.pLocation = p_location
        self.pLogin = p_login
        self.pPass = p_pass
        self.pCatalogLoad = p_catalog_load

    def ping_location(self):
        try:
            ftp = FTP()
            host = self.pLocation
            port = 21

            ftp.connect(host, port)
            ftp.login(self.pLogin, self.pPass)
            ftp.quit()
            ftp.close()
            return True
        except:
            return False

    def start_ftp(self):
        try:
            ftp = FTP()
            HOST = self.pLocation
            PORT = 21

            ftp.connect(HOST, PORT)
            ftp.login(self.pLogin, self.pPass)
            return ftp
        except:
            return False

    def get_list_regions43_fz(self):
        p_ftp = self.start_ftp()
        if not p_ftp:
            return []
        p_ftp.sendcmd('CWD fcs_regions')
        p_reg_list = []
        # print(p_ftp.retrlines('LIST'))
        # with open(self.pCatalogLoad + r'\regions.txt', 'wb') as f:
        p_ftp.retrbinary("RETR regions.txt", p_reg_list.append)
        p_ftp.quit()
        p_ftp.close()
        return p_reg_list

    def go_to_the_catalogs(self, p_list):
        for x in p_list:
            a = x.decode('UTF-8')
            a_spl = a.split()

        p_ftp = self.start_ftp()
        if not p_ftp:
            return []
        p_ftp.sendcmd('CWD fcs_regions')
        for x in a_spl:
            p_ftp.sendcmd(f'CWD {x}')
            p_reg_list = []
            p_ftp.sendcmd(f'CWD notifications/currMonth')
            p_zip = p_ftp.nlst()
            date_p = datetime.now()
            date_minus = datetime.now() - timedelta(1)
            date2 = date_p.strftime("%Y%m%d")
            date_minus = date_minus.strftime("%Y%m%d_")
            date_total = date_minus + date2

            list_downloads = [x for x in p_zip if x.find(date2) > 0]
            # print(p_ftp.retrlines('LIST'))
            # with open(self.pCatalogLoad + r'\regions.txt', 'wb') as f:
            for x in list_downloads:
                with open(self.pCatalogLoad + fr'\{x}', 'wb') as f:
                    p_ftp.retrbinary(f"RETR {x}", f.write)
            p_ftp.cwd('/fcs_regions')

            os.chdir(self.pCatalogLoad + r'\temp')

            for x in list_downloads:
                p_zip_file = self.pCatalogLoad + fr'\{x}'
                z = zipfile.ZipFile(p_zip_file, 'r')
                z.extractall()
                p_files = os.listdir(self.pCatalogLoad + r'\temp')
                for s in p_files:
                    if s[-3::] == 'xml':
                        pdoc = minidom.parse(s)
                        items = pdoc.getElementsByTagName('placingWay')
                        if len(items) == 0:
                            continue

        p_ftp.quit()
        p_ftp.close()

        return a_spl


g = FuncSpider('ftp.zakupki.gov.ru', 'free', 'free', r'C:\ftpload')

pL = g.get_list_regions43_fz()
g.go_to_the_catalogs(pL)
