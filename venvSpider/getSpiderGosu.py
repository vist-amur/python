import os
import sys
from ftplib import FTP
from datetime import datetime, timedelta
import zipfile
from xml.dom import minidom
from pathlib import Path
import pymysql
import traceback


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

    def start_ftp(self, tout = 0, pcatalog = ('none')):
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

    def get_list_regions223_fz(self):
        p_ftp = self.start_ftp()
        if not p_ftp:
            return []
        p_ftp.sendcmd('CWD out/published')
        p_reg_list = []
        # print(p_ftp.retrlines('LIST'))
        # with open(self.pCatalogLoad + r'\regions.txt', 'wb') as f:
        p_ftp.retrbinary("RETR list_regions.txt", p_reg_list.append)
        p_ftp.quit()
        p_ftp.close()
        return p_reg_list

    def get_list_catalog_regions223_fz(self):
        #p_ftp = self.start_ftp()
        #if not p_ftp:
        #    return []
        #p_ftp.sendcmd('CWD published')
        p_reg_list = ['purchaseNotice', 'purchaseNoticeAE', 'purchaseNoticeAE94',
                      'purchaseNoticeAESMBO', 'purchaseNoticeEP', 'purchaseNoticeIS',
                      'purchaseNoticeKESMBO', 'purchaseNoticeOA', 'purchaseNoticeOK',
                      'purchaseNoticeZK', 'purchaseNoticeZKESMBO', 'purchaseNoticeZPESMBO']
        # print(p_ftp.retrlines('LIST'))
        # with open(self.pCatalogLoad + r'\regions.txt', 'wb') as f:
        #p_ftp.retrbinary("RETR list_catalog.txt", p_reg_list.append)
        #p_ftp.quit()
        #p_ftp.close()
        return p_reg_list

    def go_to_the_catalogs(self, p_list):
        total_list_to_sql = []
        for x in p_list:
            a = x.decode('UTF-8')
            a_spl = a.split()

        p_ftp = self.start_ftp()
        if not p_ftp:
            return []
        p_ftp.sendcmd('CWD fcs_regions')
        for xcat in a_spl:
            p_ftp.sendcmd(f'CWD {xcat}')
            p_ftp.sendcmd(f'CWD notifications/currMonth')
            p_zip = p_ftp.nlst()
            date_p = datetime.now()
            date_minus = datetime.now() - timedelta(1)
            date2 = date_p.strftime("%Y%m%d")
            date_minus = date_minus.strftime("%Y%m%d")
            date_total = date_minus + date2

            list_downloads = [x for x in p_zip if x.find(date_minus) > 0 or x.find(date2) > 0]
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
                        if s.find('Clarification') > -1:
                            continue
                        if s.find('Cancel') > -1:
                            continue
                        p_reg_list = {}
                        p_ntag = ''
                        p_natrr = ''
                        try:
                            pdoc = minidom.parse(s)
                        except:
                            continue
                        # items = pdoc.getElementsByTagName('placingWay')
                        # if len(items) == 0:
                        #    continue
                        p_reg_list['дата_создания'] = str(datetime.today())
                        p_reg_list['фз'] = '44-ФЗ'
                        p_reg_list['регион'] = xcat

                        # tag placingWay - start
                        items = pdoc.getElementsByTagName('placingWay')
                        if len(items) > 0:
                            for el in items:
                                name_obj = el.getElementsByTagName("name")[0]
                            for xi in range(0, 1):
                                nodes = name_obj.childNodes
                                for node in nodes:
                                    if node.nodeType == node.TEXT_NODE:
                                        p_reg_list['тип_фз'] = node.data
                        else:
                            items = pdoc.getElementsByTagName('ns9:placingWay')
                            if len(items) > 0:
                                p_ntag = 'ns9:'
                                p_natrr = 'ns4:'
                                for el in items:
                                    name_obj = el.getElementsByTagName("ns4:name")[0]
                                for xi in range(0, 1):
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['тип_фз'] = node.data

                        if 'тип_фз' not in p_reg_list:
                            p_reg_list['тип_фз'] = 'Неопределено'
                        # finish

                        # tag PublishDate - start
                        items = pdoc.getElementsByTagName(p_ntag + 'plannedPublishDate')
                        # for el in items:
                        #    name_obj = el.getElementsByTagName(p_natrr + "name")[0]
                        if len(items) > 0:
                            for name_obj in items:
                                nodes = name_obj.childNodes
                                for node in nodes:
                                    if node.nodeType == node.TEXT_NODE:
                                        p_reg_list['дата_размещения'] = node.data
                        if 'дата_размещения' not in p_reg_list:
                            items = pdoc.getElementsByTagName(p_ntag + 'docPublishDate')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['дата_размещения'] = node.data
                        if 'дата_размещения' not in p_reg_list:
                            p_reg_list['дата_размещения'] = '1970-01-01'
                        # finish

                        # tag endDT - start
                        items = pdoc.getElementsByTagName(p_ntag + 'endDT')
                        if len(items) > 0:
                            for name_obj in items:
                                nodes = name_obj.childNodes
                                for node in nodes:
                                    if node.nodeType == node.TEXT_NODE:
                                        p_reg_list['дата_окончания'] = node.data

                        if 'дата_окончания' not in p_reg_list:
                            items = pdoc.getElementsByTagName(p_ntag + 'endDate')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['дата_окончания'] = node.data
                        if 'дата_окончания' not in p_reg_list:
                            p_reg_list['дата_окончания'] = '1970-01-01'
                        # finish

                        # tag purchaseNumber - start
                        items = pdoc.getElementsByTagName(p_ntag + 'purchaseNumber')
                        if len(items) > 0:
                            for name_obj in items:
                                nodes = name_obj.childNodes
                                for node in nodes:
                                    if node.nodeType == node.TEXT_NODE:
                                        p_reg_list['номер_извещения'] = node.data
                                break

                        if 'номер_извещения' not in p_reg_list:
                            p_reg_list['номер_извещения'] = 'Неопределено'
                        # finish

                        # tag href - start
                        items = pdoc.getElementsByTagName(p_ntag + 'href')
                        if len(items) > 0:
                            for name_obj in items:
                                nodes = name_obj.childNodes
                                for node in nodes:
                                    if node.nodeType == node.TEXT_NODE:
                                        p_reg_list['ссылка_на_сайт'] = node.data

                        if 'ссылка_на_сайт' not in p_reg_list:
                            p_reg_list['ссылка_на_сайт'] = 'Неопределено'
                        # finish

                        # tag purchaseObjectInfo - start
                        items = pdoc.getElementsByTagName(p_ntag + 'purchaseObjectInfo')
                        if len(items) > 0:
                            for name_obj in items:
                                nodes = name_obj.childNodes
                                for node in nodes:
                                    if node.nodeType == node.TEXT_NODE:
                                        p_reg_list['объект_закупки'] = node.data

                        if 'объект_закупки' not in p_reg_list:
                            p_reg_list['объект_закупки'] = 'Неопределено'
                        # finish

                        # tag PostAddress - start
                        items = pdoc.getElementsByTagName(p_ntag + 'orgPostAddress')
                        if len(items) > 0:
                            for name_obj in items:
                                nodes = name_obj.childNodes
                                for node in nodes:
                                    if node.nodeType == node.TEXT_NODE:
                                        p_reg_list['адрес_заказчика'] = node.data

                        if 'адрес_заказчика' not in p_reg_list:
                            items = pdoc.getElementsByTagName(p_ntag + 'postAddress')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['адрес_заказчика'] = node.data
                        if 'адрес_заказчика' not in p_reg_list:
                            p_reg_list['адрес_заказчика'] = 'Неопределено'
                        # finish

                        # tag fullName - start
                        items = pdoc.getElementsByTagName(p_ntag + 'fullName')
                        if len(items) > 0:
                            for name_obj in items:
                                nodes = name_obj.childNodes
                                for node in nodes:
                                    if node.nodeType == node.TEXT_NODE:
                                        p_reg_list['заказчик'] = node.data
                                break

                        if 'заказчик' not in p_reg_list:
                            p_reg_list['заказчик'] = 'Неопределено'
                        # finish

                        # tag maxPrice - start
                        items = pdoc.getElementsByTagName(p_ntag + 'maxPrice')
                        if len(items) > 0:
                            for name_obj in items:
                                nodes = name_obj.childNodes
                                for node in nodes:
                                    if node.nodeType == node.TEXT_NODE:
                                        p_reg_list['начальная_цена'] = node.data
                                break

                        if 'начальная_цена' not in p_reg_list:
                            p_reg_list['начальная_цена'] = '0'
                        # finish

                        total_list_to_sql.append(p_reg_list)
                path = Path(self.pCatalogLoad + r'\temp')
                for p in path.glob('*.xml'):
                    p.unlink()
                for p in path.glob('*.sig'):
                    p.unlink()
            z.close()
            path = Path(self.pCatalogLoad)
            for p in path.glob('*.zip'):
                p.unlink()

        #p_ftp.quit()
        p_ftp.close()

        return total_list_to_sql

    def go_to_the_catalogs223fz(self, p_list, p_catalog):
        total_list_to_sql = []
        for x in p_list:
            a = x.decode('UTF-8')
            a_spl = a.split()
        #for x in p_catalog:
        #    a = x.decode('UTF-8')
        #    a_catalog = a.split()

        p_ftp = self.start_ftp()
        if not p_ftp:
            return []
        p_ftp.sendcmd('CWD out/published')
        for xcat in a_spl:
            op_catalog = p_ftp.pwd()
            if 'published/' in op_catalog:
                p_ftp.sendcmd(f'CWD /out/published')
            p_ftp.sendcmd(f'CWD {xcat}')
            for xlistcatalog in p_catalog:
                try:
                    p_ftp.sendcmd(f'CWD {xlistcatalog}/daily')
                except:
                    p_ftp.cwd(f'/out/published/{xcat}')
                    continue
                p_zip = p_ftp.nlst()
                date_p = datetime.now()
                date_minus = datetime.now() - timedelta(1)
                date2 = date_p.strftime("%Y%m%d")
                date_minus = date_minus.strftime("%Y%m%d")
                date_total = date_minus + date2

                list_downloads = [x for x in p_zip if x.find(date_minus) > 0 or x.find(date2) > 0]
                # print(p_ftp.retrlines('LIST'))
                # with open(self.pCatalogLoad + r'\regions.txt', 'wb') as f:
                for x in list_downloads:
                    with open(self.pCatalogLoad + fr'\{x}', 'wb') as f:
                        p_ftp.retrbinary(f"RETR {x}", f.write)

                p_ftp.cwd(f'/out/published/{xcat}')

                os.chdir(self.pCatalogLoad + r'\temp')

                for x in list_downloads:
                    p_zip_file = self.pCatalogLoad + fr'\{x}'
                    z = zipfile.ZipFile(p_zip_file, 'r')
                    z.extractall()
                    p_files = os.listdir(self.pCatalogLoad + r'\temp')

                    for s in p_files:

                        if s[-3::] == 'xml':
                            if s.find('Clarification') > -1:
                                continue
                            if s.find('Cancel') > -1:
                                continue
                            p_reg_list = {}
                            p_ntag = ''
                            p_natrr = ''
                            try:
                                pdoc = minidom.parse(s)
                            except:
                               continue
                            # items = pdoc.getElementsByTagName('placingWay')
                            # if len(items) == 0:
                            #    continue
                            p_reg_list['дата_создания'] = str(datetime.today())
                            p_reg_list['фз'] = '223-ФЗ'
                            p_reg_list['регион'] = xcat

                            # tag placingWay - start
                            items = pdoc.getElementsByTagName(p_ntag + 'ns2:purchaseCodeName')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['тип_фз'] = node.data

                            if 'тип_фз' not in p_reg_list:
                                p_reg_list['тип_фз'] = 'Неопределено'
                            # finish

                            # tag PublishDate - start
                            items = pdoc.getElementsByTagName(p_ntag + 'plannedPublishDate')
                            # for el in items:
                            #    name_obj = el.getElementsByTagName(p_natrr + "name")[0]
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['дата_размещения'] = node.data
                            if 'дата_размещения' not in p_reg_list:
                                items = pdoc.getElementsByTagName(p_ntag + 'deliveryStartDateTime')
                                if len(items) > 0:
                                    for name_obj in items:
                                        nodes = name_obj.childNodes
                                        for node in nodes:
                                            if node.nodeType == node.TEXT_NODE:
                                                p_reg_list['дата_размещения'] = node.data
                            if 'дата_размещения' not in p_reg_list:
                                p_reg_list['дата_размещения'] = '1970-01-01'
                            # finish

                            # tag endDT - start
                            items = pdoc.getElementsByTagName(p_ntag + 'deliveryEndDateTime')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['дата_окончания'] = node.data

                            if 'дата_окончания' not in p_reg_list:
                                items = pdoc.getElementsByTagName(p_ntag + 'endDate')
                                if len(items) > 0:
                                    for name_obj in items:
                                        nodes = name_obj.childNodes
                                        for node in nodes:
                                            if node.nodeType == node.TEXT_NODE:
                                                p_reg_list['дата_окончания'] = node.data
                            if 'дата_окончания' not in p_reg_list:
                                p_reg_list['дата_окончания'] = '1970-01-01'
                            # finish

                            # tag purchaseNumber - start
                            items = pdoc.getElementsByTagName(p_ntag + 'ns2:registrationNumber')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['номер_извещения'] = node.data
                                    break

                            if 'номер_извещения' not in p_reg_list:
                                p_reg_list['номер_извещения'] = 'Неопределено'
                            # finish

                            # tag href - start
                            #items = pdoc.getElementsByTagName(p_ntag + 'href')
                            #if len(items) > 0:
                            #    for name_obj in items:
                            #        nodes = name_obj.childNodes
                            #        for node in nodes:
                            #            if node.nodeType == node.TEXT_NODE:
                            #                p_reg_list['ссылка_на_сайт'] = node.data
                            if p_reg_list['номер_извещения'] != 'Неопределено':
                                p_reg_list['ссылка_на_сайт'] = r'https://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?regNumber=' + p_reg_list['номер_извещения']
                            else:
                                p_reg_list['ссылка_на_сайт'] = 'Неопределено'
                            # finish

                            # tag purchaseObjectInfo - start
                            items = pdoc.getElementsByTagName(p_ntag + 'ns2:name')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['объект_закупки'] = node.data

                            if 'объект_закупки' not in p_reg_list:
                                p_reg_list['объект_закупки'] = 'Неопределено'
                            # finish

                            # tag PostAddress - start
                            items = pdoc.getElementsByTagName(p_ntag + 'legalAddress')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['адрес_заказчика'] = node.data
                                    break
                            if 'адрес_заказчика' not in p_reg_list:
                                items = pdoc.getElementsByTagName(p_ntag + 'postAddress')
                                if len(items) > 0:
                                    for name_obj in items:
                                        nodes = name_obj.childNodes
                                        for node in nodes:
                                            if node.nodeType == node.TEXT_NODE:
                                                p_reg_list['адрес_заказчика'] = node.data
                            if 'адрес_заказчика' not in p_reg_list:
                                p_reg_list['адрес_заказчика'] = 'Неопределено'
                            # finish

                            # tag fullName - start
                            items = pdoc.getElementsByTagName(p_ntag + 'fullName')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['заказчик'] = node.data
                                    break

                            if 'заказчик' not in p_reg_list:
                                p_reg_list['заказчик'] = 'Неопределено'
                            # finish

                            # tag maxPrice - start
                            items = pdoc.getElementsByTagName(p_ntag + 'initialSum')
                            if len(items) > 0:
                                for name_obj in items:
                                    nodes = name_obj.childNodes
                                    for node in nodes:
                                        if node.nodeType == node.TEXT_NODE:
                                            p_reg_list['начальная_цена'] = node.data
                                    break

                            if 'начальная_цена' not in p_reg_list:
                                p_reg_list['начальная_цена'] = '0'
                            # finish

                            total_list_to_sql.append(p_reg_list)
                    path = Path(self.pCatalogLoad + r'\temp')
                    for p in path.glob('*.xml'):
                       p.unlink()
                    for p in path.glob('*.sig'):
                        p.unlink()
                try:
                    z.close()
                except:
                    print('Connected was closed!')

            path = Path(self.pCatalogLoad)
            for p in path.glob('*.zip'):
                p.unlink()

        #p_ftp.quit()
        p_ftp.close()

        return total_list_to_sql


