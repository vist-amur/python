import sys
from datetime import datetime, timedelta

from dash import dash
from dash import dash_table as dt
import dash_bootstrap_components as dbc
from dash import html as html
from dash import dcc as dcc
import pandas as pd
import pymysql as mysql
from dash.dependencies import Input, Output

data_tooltip = {}
num_progress = 0


def tuple_to_dataframe(p_tuple):
    p_list = []
    for x in p_tuple:
        a = [y for y in x]
        p_list.append(a)
    return p_list


def get_columns_table():
    columns = ['Дата_публикации', 'Дата_окончания', 'ФЗ', 'Тип_закупки', 'Регион', 'Номер_извещения', 'Начальная_цена',
               'Предмет_закупки', 'Заказчик', 'Адрес_заказчика', 'Ссылка']
    return columns


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
                    'Jamalo-Neneckij_AO': 'Ямало-Ненецкий автономный округ',
                    'Jaroslavskaja_obl': 'Ярославская область',
                    'Kabardino-Balkarskaja_Resp': 'Кабардино-Балкарская Республика',
                    'Kaliningradskaja_obl': 'Калининградская область',
                    'Kalmykija_Resp': 'Республика Калмыкия',
                    'Kaluzhskaja_obl': 'Калужская область',
                    'Kamchatskij_kraj': 'Камчатский край',
                    'Karachaevo-Cherkesskaja_Resp': 'Карачаево-Черкесская Республика',
                    'Karelija_Resp': 'Республика Карелия',
                    'Kemerovskaja_obl': 'Кемеровская область',
                    'Khabarovskij_kraj': 'Хабаровский край',
                    'Khakasija_Resp': 'Республика Хакасия',
                    'Khanty-Mansijskij_AO - Jugra_AO': 'Ханты-Мансийский автономный округ — Югра',
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
                    'Sankt-Peterburg': 'Санкт-Петербург',
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


