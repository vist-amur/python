import datetime
import streamlit as st
from PIL import Image
import pymysql
import platform
import sys

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
def get_region(p_key, p_status = False):
    dict_regions = {'Altaj_Resp': 'Республика Алтай',
                    'Altajskij_kraj': 'Алтайский край',
                    'Amurskaja_obl': 'Амурская область',
                    'Arkhangelskaja_obl': 'Архангельская область',
                    'Astrakhanskaja_obl': 'Астраханская область',
                    'Bajkonur_g': 'Байконур',
                    'Bashkortostan_Resp': 'Республика Башкортостан',
                    'Belgorodskaja_obl': 'Белгородская область',
                    'Brjanskaja_obl': 'Брянская область',
                    'Burjatija_Resp': 'Республика Бурятия',
                    'Chechenskaja_Resp': 'Чеченская Республика',
                    'Cheljabinskaja_obl': 'Челябинская область',
                    'Chukotskij_AO': 'Чукотский автономный округ',
                    'Chuvashskaja_Resp': 'Чувашская Республика-Чувашия',
                    'Dagestan_Resp': 'Республика Дагестан',
                    'Evrejskaja_Aobl': 'Еврейская автономная область',
                    'Ingushetija_Resp': 'Республика Ингушетия',
                    'Irkutskaja_obl': 'Иркутская область',
                    'Ivanovskaja_obl': 'Ивановская область',
                    'Jamalo - Neneckij_AO': 'Ямало-Ненецкий автономный округ',
                    'Jaroslavskaja_obl': 'Ярославская область',
                    'Kabardino - Balkarskaja_Resp': 'Кабардино-Балкарская Республика',
                    'Kaliningradskaja_obl': 'Калининградская область',
                    'Kalmykija_Resp': 'Республика Калмыкия',
                    'Kaluzhskaja_obl': 'Калужская область',
                    'Kamchatskij_kraj': 'Камчатский край',
                    'Karachaevo - Cherkesskaja_Resp': 'Карачаево-Черкесская Республика',
                    'Karelija_Resp': 'Республика Карелия',
                    'Kemerovskaja_obl': 'Кемеровская область',
                    'Khabarovskij_kraj': 'Хабаровский край',
                    'Khakasija_Resp': 'Республика Хакасия',
                    'Khanty - Mansijskij_AO - Jugra_AO': 'Ханты-Мансийский автономный округ — Югра',
                    'Kirovskaja_obl': 'Кировская область',
                    'Komi_Resp': 'Республика Коми',
                    'Kostromskaja_obl': 'Костромская область',
                    'Krasnodarskij_kraj': 'Краснодарский край',
                    'Krasnojarskij_kraj': 'Красноярский край',
                    'Krim_Resp': 'Республика Крым',
                    'Kurganskaja_obl': 'Курганская область',
                    'Kurskaja_obl': 'Курская область',
                    'Leningradskaja_obl': 'Ленинградская область',
                    'Lipeckaja_obl': 'Липецкая область',
                    'Magadanskaja_obl': 'Магаданская область',
                    'Marij_El_Resp': 'Республика Марий Эл',
                    'Mordovija_Resp': 'Республика Мордовия',
                    'Moskovskaja_obl': 'Московская область',
                    'Moskva': 'Москва',
                    'Murmanskaja_obl': 'Мурманская область',
                    'Neneckij_AO': 'Ненецкий автономный округ',
                    'Nizhegorodskaja_obl': 'Нижегородская область',
                    'Novgorodskaja_obl': 'Новгородская область',
                    'Novosibirskaja_obl': 'Новосибирская область',
                    'Omskaja_obl': 'Омская область',
                    'Orenburgskaja_obl': 'Оренбургская область',
                    'Orlovskaja_obl': 'Орловская область',
                    'Penzenskaja_obl': 'Пензенская область',
                    'Permskij_kraj': 'Пермский край',
                    'Primorskij_kraj': 'Приморский край',
                    'Pskovskaja_obl': 'Псковская область',
                    'Rjazanskaja_obl': 'Рязанская область',
                    'Rostovskaja_obl': 'Ростовская область',
                    'Sakha_Jakutija_Resp': 'Республика Саха (Якутия)',
                    'Sakhalinskaja_obl': 'Сахалинская область',
                    'Samarskaja_obl': 'Самарская область',
                    'Sankt - Peterburg': 'Санкт-Петербург',
                    'Saratovskaja_obl': 'Саратовская область',
                    'Sevastopol_g': 'Севастополь',
                    'Severnaja_Osetija - Alanija_Resp': 'Республика Северная Осетия — Алания',
                    'Smolenskaja_obl': 'Смоленская область',
                    'Stavropolskij_kraj': 'Ставропольский край',
                    'Sverdlovskaja_obl': 'Свердловская область',
                    'Tambovskaja_obl': 'Тамбовская область',
                    'Tatarstan_Resp': 'Республика Татарстан',
                    'Tjumenskaja_obl': 'Тюменская область',
                    'Tomskaja_obl': 'Томская область',
                    'Tulskaja_obl': 'Тульская область',
                    'Tverskaja_obl': 'Тверская область',
                    'Tyva_Resp': 'Республика Тыва',
                    'Udmurtskaja_Resp': 'Удмуртская Республика',
                    'Uljanovskaja_obl': 'Ульяновская область',
                    'Vladimirskaja_obl': 'Владимирская область',
                    'Volgogradskaja_obl': 'Волгоградская область',
                    'Vologodskaja_obl': 'Вологодская область',
                    'Voronezhskaja_obl': 'Воронежская область',
                    'Zabajkalskij_kraj': 'Забайкальский край'}
    if p_status:
        return dict_regions.values()
    for key, value in dict_regions.items():
        if value == p_key:
            return key
    return ""