def main(inner=False):
    if len(sys.argv) == 0:
        print('Parametres not found!')
        return False
    # Разбор параметров
    # 1.FTP сайта госзакупок; 2.Логин; 3. Пароль; 4. Временный каталог для распаковки скачанных архивов
    # 5.Адрес БД; 6.Пользователь БД; 7.Пароль пользователя БД; 8.Имя БД; 9.Имя таблицы извещений
    if inner:
        g = FuncSpider('ftp.zakupki.gov.ru', 'free', 'free', r'C:\ftpload')

        pL = g.get_list_regions43_fz()
        p_list_notifications = g.go_to_the_catalogs(pL)
        print(len(p_list_notifications))
        #p_list_notifications = [{'дата_создания': '2021-12-10 15:15:52.030514', 'тип_фз': 'Электронный аукцион',
        #                     'дата_размещения': '2021-12-08T16:28:48.649+07:00',
        #                         'дата_окончания': '2021-12-16T23:59:00+07:00',
        #                         'номер_извещения': '0177100001321000020',
        #                         'ссылка_на_сайт': 'https://zakupki.gov.ru/epz/order/notice/ea44/view/common-info.html?regNumber=0177100001321000020',
        #                         'объект_закупки': 'Подписка на периодические издания и услуги по доставке ',
        #                         'адрес_заказчика': 'Российская Федерация, 649000, Алтай Респ, Горно-Алтайск г, Ленкина ул, 4',
        #                         'заказчик': 'АРБИТРАЖНЫЙ СУД РЕСПУБЛИКИ АЛТАЙ', 'начальная_цена': '123510.69'}]
        connection = pymysql.connect(host="94.228.121.182", user="phpmyadmin", passwd="g7A1PuDN", database="goszakupki")
        for x in p_list_notifications:
            try:
                cursor = connection.cursor()
                niz = x["номер_извещения"]
                sql = f"Select * from notifications where num_notification LIKE '{niz}'"
                cursor.execute(sql)

                oneRow = cursor.fetchone()

                if oneRow == None:
                    cursor = connection.cursor()
                    sql = 'INSERT INTO notifications (date, fz, region, type_fz, ' \
                          'date_publish, date_finish, num_notification, ref, ' \
                          'subject_purchase, customer, address_customer, price) ' \
                          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    cursor.execute(sql, (datetime.strptime(x["дата_создания"], '%Y-%m-%d %H:%M:%S.%f'), x["фз"], x["регион"], x["тип_фз"] , datetime.strptime(x["дата_размещения"][0:10], '%Y-%m-%d'), datetime.strptime(x["дата_окончания"][0:10], '%Y-%m-%d'),
                                         x["номер_извещения"], x["ссылка_на_сайт"], x["объект_закупки"], x["адрес_заказчика"],
                                         x["заказчик"], float(x["начальная_цена"])))
                    connection.commit()
            except:
                connection.close()
                with open(r'D:\trace.txt', 'a') as fp:
                    traceback.print_exc(file=fp)
                    # повторный вызов исключения, если это необходимо.
                raise
                break

        try:
            connection.close()
        except:
            print('Connected was closed!')
        del g
        del pL
        del p_list_notifications
        del  connection
    # 223-ФЗ
    if inner:
        g = FuncSpider('ftp.zakupki.gov.ru', 'fz223free', 'fz223free', r'C:\ftpload')

        pL = g.get_list_regions223_fz()
        p_list_notifications = g.go_to_the_catalogs223fz(pL, g.get_list_catalog_regions223_fz())
        print(len(p_list_notifications))
        #p_list_notifications = [{'дата_создания': '2021-12-10 15:15:52.030514', 'тип_фз': 'Электронный аукцион',
        #                     'дата_размещения': '2021-12-08T16:28:48.649+07:00',
        #                         'дата_окончания': '2021-12-16T23:59:00+07:00',
        #                         'номер_извещения': '0177100001321000020',
        #                         'ссылка_на_сайт': 'https://zakupki.gov.ru/epz/order/notice/ea44/view/common-info.html?regNumber=0177100001321000020',
        #                         'объект_закупки': 'Подписка на периодические издания и услуги по доставке ',
        #                         'адрес_заказчика': 'Российская Федерация, 649000, Алтай Респ, Горно-Алтайск г, Ленкина ул, 4',
        #                         'заказчик': 'АРБИТРАЖНЫЙ СУД РЕСПУБЛИКИ АЛТАЙ', 'начальная_цена': '123510.69'}]
        connection = pymysql.connect(host="94.228.121.182", user="phpmyadmin", passwd="g7A1PuDN", database="goszakupki")
        for x in p_list_notifications:
            try:
                cursor = connection.cursor()
                niz = x["номер_извещения"]
                sql = f"Select * from notifications where num_notification LIKE '{niz}'"
                cursor.execute(sql)

                oneRow = cursor.fetchone()

                if oneRow == None:
                    cursor = connection.cursor()
                    sql = 'INSERT INTO notifications (date, fz, region, type_fz, ' \
                          'date_publish, date_finish, num_notification, ref, ' \
                          'subject_purchase, customer, address_customer, price) ' \
                          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    cursor.execute(sql, (datetime.strptime(x["дата_создания"], '%Y-%m-%d %H:%M:%S.%f'), x["фз"], x["регион"], x["тип_фз"] , datetime.strptime(x["дата_размещения"][0:10], '%Y-%m-%d'), datetime.strptime(x["дата_окончания"][0:10], '%Y-%m-%d'),
                                         x["номер_извещения"], x["ссылка_на_сайт"], x["объект_закупки"], x["адрес_заказчика"],
                                         x["заказчик"], float(x["начальная_цена"])))
                    connection.commit()
            except:
                connection.close()
                with open(r'D:\trace.txt', 'a') as fp:
                    traceback.print_exc(file=fp)
                    # повторный вызов исключения, если это необходимо.
                raise
                break

        try:
            connection.close()
        except:
            print('Connected was closed!')

if __name__ == "__main__":
    main(True)