def get_region_all(p_key):
    dict_regions = {'Республика Адыгея': ['Adygeja_Resp','Adygeya_Resp'],
                    'Республика Алтай': ['Altaj_Resp','Altay_Resp'],
                    'Алтайский край': ['Altajskij_kraj', 'Altayskii__krai']
                    'Амурская область': ['Amurskaja_obl', 'Amurskaya_obl'],
                    'Архангельская область': ['Arkhangelskaja_obl', 'Arhangelskaya_obl'],
                    'Астраханская область': ['Astrakhanskaja_obl', 'Astrahanskaya_obl'],
                    'Байконур': ['Bajkonur_g', 'Baikonur_g'],
                    'Республика Башкортостан': ['Bashkortostan_Resp', 'Bashkortostan_Resp'],
                    'Белгородская область': ['Belgorodskaja_obl', 'Belgorodskaya_obl'],
                    'Брянская область': ['Brjanskaja_obl', 'Brianskaya_obl'],
                    'Республика Бурятия': ['Burjatija_Resp', 'Buryatiya_Resp'],
                    'Chechenskaja_Resp': 'Чеченская Республика',
                    'Cheljabinskaja_obl': 'Челябинская область',
                    'Chukotskij_AO': 'Чукотский автономный округ',
                    'Chuvashskaja_Resp': 'Чувашская Республика-Чувашия',
                    'Dagestan_Resp': 'Республика Дагестан',
                    'Evrejskaja_Aobl': 'Еврейская автономная область',
                    'Ingushetija_Resp': 'Республика Ингушетия',
                    'Irkutskaja_obl': 'Иркутская область',
                    'Ivanovskaja_obl': 'Ивановская область',
                    'Jamalo-Neneckij_AO': 'Ямало-Ненецкий автономный округ',
                    'Jaroslavskaja_obl': 'Ярославская область',
                    'Kabardino-Balkarskaja_Resp': 'Кабардино-Балкарская Республика',
                    'Kaliningradskaja_obl': 'Калининградская область',
                    'Kalmykija_Resp': 'Республика Калмыкия',
                    'Kaluzhskaja_obl': 'Калужская область',
                    'Kamchatskij_kraj': 'Камчатский край',
                    'Karachaevo-Cherkesskaja_Resp': 'Карачаево-Черкесская Республика',
                    'Karelija_Resp': 'Республика Карелия',
                    'Kemerovskaja_obl': 'Кемеровская область',
                    'Khabarovskij_kraj': 'Хабаровский край',
                    'Khakasija_Resp': 'Республика Хакасия',
                    'Khanty-Mansijskij_AO - Jugra_AO': 'Ханты-Мансийский автономный округ — Югра',
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
                    'Sankt-Peterburg': 'Санкт-Петербург',
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


standard_BS = dbc.themes.BOOTSTRAP
app = dash.Dash(__name__, external_stylesheets=[standard_BS])
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
df_gl = pd.DataFrame
app.layout = html.Div(
    [
        dbc.Row(html.Div([

            html.Div([], className='col-2'),

            html.Div([
                html.H1(children='Поисковый сервис Веди - Госзакупки',
                        style={'textAlign': 'center', 'color': '#ffffff', 'marginBottom': '3rem'}
                        )],
                className='col-8',
                style={'padding-top': '3%'}
            ),

            # html.Div([
            #     html.Img(
            #         src=app.get_asset_url('logo_001c.png'),
            #         height='43 px',
            #         width='auto')
            # ],
            #     className='col-2',
            #     style={
            #         'align-items': 'center',
            #         'padding-top': '1%',
            #         'height': 'auto'})

        ],
            className='row',
            style={'height': '4%',
                   'background-color': '#0d3117'}
        ), style={'height': '4%'}),
        dbc.Row(html.Div([]), style={'height': '50px',
                                     'background-color': '#ffffff'}),
        dbc.Row(
            [
                dbc.Col(
                    html.Div([html.Div(children='Период размещения закупок:',
                                       style={'text-align': 'center',
                                              'color': '#0d3117', 'font-size': '18px'}),

                              html.Div(['',
                                        dcc.DatePickerRange(
                                            id='date-picker-sales',
                                            start_date=datetime.now() - timedelta(days=1),
                                            end_date=datetime.now(),
                                            min_date_allowed=datetime(2021, 1, 1),

                                            start_date_placeholder_text='Start date',
                                            display_format='DD-MMM-YYYY',
                                            first_day_of_week=1,
                                            end_date_placeholder_text='End date',
                                            style={'font-size': '12px', 'display': 'inline-block',
                                                   'border-radius': '2px',
                                                   'border': '1px solid #ccc', 'color': '#333', 'border-spacing': '0',
                                                   'border-collapse': 'separate'})
                                        ], style={'margin-top': '5px', 'text-align': 'center'},
                                       )
                              ]),

                ),
                dbc.Col(html.Div(
                    children=[html.Div(children="Регионы РФ:", id="regions_el", className="menu-title",
                                       style={'font-size': '18px', 'color': '#0d3117'}),
                              dcc.Dropdown(
                                  id="region-filter",
                                  options=[
                                      {"label": region, "value": region}
                                      for region in get_region('', True)
                                  ],
                                  value="",
                                  clearable=False,
                                  className="dropdown",
                                  multi=True,
                              ),
                              html.Div(
                                  children="Укажите ключевые слова для поиска по наименованию закупки, через запятую."
                                           " По окончании ввода, введите точку:",
                                  id="input_wrd", className="menu-words",
                                  style={'font-size': '14px', 'color': '#0d3117'}),
                              dcc.Input(
                                  id="input_words",
                                  placeholder='Вводите слова через запятую...',
                                  type='text',
                                  value="",
                                  style={"width": "100%", 'font-size': '18px', 'border': '1px solid #ccc',
                                         'border-radius': '2px', 'border-spacing': '0'}
                              ),
                              html.Div(
                                  children="Закон",
                                  id="text_fz", className="class-text-fz",
                                  style={'font-size': '18px', 'color': '#0d3117'}),
                              dcc.Dropdown(
                                  id="fz-filter",
                                  options=[
                                      {"label": fz, "value": fz}
                                      for fz in ['44-ФЗ', '223-ФЗ']
                                  ],
                                  value='44-ФЗ',
                                  clearable=False,
                                  className="dropdown",
                                  multi=True,
                              ),

                              ], style={"width": "50%", 'font-size': '12px'}, )
                ),

            ]
        ),
        dbc.Row(html.Div([]), style={'height': '50px',
                                     'background-color': '#ffffff'}),
        dbc.Row(
            [dt.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in get_columns_table()],
                export_format="xlsx",
                css=[{
                    'selector': '.dash-spreadsheet td div',
                    'rule': '''
                            line-height: 15px;
                            max-height: 80px; min-height: 80px; height: 80px;
                            display: block;
                            overflow-y: hidden;
                        '''
                }],
                tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in data_tooltip
                ],
                tooltip_duration=None,
                style_cell={'textAlign': 'left'},
                style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Date', 'Region']
                ],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'lineHeight': '15px'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },

                style_table={'overflowX': 'auto'},

                # page_current=1,
                page_size=10,
                # page_action='custom'
            ),
                dbc.Row(html.Div([]), style={'height': '50px',
                                             'background-color': '#ffffff'}),
                dcc.Loading(
                    id="loading-1",
                    children=[html.Div([html.Div(id="table-output-1")])],
                    type="circle",
                ),

            ], style={"width": "80%", 'font-size': '12px', "margin": "auto"}),
        dbc.Row(html.Div([]), style={'height': '50px',
                                     'background-color': '#ffffff'}),

    ]
)


