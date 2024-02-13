import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
import pandas as pd
import numpy as np

# ----------------------------------------------------------------
# Configuração da página

# SIDEBAR

with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: black;'>Base Potencial</h1>", unsafe_allow_html=True)
    st.image('full_IoT_site.png')
    st.subheader('Filtros')

ufs = ['TODOS', 'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'EX', 'GO', 'MA',
       'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO',
       'RR', 'RS', 'SC', 'SE', 'SP', 'TO']

@st.cache_data
def carregar_dados(allow_output_mutation=True):
    # Simule a leitura do arquivo CSV aqui
    df = pd.read_csv('./dados/sample-base-full-iot-limpa.csv')
    return df

df = carregar_dados()

# ----------------------------------------------------------------
# FILTROS

# ESTADO
uf_select = st.sidebar.selectbox('ESTADO', ufs)

# MUNICIPIO
if uf_select == 'TODOS':
    mun = df.descricao.unique()
    mun.sort()
else:
    mun = df[df.uf==uf_select].descricao.unique()
    mun.sort()
mun = np.insert(mun, 0, 'TODOS')
municipios_select = st.sidebar.selectbox('MUNICIPIOS', mun)

# CAPITAL SOCIAL
cap_social = ['TODOS','0 a 1.000', '1.000 a 100.000', '100.000 a 1.000.000', 'Mais de 1.000.000']
filtro_capital_social = st.sidebar.selectbox('CAPITAL SOCIAL', cap_social)

# SEGMENTO
if uf_select == 'TODOS':
    df_filtros = df
else:
    df_filtros = df[df.uf==uf_select]

if municipios_select == 'TODOS':
    pass
else:
    df_filtros = df_filtros[df_filtros.descricao==municipios_select]

if filtro_capital_social == 'TODOS':
    pass
elif filtro_capital_social == 'Mais de 1.000.0000':
    df_filtros = df_filtros[df_filtros.capital_social >= 1000000]
elif filtro_capital_social == '100.000 a 1.000.000':
    df_filtros = df_filtros[df_filtros.capital_social >= 100000]
elif filtro_capital_social == '1.000 a 100.000':
    df_filtros = df_filtros[df_filtros.capital_social >= 1000]
else:
    df_filtros = df_filtros[df_filtros.capital_social < 1000]

dynamic_filters = DynamicFilters(df_filtros, filters=['SEGMENTO'])
with st.sidebar:
    dynamic_filters.display_filters()

# ---------------------------------------------------------------
# BODY
df_filtered = dynamic_filters.filter_df()
df_filtered = df_filtered.reset_index()
df_filtered = df_filtered.drop('index', axis=1)

st.title('📊 Full IoT - Base Potencial')

df_filtered.capital_social = df_filtered.capital_social.astype('int64')
# COLUNAS
st.subheader('KPI Metrics')
a1, a2 = st.columns(2)
vol_total = len(df_filtered)
med_cap_social = int(df_filtered.capital_social.mean())
with a1:
    # st.markdown('### Total')
    a1.metric("Vol. Total", vol_total)

with a2:
    # st.markdown('### Total')
    a2.metric("Média Capital Social", f"{med_cap_social:,d}")




st.divider()
# BASE POTENCIAL
st.subheader('Amostra da Base Potencial (até 10 linhas)')
st.dataframe(df_filtered.head(10))

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_filtered)

st.download_button(
    label="Download Dados Filtrados Totais",
    data=csv,
    file_name='dados-filtrados-totais.csv',
    mime='text/csv',
)

# dynamic_filters.display_df()

# st.write(df.head(10)) 

# df.cnpj = df.cnpj.astype(str)
# # df.telefone1 = df.telefone1.astype(str)
# df.data_inicio_atividades = df.data_inicio_atividades.astype(str)

# df.info()
# st.write(df.head(10)) 