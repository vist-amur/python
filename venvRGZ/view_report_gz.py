import base64
import datetime
import streamlit as st
from PIL import Image
import pymysql
import platform
import sys
import plotly.express as px
import plotly.graph_objects as go
from altair.vega import alignValue
import pandas as pd
import csv

# comment
def load_css(file_name: str):
    '''
        Function to load and render a local stylesheet
    '''
    with open(file_name) as f:
        d = f.read()
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def decryption_of_parameters():
    print('Разбор параметров '
          '1.Адрес БД; 2.Пользователь БД; 3.Пароль пользователя БД; 4.Имя БД; 5.Имя таблицы извещений)')
    print(r'Пример: 94.228.121.182 phpmyadmin pass goszakupki notifications '
          r'C:\Users\User\PycharmProjects\pythonProject\venvRGZ logo.png '
          r'C:\Users\User\PycharmProjects\pythonProject\venvRGZ style.css')


def get_region(p_key, p_status=False):
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


def tuple_to_dataframe(p_tuple):
    p_list = []
    for x in p_tuple:
        a = [y for y in x]
        p_list.append(a)
    return p_list


def to_csv(p_tuple):
    with open('tuple.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(p_tuple)


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href

def main():
    p_address = sys.argv[1]
    p_login_db = sys.argv[2]
    p_pass_db = sys.argv[3]
    p_name_db = sys.argv[4]
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

    PAGE_CONFIG = {"page_title": "База данных извещений с сайта zakupki.gov.ru",
                   "page_icon": image,
                   "layout": "centered",
                   "initial_sidebar_state": "auto"}

    st.set_page_config(**PAGE_CONFIG)
    table_contener_df = st.container()
    connection = pymysql.connect(host=p_address, user=p_login_db, passwd=p_pass_db, database=p_name_db)

    st.sidebar.markdown('## Фильтры')
    selected_regions = st.sidebar.multiselect("Регионы РФ", get_region('', True))
    date_start = st.sidebar.date_input('Период размещения заявок:',
                                       [datetime.datetime.now() - datetime.timedelta(1), datetime.datetime.now()])
    like_words = st.sidebar.text_input('Ключевые фразы объекта закупки, указанные через запятую:')
    list_like_words = like_words.split(',')
    # with st.echo():
    #    st.write(selected_regions)
    # with st.echo():
    #    st.write(list_like_words)
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

    p_sql_regions_pre = " AND region IN ("
    if len(selected_regions) > 0:
        sql_regions = [f"\'{get_region(x)}\'" for x in selected_regions if get_region(x) != "" f"'{get_region(x)}'"]
        p_sql_regions = ",".join(sql_regions) + ')'
    else:
        p_sql_regions = ""
        p_sql_regions_pre = ""
        # sql_regions = sql_regions + f' AND region IN ({sql_regions})'
    # SELECT * FROM `notifications` WHERE `date_publish` BETWEEN '2021-12-13' AND '2021-12-13'
    # AND `region` IN () AND `subject_purchase`LIKE ''
    cursor = connection.cursor()
    sql = f"Select date_publish,date_finish,fz,type_fz,region,num_notification,price,subject_purchase,customer, address_customer, ref from {p_nametable} where date_publish BETWEEN '{date_start[0]}' AND '{date_start[-1]}'{p_sql_regions_pre}{p_sql_regions}{sql_like_words}" \
          f" ORDER BY date_publish, region"
    cursor.execute(sql)
    # with st.echo():
    #    st.write(sql)

    AllRow = cursor.fetchall()
    # st.dataframe()
    # st.table(AllRow)

    # list_a = [['1', '2', '3'],
    #          ['6', '7', '8']]
    columns = ['Дата_публикации', 'Дата_окончания', 'ФЗ', 'Тип_закупки', 'Регион', 'Номер_извещения', 'Начальная_цена',
               'Предмет_закупки', 'Заказчик', 'Адрес_заказчика', 'Ссылка']
    df_a = pd.DataFrame(tuple_to_dataframe(AllRow), columns=columns)

    # with table_contener:
    #    fig = go.Figure(data=go.Table(
    #                    header=dict(values=['Дата публикации','Дата окончания', 'ФЗ', 'Тип закупки', 'Регион', 'Номер извещения', 'Начальная цена', 'Предмет закупки', 'Заказчик', 'Адрес заказчика', 'Ссылка'], fill_color='#dde23e', align='center'),
    #                    cells=dict(values=[df_a.Дата_публикации,df_a.Дата_окончания,df_a.ФЗ, df_a.Тип_закупки, df_a.Регион, df_a.Номер_извещения, df_a.Начальная_цена, df_a.Предмет_закупки, df_a.Заказчик, df_a.Адрес_заказчика, df_a.Ссылка],font = dict(color = 'darkslategray', size = 12))))

    #    fig.update_layout(margin=dict(l=2,r=2, b=2, t=2))
    #    st.write(fig)

    with table_contener_df:
        st.dataframe(df_a)
    if st.button('Сохранить таблицу в Excel файл'):
        p_xls = df_a.to_excel("/var/www/html/data_goszakupki.xlsx")
        st.markdown(f'<a href="http://zimin.website/data_goszakupki.xlsx">Download csv file</a>', unsafe_allow_html=True )
    # load_css(fr'{p_css}{p_slash}{p_name_css}')
    #st.download_button('Download CSV', text_contents, 'text/csv')
    #with open('myfile.csv') as f:
    #    st.download_button('Download CSV', f)  # Defaults to 'text/plain'

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Parameters are not specified!')
    elif len(sys.argv) == 2:
        decryption_of_parameters()
    else:
        main()
