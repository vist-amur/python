import datetime
import streamlit as st
from PIL import Image
import pymysql
import platform

def load_css(file_name:str):
    '''
        Function to load and render a local stylesheet
    '''
    with open(file_name) as f:
        d = f.read()
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def decryption_of_parameters():
    print('Разбор параметров '
           '1.Адрес БД; 2.Пользователь БД; 3.Пароль пользователя БД; 4.Имя БД; 5.Имя таблицы извещений)')
    print(r'Пример: 94.228.121.182 phpmyadmin pass goszakupki '
          'notifications')

def main():
    p_loginDB = sys.argv[1]
    p_passDB = sys.argv[2]
    p_nameDB = sys.argv[3]
    p_nametable = sys.argv[4]
    p_logo = sys.argv[5]
    p_name_logo = sys.argv[6]
    p_css = sys.argv[7]
    p_name_css = sys.argv[8]

    p_slash = ''
    p_os = platform.system().lower()
    if "win" in p_os:
        p_slash = '\\'
    else:
        p_slash = '/'

    try:
        image_directory = fr"{p_logo}{p_slash}{p_name_logo}"
        image = Image.open(image_directory)
    finally:
        image = Image.new(mode="RGB", size=(120, 120))

    PAGE_CONFIG = {"page_title":"База данных извещений с сайта zakupki.gov.ru",
                   "page_icon":image,
                   "layout":"centered",
                   "initial_sidebar_state":"auto"}

    st.set_page_config(**PAGE_CONFIG)

    selected_regions = st.sidebar.multiselect("Регионы РФ", ['Амурская область', 'Хабаровский край'])
    date_start = st.sidebar.date_input('Период размещения заявок:',[datetime.datetime.now() - datetime.timedelta(1), datetime.datetime.now()])
    like_words = st.sidebar.text_input('Ключевые фразы, указанные через запятую:')

    connection = pymysql.connect(host=p_addressDB, user=p_loginDB, passwd=p_passDB, database=p_nameDB)
    #SELECT * FROM `notifications` WHERE `date_publish` BETWEEN '2021-12-13' AND '2021-12-13'
    #AND `region` IN () AND `subject_purchase`LIKE ''
    cursor = connection.cursor()
    sql = f"Select * from {p_nametable} where num_notification LIKE '{niz}'"
    cursor.execute(sql)

    oneRow = cursor.fetchone()

    load_css(fr'{p_css}{p_slash}{p_name_css}')


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Parameters are not specified!')
    elif len(sys.argv) == 2:
        decryption_of_parameters()
    else:
        main(True)