def main():
    p_address = sys.argv[1]
    p_loginDB = sys.argv[2]
    p_passDB = sys.argv[3]
    p_nameDB = sys.argv[4]
    p_nametable = sys.argv[5]
    p_logo = sys.argv[6]
    p_name_logo = sys.argv[7]
    p_css = sys.argv[8]
    p_name_css = sys.argv[9]


    p_slash = ''
    p_os = platform.system().lower()
    if "win" in p_os:
        p_slash = '\\'
    else:
        p_slash = '/'

    try:
        image_directory = fr"{p_logo}{p_slash}{p_name_logo}"
        image = Image.open(fr'{image_directory}')
    finally:
        image = Image.new(mode="RGB", size=(120, 120))

    PAGE_CONFIG = {"page_title":"База данных извещений с сайта zakupki.gov.ru",
                   "page_icon":image,
                   "layout":"centered",
                   "initial_sidebar_state":"auto"}

    st.set_page_config(**PAGE_CONFIG)

    connection = pymysql.connect(host=p_address, user=p_loginDB, passwd=p_passDB, database=p_nameDB)

    selected_regions = st.sidebar.multiselect("Регионы РФ", get_region('',True))
    date_start = st.sidebar.date_input('Период размещения заявок:',[datetime.datetime.now() - datetime.timedelta(1), datetime.datetime.now()])
    like_words = st.sidebar.text_input('Ключевые фразы объекта закупки, указанные через запятую:')
    list_like_words = like_words.split(',')
    with st.echo():
        st.write(selected_regions)
    with st.echo():
        st.write(list_like_words)
    sql_like_words = ''
    ind = 0
    if len(list_like_words) > 0:
        if list_like_words[0] != "":
            for x in list_like_words:
                if ind == 0:
                    sql_like_words = sql_like_words + f' AND (subject_purchase LIKE \'%{x}%\''
                else:
                    sql_like_words = sql_like_words + f' OR subject_purchase LIKE \'%{x}%\''
                ind += 1
            sql_like_words = sql_like_words + ')'
        else:
            sql_like_words = ''


    sql_regions = []
    p_sql_regions = ""
    p_sql_regions_pre = " AND region IN ("
    if len(selected_regions) > 0:
        sql_regions = [f"\'{get_region(x)}\'" for x in selected_regions if get_region(x) != "" f"'{get_region(x)}'"]
        p_sql_regions = ",".join(sql_regions) + ')'
    else:
        p_sql_regions = ""
        p_sql_regions_pre = ""
        #sql_regions = sql_regions + f' AND region IN ({sql_regions})'
    #SELECT * FROM `notifications` WHERE `date_publish` BETWEEN '2021-12-13' AND '2021-12-13'
    #AND `region` IN () AND `subject_purchase`LIKE ''
    cursor = connection.cursor()
    sql = f"Select * from {p_nametable} where date_publish BETWEEN '{date_start[0]}' AND '{date_start[-1]}'{p_sql_regions_pre}{p_sql_regions}{sql_like_words}"
    cursor.execute(sql)
    with st.echo():
        st.write(sql)

    AllRow = cursor.fetchmany(25)

    with st.echo():
        st.write(AllRow)

    load_css(fr'{p_css}{p_slash}{p_name_css}')


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Parameters are not specified!')
    elif len(sys.argv) == 2:
        decryption_of_parameters()
    else:
        main()