@app.callback(
    [Output("table", "data")],
    [
        Input("region-filter", "value"),
        Input("fz-filter", "value"),
        Input("input_words", "value"),
        Input("date-picker-sales", "start_date"),
        Input("date-picker-sales", "end_date"),
    ],
)
def update_table(region, fz, words, start_date, end_date):
    sql_like_words = ''
    ind = 0
    p_words = words.strip()
    if len(p_words) > 0:
        if p_words[-1] == ".":
            p_spl = p_words.replace('.', '').split(',')
            for x in p_spl:
                if ind == 0:
                    sql_like_words = sql_like_words + f' AND (subject_purchase LIKE \'%{x}%\''
                else:
                    sql_like_words = sql_like_words + f' OR subject_purchase LIKE \'%{x}%\''
                ind += 1
            sql_like_words = sql_like_words + ')'
        else:
            sql_like_words = ''
    p_sql_regions_pre = " AND region IN ("
    if len(region) > 0:
        sql_regions = [f"\'{get_region(x)}\'" for x in region if get_region(x) != "" f"'{get_region(x)}'"]
        p_sql_regions = ",".join(sql_regions) + ')'
    else:
        p_sql_regions = ""
        p_sql_regions_pre = ""

    p_sql_type_fz_pre = " AND fz IN ("
    if len(fz) > 0:
        sql_type_fz = [f"\'{x}\'" for x in fz]
        if isinstance(fz, str):
            p_sql_type_fz = f"\'{fz}\')"
        else:
            p_sql_type_fz = ",".join(sql_type_fz) + ')'
    else:
        p_sql_type_fz = ""
        p_sql_type_fz_pre = ""
    try:
        connection = mysql.connect(host="37.77.105.58", user="phpmyadmin", passwd="g7A1PuDN", database="goszakupki")
    except:
        print("Not connect with database!")
        sys.exit()

    p_nametable = 'notifications'
    cursor = connection.cursor()
    sql = f"Select date_publish,date_finish,fz,type_fz,region,num_notification,price,subject_purchase,customer, address_customer, ref from {p_nametable} where date_publish BETWEEN '{start_date}' AND '{end_date}'{p_sql_regions_pre}{p_sql_regions}{p_sql_type_fz_pre}{p_sql_type_fz}{sql_like_words}" \
          f" ORDER BY date_publish, region"
    cursor.execute(sql)
    # with st.echo():
    #    st.write(sql)

    AllRow = cursor.fetchall()
    tup = tuple_to_dataframe(AllRow)
    df_a = pd.DataFrame(tuple_to_dataframe(AllRow), columns=get_columns_table())
    global df_gl
    df_gl = df_a.copy()
    data = df_a.to_dict('records')
    global data_tooltip
    data_tooltip = data.copy()
    connection.close()
    return [data]


@app.callback(Output("table-output-1", "children"), Input("table", "value"))
def input_triggers_spinner(value):
    # time.sleep(1)
    return value


server = app.server

if __name__ == '__main__':
    server.run(debug=True)
