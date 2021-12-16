import datetime
import streamlit as st
from PIL import Image

def load_css(file_name:str):
    '''
        Function to load and render a local stylesheet
    '''
    with open(file_name) as f:
        d = f.read()
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


image_directory = r"C:\Users\DNS\report_goszakupki\venvRGZ\logo.PNG"
image = Image.open(image_directory)

PAGE_CONFIG = {"page_title":"База данных извещений с сайта zakupki.gov.ru",
               "page_icon":image,
               "layout":"centered",
               "initial_sidebar_state":"auto"}

st.set_page_config(**PAGE_CONFIG)

selected_regions = st.sidebar.multiselect("Регионы РФ", ['Амурская область', 'Хабаровский край'])
date_start = st.sidebar.date_input('Период размещения заявок:',[datetime.datetime.now() - datetime.timedelta(1), datetime.datetime.now()])
like_words = st.sidebar.text_input('Ключевые фразы, указанные через запятую:')

load_css(r'C:\Users\DNS\report_goszakupki\venvRGZ\style.css')
