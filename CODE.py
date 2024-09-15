#IMPORT THƯ VIỆN
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import ta
import numpy as np
import ipywidgets as widgets
from IPython.display import display
from matplotlib.gridspec import GridSpec
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from PIL import Image
import altair as alt
import streamlit as st
import requests
import talib as ta
import plotly.subplots as sp
from pathlib import Path
import plotly.express as px
#THIẾT LẬP GIAO DIỆN BẰNG STREAMLIT
st.markdown("""
    <style>
        h1 {
            color: blue;
            text-align: left;
            font-size: 36px;
            padding-bottom: 5px; /* Thêm padding dưới cho h1 */
        }
        h2 {
            color: gray;
            text-align: left;
            font-size: 24px;
            padding-top: 5px; /* Thêm padding trên cho h2 */
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("<h1>CTCP Tập đoàn Hòa Phát (HOSE: HPG)</h1>", unsafe_allow_html=True)
st.markdown("<h2>Hoa Phat Group JSC</h2>", unsafe_allow_html=True)
with st.sidebar:
    selected = option_menu(
        menu_title= None,
        options= ["Trang chủ", "Tổng quan ngành", "Biểu đồ giá và khối lượng", "Các đường chỉ báo", "Tài chính"],
        icons=["house", "briefcase", "p-circle", "activity", "wallet"]
    )
if selected == "Trang chủ":
    st.write('Hòa Phát là Tập đoàn sản xuất công nghiệp hàng đầu Việt Nam. Khởi đầu từ một Công ty chuyên buôn bán các loại máy xây dựng từ tháng 8/1992, Hòa Phát lần lượt mở rộng sang các lĩnh vực khác như Nội thất, ống thép, thép xây dựng, điện lạnh, bất động sản và nông nghiệp. Ngày 15/11/2007, Hòa Phát chính thức niêm yết cổ phiếu trên thị trường chứng khoán Việt Nam với mã chứng khoán HPG. '
             '\n\nHiện nay, Tập đoàn hoạt động trong 05 lĩnh vực: Gang thép (thép xây dựng, thép cuộn cán nóng) - Sản phẩm thép (gồm Ống thép, tôn mạ, thép rút dây, thép dự ứng lực) - Nông nghiệp - Bất động sản – Điện máy gia dụng. Sản xuất thép là lĩnh vực cốt lõi chiếm tỷ trọng 90% doanh thu và lợi nhuận toàn Tập đoàn. Với công suất 8.5 triệu tấn thép thô/năm, Hòa Phát là doanh nghiệp sản xuất thép lớn nhất khu vực Đông Nam Á. '
             '\n\nTập đoàn Hòa Phát giữ thị phần số 1 Việt Nam về thép xây dựng, ống thép; Top 5 về tôn mạ. Hiện nay, Hòa Phát nằm trong Top 5 doanh nghiệp tư nhân lớn nhất Việt Nam, Top 50 DN niêm yết hiệu quả nhất, Top 30 DN nộp ngân sách Nhà nước lớn nhất Việt Nam, Top 3 DN có vốn điều lệ lớn nhất thị trường chứng khoán, Top 10 cổ phiếu có vốn hóa lớn nhất thị trường chứng khoán Việt Nam.')
if selected == "Các đường chỉ báo":
    sub_categories = ["None", "SMA", "MACD", "Bollinger Bands", "RSI", "Stochastic Oscillator" ]
    selected_sub_category = st.selectbox("Chọn đường chỉ báo", sub_categories)
if selected == "Tài chính":
    sub_categories_fi = ["None", "Biểu đồ tài chính", "Chỉ số tài chính"]
    selected_sub_category_fi = st.selectbox("Chọn danh mục", sub_categories_fi)
@st.cache_data()
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
#XỬ LÍ DỮ LIỆU VÀ LỌC RA MCK HÒA PHÁT
def read_excel_data(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df
df_sheet1 = read_excel_data('/Users/huynhthao/Downloads/Price-Vol VN 2015-2023.xlsx', sheet_name='Info')
df_sheet2 = read_excel_data('/Users/huynhthao/Downloads/Price-Vol VN 2015-2023.xlsx', sheet_name='Price')
df_sheet3 = read_excel_data('/Users/huynhthao/Downloads/Price-Vol VN 2015-2023.xlsx', sheet_name='Volume')
column_name = 'Activity'
value_to_remove = 'Dead'
df_sheet1 = df_sheet1[df_sheet1[column_name] != value_to_remove]
nan_rows_sheet1 = df_sheet1.iloc[:, 1:].isnull().all(axis=1)
df_sheet1 = df_sheet1[~nan_rows_sheet1]
def rename_element_sheet1(element):
   return str(element).replace('VT:', '').strip()
df_sheet1["Symbol"] = df_sheet1["Symbol"].apply(rename_element_sheet1)
nan_rows_sheet2 = df_sheet2.iloc[:, 1:].isnull().all(axis=1)
df_sheet2 = df_sheet2[~nan_rows_sheet2]
def rename_element_sheet2(element):
   return str(element).replace('VT:', '').replace('(P)', '').strip()
df_sheet2["Code"] = df_sheet2["Code"].apply(rename_element_sheet2)
df_sheet2.columns = ['Name', 'Code', 'CURRENCY'] + pd.to_datetime(df_sheet2.columns[3:], format='%d/%m/%Y').astype(
   str).tolist()
df_merged12 = pd.merge(df_sheet2, df_sheet1, left_on='Name', right_on='Name', how='inner')
melted_df = pd.melt(df_merged12, id_vars=['Name', 'Code', 'Start Date', 'Currency', 'Activity'],
                   value_vars=df_merged12.columns[3:],
                   var_name='Date', value_name='Price')
melted_df['Date'] = pd.to_datetime(melted_df['Date'], format='%Y-%m-%d', errors='coerce')
melted_df = melted_df.dropna(subset=['Date'])
melted_df12 = pd.melt(df_merged12, id_vars=['Name', 'Code'],
                    value_vars=df_merged12.columns[3:],
                    var_name='Date', value_name='Price')
melted_df12['Date'] = pd.to_datetime(melted_df12['Date'], format='%Y-%m-%d', errors='coerce')
melted_df12 = melted_df12.dropna(subset=['Date'])
desiredprice_stock_code= melted_df12[melted_df12['Code'] == 'HPG']
column_name2 = 'Name'
value_to_remove2 = '#ERROR'
df_sheet3 = df_sheet3[df_sheet3[column_name2] != value_to_remove2]
nan_rows_sheet3 = df_sheet3.iloc[:, 1:].isnull().all(axis=1)
df_sheet3 = df_sheet3[~nan_rows_sheet3]
def rename_element_sheet3(element):
   return str(element).replace('VT:', '').replace('(VO)', '').strip()
df_sheet3["Code"] = df_sheet3["Code"].apply(rename_element_sheet3)
df_sheet3.columns = ['Name', 'Code', 'CURRENCY'] + pd.to_datetime(df_sheet3.columns[3:], format='%d/%m/%Y').astype(
   str).tolist()
df_sheet3 = df_sheet3.drop('Name',axis=1)
df_merged13 = pd.merge(df_sheet3, df_sheet1, left_on='Code', right_on='Symbol', how='inner')
melted_df13 = pd.melt(df_merged13, id_vars=[  'Code', 'Start Date', 'Currency', 'Activity'],
                   value_vars=df_merged13.columns[3:],
                   var_name='Date', value_name='Volume')
melted_df13['Date'] = pd.to_datetime(melted_df13['Date'], format='%Y-%m-%d', errors='coerce')
melted_df13 = melted_df13.dropna(subset=['Date'])
melted_df13 = pd.melt(df_merged13, id_vars=['Name', 'Code'],
                    value_vars=df_merged13.columns[3:],
                    var_name='Date', value_name='Volume')
melted_df13['Date'] = pd.to_datetime(melted_df13['Date'], format='%Y-%m-%d', errors='coerce')
melted_df13 = melted_df13.dropna(subset=['Date'])
desired_volume_stock= melted_df13[melted_df13['Code'] == 'HPG']
#VẼ ĐƯỜNG BIỂU ĐỒ GIÁ
fig_price = sp.make_subplots(specs=[[{"secondary_y": True}]])
    # Add trace for price
fig_price.add_trace(
        go.Scatter(x=desiredprice_stock_code['Date'], y=desiredprice_stock_code['Price'], mode='lines', name='Price',marker=dict(color='red')),
        secondary_y=False,
    )
    # Add trace for volume
fig_price.add_trace(
        go.Bar(x=desired_volume_stock['Date'], y=desired_volume_stock['Volume'], name='Volume',marker=dict(color='#ADD8E6')
),
        secondary_y=True,
    )
    # Update layout
fig_price.update_layout(
        title=f"Biểu đồ Giá và Khối lượng của cổ phiếu HPG giai đoạn 2015-2023",
        xaxis_title='Ngày',
        yaxis_title='Giá',
        yaxis2_title='Volume',
        xaxis_rangeslider=dict(visible=True),
    )
if selected == "Biểu đồ giá và khối lượng":
    chart_container = st.empty()
    chart_container.plotly_chart(fig_price)
#VẼ CÁC ĐƯỜNG CHỈ BÁO
def plot_sma(desiredprice_stock_code, column='Price', window=20):
    # Loại bỏ các ngày thứ 7 và chủ nhật khỏi dữ liệu
    desiredprice_stock_code = desiredprice_stock_code[desiredprice_stock_code['Date'].dt.dayofweek < 5]
    # Tính toán giá trị SMA
    sma = ta.SMA(desiredprice_stock_code[column], timeperiod=window)
    # Vẽ biểu đồ Scatter cho SMA
    sma_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=sma, name=f'SMA-{window}', line=dict(color='orange'))
    # Cài đặt layout cho biểu đồ
    layout = go.Layout(
        title=f'Biểu đồ đường trung bình SMA',
        xaxis=dict(rangeslider=dict(visible=True)),
        yaxis=dict(title='Giá(VNĐ)')
    )
    # Tạo subplot
    fig = go.Figure(data=[sma_trace], layout=layout)
    return fig
def plot_macd(desiredprice_stock_code, column='Price', short_window=12, long_window=26, signal_window=9):
    # Loại bỏ các ngày thứ 7 và chủ nhật khỏi dữ liệu
    desiredprice_stock_code = desiredprice_stock_code[desiredprice_stock_code['Date'].dt.dayofweek < 5]
    # Tính các giá trị cần thiết cho đường MACD
    short_ema = desiredprice_stock_code[column].ewm(span=short_window, adjust=False).mean()
    long_ema = desiredprice_stock_code[column].ewm(span=long_window, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    # Tính sự chênh lệch giữa MACD và Signal Line để tạo Histogram
    histogram = macd_line - signal_line
    # Vẽ biểu đồ dữ liệu gốc
    macd_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=macd_line, name='MACD Line', line=dict(color='blue'))
    signal_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=signal_line, name='Signal Line', line=dict(color='red'))
    histogram_trace = go.Bar(x=desiredprice_stock_code['Date'], y=histogram, name='Histogram', marker=dict(color='green'))
    # Cài đặt layout cho biểu đồ
    layout = go.Layout(
        title='Đường chỉ báo MACD',
        xaxis=dict(rangeslider=dict(visible=True)),
        yaxis=dict(title=''),
    )
   # Tạo subplot
    fig = go.Figure(data=[macd_trace, signal_trace, histogram_trace], layout=layout)
    return fig
# Sử dụng hàm để vẽ biểu đồ MACD với Histogram
#plot_macd_with_histogram(filtered_data, column='Price', short_window=12, long_window=26, signal_window=9)
def plot_bollinger_bands(desiredprice_stock_code, column='Price', window=20, num_std_dev=2):
    # Loại bỏ các ngày thứ 7 và chủ nhật khỏi dữ liệu
    desiredprice_stock_code = desiredprice_stock_code[desiredprice_stock_code['Date'].dt.dayofweek < 5]
    # Tính giá trị trung bình và độ lệch chuẩn của dữ liệu
    rolling_mean = desiredprice_stock_code[column].rolling(window=window).mean()
    upper_band = rolling_mean + (desiredprice_stock_code[column].rolling(window=window).std() * num_std_dev)
    lower_band = rolling_mean - (desiredprice_stock_code[column].rolling(window=window).std() * num_std_dev)
    # Vẽ biểu đồ dữ liệu gốc
    price_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=desiredprice_stock_code[column], name=column, line=dict(color='blue'))
    # Vẽ đường trung bình
    mean_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=rolling_mean, name=f'Mean ({window} days)', line=dict(color='orange'))
    # Vẽ Bollinger Bands
    upper_band_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=upper_band, name=f'Upper Band', line=dict(color='red'))
    lower_band_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=lower_band, name=f'Lower Band', line=dict(color='green'))
    # Cài đặt layout cho biểu đồ
    layout = go.Layout(
        title=f'Đường chỉ báo Bollinger Bands',
        xaxis=dict(rangeslider=dict(visible=True)),
        yaxis=dict(title="Giá(VNĐ)"),
    )
    # Tạo subplot
    fig = go.Figure(data=[price_trace, mean_trace, upper_band_trace, lower_band_trace], layout=layout)
    return fig
def plot_rsi(desiredprice_stock_code, column='Price', window=14):
    # Loại bỏ các ngày thứ 7 và chủ nhật khỏi dữ liệu
    desiredprice_stock_code = desiredprice_stock_code[desiredprice_stock_code['Date'].dt.dayofweek < 5]
    # Tính toán giá trị RSI
    rsi = ta.RSI(desiredprice_stock_code[column], timeperiod=window)
    # Vẽ biểu đồ Scatter cho RSI
    rsi_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=rsi, name='RSI', line=dict(color='blue'))
    # Tạo các đường ngang cho mức quá mua và quá bán
    overbought_line = go.Scatter(x=desiredprice_stock_code['Date'], y=[70] * len(desiredprice_stock_code), mode='lines',
                                 name='Overbought (70)', line=dict(color='red', dash='dash'))

    oversold_line = go.Scatter(x=desiredprice_stock_code['Date'], y=[30] * len(desiredprice_stock_code), mode='lines',
                               name='Oversold (30)', line=dict(color='green', dash='dash'))
    # Cài đặt layout cho biểu đồ
    layout = go.Layout(
        title='Đường chỉ báo RSI',
        xaxis=dict(rangeslider=dict(visible=True)),
        yaxis=dict(title='RSI'),
        shapes=[
            dict(
                type='line',
                x0=desiredprice_stock_code['Date'].iloc[0],
                x1=desiredprice_stock_code['Date'].iloc[-1],
                y0=70,
                y1=70,
                line=dict(color='red', dash='dash')
            ),
            dict(
                type='line',
                x0=desiredprice_stock_code['Date'].iloc[0],
                x1=desiredprice_stock_code['Date'].iloc[-1],
                y0=30,
                y1=30,
                line=dict(color='green', dash='dash')
            )
        ]
    )
    # Tạo subplot
    fig = go.Figure(data=[rsi_trace, overbought_line, oversold_line], layout=layout)
    return fig
def plot_stochastic_oscillator(desiredprice_stock_code, close_column='Price', window=14, smoothing=3):
    # Loại bỏ các ngày thứ 7 và chủ nhật khỏi dữ liệu
    desiredprice_stock_code = desiredprice_stock_code[desiredprice_stock_code['Date'].dt.dayofweek < 5]
    # Tính giá trị Stochastic Oscillator
    stoch_oscillator = ta.STOCH(desiredprice_stock_code[close_column], desiredprice_stock_code[close_column], desiredprice_stock_code[close_column], fastk_period=window,
                                slowk_period=smoothing, slowd_period=smoothing)
    # Vẽ đường Stochastic Oscillator (%K và %D)
    percent_k_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=stoch_oscillator[0], name='%K', line=dict(color='blue'))
    percent_d_trace = go.Scatter(x=desiredprice_stock_code['Date'], y=stoch_oscillator[1], name='%D', line=dict(color='red'))
    # Tạo đường ngang 80% và 20% cho biểu đồ Stochastic Oscillator
    overbought_line = go.Scatter(x=desiredprice_stock_code['Date'], y=[80] * len(desiredprice_stock_code), mode='lines',
                                 name='Overbought (80)', line=dict(color='red', dash='dash'))

    oversold_line = go.Scatter(x=desiredprice_stock_code['Date'], y=[20] * len(desiredprice_stock_code), mode='lines',
                               name='Oversold (20)', line=dict(color='green', dash='dash'))
    layout = go.Layout(
        title=f'Đường chỉ báo dao động Stochastic Oscillator',
        xaxis=dict(rangeslider=dict(visible=True)),
    )
    fig = go.Figure(data=[percent_k_trace, percent_d_trace], layout=layout)
    return fig
if selected == "Các đường chỉ báo":
    if selected_sub_category == "None":
        st.empty()
    elif selected_sub_category == "SMA":  # Chỉnh sửa thành selected_sub_category
        #st.plotly_chart(fig_price, use_container_width=True)
        st.plotly_chart(plot_sma(desiredprice_stock_code))  # Truyền dữ liệu vào hàm plot_sma
    elif selected_sub_category == "MACD":
        st.plotly_chart(plot_macd(desiredprice_stock_code))
    elif selected_sub_category == "Bollinger Bands":
        st.plotly_chart(plot_bollinger_bands(desiredprice_stock_code))
    elif selected_sub_category == "RSI":
        st.plotly_chart(plot_rsi(desiredprice_stock_code))
    elif selected_sub_category == "Stochastic Oscillator":
        st.plotly_chart(plot_stochastic_oscillator(desiredprice_stock_code))
######
# Đọc dữ liệu từ 5 file Excel vào DataFrame
file_paths = [
    "/Users/huynhthao/Downloads/2018-Vietnam.xlsx",
    "/Users/huynhthao/Downloads/2019-Vietnam.xlsx",
    "/Users/huynhthao/Downloads/2020-Vietnam.xlsx",
    "/Users/huynhthao/Downloads/2021-Vietnam.xlsx",
    "/Users/huynhthao/Downloads/2022-Vietnam.xlsx",
]
industry_path = "/Users/huynhthao/Downloads/2022-Vietnam.xlsx"
# Tạo một danh sách chứa các giá trị cần tính:
doanh_thu_thuan_values = []
loi_nhuan_thuan_hdkd_values = []
loi_nhuan_sau_thue_values = []
loi_nhuan_truoc_thue_values = []
loi_nhuan_gop_values = []
khau_hao_values = []
chi_phi_lai_vay_values = []
no_vay_dh_values = []
no_vay_nh_values = []
no_pt_values = []
no_nh_values = []
tts_nh_values = []
tts_dh_values = []
von_csh_values = []
cd_ctyme_values = []
lct_hdkd_values = []
lct_hdtc_values = []
lct_hddt_values = []
tien_tdt_values = []
htk_values = []
ptkh_values = []
nam_values = ['2018', '2019', '2020', '2021', '2022']
namm_values = ['2019', '2020', '2021', '2022']
# Lặp qua từng năm để thêm dữ liệu vào danh sách
for file_path in file_paths:
    df = pd.read_excel(file_path, header=1)
    hpg_data = df[df['Mã'] == 'HPG']
    doanh_thu_thuan_col = df.columns[df.columns.str.contains('KQKD. Doanh thu thuần', regex=True)][0]
    loi_nhuan_thuan_hdkd_col = df.columns[df.columns.str.contains('KQKD. Lợi nhuận thuần từ hoạt động kinh doanh', regex=True)][0]
    loi_nhuan_sau_thue_col = df.columns[df.columns.str.contains('KQKD. Lợi nhuận sau thuế', regex=True)][0]
    loi_nhuan_truoc_thue_col = df.columns[df.columns.str.contains('KQKD. Tổng lợi nhuận kế toán trước thuế', regex=True)][0]
    loi_nhuan_gop_col = df.columns[df.columns.str.contains('KQKD. Lợi nhuận gộp', regex=True)][0]
    khau_hao_col = df.columns[df.columns.str.contains('LCTT. Khấu hao TSCĐ', regex=True)][0]
    chi_phi_lai_vay_col = df.columns[df.columns.str.contains('KQKD. Trong đó: Chi phí lãi vay', regex=True)][0]
    no_vay_dh_col = [col for col in df.columns if 'CĐKT. Vay và nợ thuê tài chính dài hạn' in col][0]
    no_vay_nh_col = [col for col in df.columns if 'CĐKT. Vay và nợ thuê tài chính ngắn hạn' in col][0]
    no_pt_col = [col for col in df.columns if 'CĐKT. NỢ PHẢI TRẢ' in col][0]
    no_nh_col = [col for col in df.columns if 'CĐKT. Nợ ngắn hạn' in col][0]
    tts_nh_col = [col for col in df.columns if 'CĐKT. TÀI SẢN NGẮN HẠN' in col][0]
    tts_dh_col = [col for col in df.columns if 'CĐKT. TÀI SẢN DÀI HẠN' in col][0]
    von_csh_col = [col for col in df.columns if 'CĐKT. VỐN CHỦ SỞ HỮU' in col][0]
    cd_ctyme_col = [col for col in df.columns if 'KQKD. Cổ đông của Công ty mẹ' in col][0]
    lct_hdkd_col = [col for col in df.columns if 'LCTT. Lưu chuyển tiền tệ ròng từ các hoạt động sản xuất kinh doanh' in col][0]
    lct_hdtc_col = [col for col in df.columns if 'LCTT. Lưu chuyển tiền tệ từ hoạt động tài chính' in col][0]
    lct_hddt_col = [col for col in df.columns if 'LCTT. Lưu chuyển tiền tệ ròng từ hoạt động đầu tư' in col][0]
    tien_tdt_col = [col for col in df.columns if 'LCTT. Tiền và tương đương tiền cuối kỳ' in col][0]
    htk_col = [col for col in df.columns if 'CĐKT. Hàng tồn kho' in col][0]
    ptkh_col = [col for col in df.columns if 'CĐKT. Các khoản phải thu ngắn hạn' in col][0]
    # Kiểm tra xem có dữ liệu hay không
    if not hpg_data.empty:
        doanh_thu_thuan_values.extend(hpg_data[doanh_thu_thuan_col].values)
        loi_nhuan_sau_thue_values.extend(hpg_data[loi_nhuan_sau_thue_col].values)
        loi_nhuan_truoc_thue_values.extend(hpg_data[loi_nhuan_truoc_thue_col].values)
        loi_nhuan_gop_values.extend(hpg_data[loi_nhuan_gop_col].values)
        khau_hao_values.extend(hpg_data[khau_hao_col].values)
        chi_phi_lai_vay_values.extend(hpg_data[chi_phi_lai_vay_col].values)
        no_vay_dh_values.append(hpg_data[no_vay_dh_col].values[0])
        no_vay_nh_values.append(hpg_data[no_vay_nh_col].values[0])
        no_pt_values.append(hpg_data[no_pt_col].values[0])
        no_nh_values.append(hpg_data[no_nh_col].values[0])
        tts_nh_values.append(hpg_data[tts_nh_col].values[0])
        tts_dh_values.append(hpg_data[tts_dh_col].values[0])
        von_csh_values.append(hpg_data[von_csh_col].values[0])
        cd_ctyme_values.append(hpg_data[cd_ctyme_col].values[0])
        lct_hdkd_values.append(hpg_data[lct_hdkd_col].values[0])
        lct_hdtc_values.append(hpg_data[lct_hdtc_col].values[0])
        lct_hddt_values.append(hpg_data[lct_hddt_col].values[0])
        tien_tdt_values.append(hpg_data[tien_tdt_col].values[0])
        htk_values.append(hpg_data[htk_col].values[0])
        ptkh_values.append(hpg_data[ptkh_col].values[0])
        loi_nhuan_thuan_hdkd_values.append(hpg_data[loi_nhuan_thuan_hdkd_col].values[0])
#TÍNH TOÁN BIỂU THỨC TỶ SUẤT LỢI NHUẬN GỘP BIÊN:
gross_profit_margin = [(ln / dt) * 100 if dt != 0 else 0 for ln, dt in zip(loi_nhuan_gop_values, doanh_thu_thuan_values)]
#VẼ BIỂU ĐỒ
fig_ty_le_lngb = go.Figure()
fig_ty_le_lngb.add_trace(go.Bar(
    x=nam_values,
    y=gross_profit_margin,
    marker_color='blue',
    name='Tỷ lệ lợi nhuận gộp biên '
))
# Update layout to add labels and title
fig_ty_le_lngb.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ lệ lợi nhuận gộp biên'
)
#TÍNH TOÁN GIÁ TRỊ EBITDA:
ebitda_values = [ln + kh - cp for ln, kh, cp in zip(loi_nhuan_truoc_thue_values, khau_hao_values, chi_phi_lai_vay_values)]
#TÍNH TOÁN GIÁ TRỊ EBIT:
ebit_values = [ebitda - kh for ebitda, kh in zip (ebitda_values, khau_hao_values)]
#TÍNH TOÁN TỶ LỆ LÃI EBITDA:
ebitda_margin = [(ebitda / dt) * 100 if dt != 0 else 0 for ebitda, dt in zip(ebitda_values, doanh_thu_thuan_values)]
#VẼ BIỂU ĐỒ:
# Hiển thị biểu đồ
fig_ebitda = go.Figure()
fig_ebitda.add_trace(go.Bar(
    x=nam_values,
    y=ebitda_margin,
    marker_color='blue',
    name='Tỷ lệ lãi EBITDA '
))
# Update layout to add labels and title
fig_ebitda.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ lệ lãi EBITDA'
)
#TÍNH TOÁN TỶ LỆ LÃI EBIT:
ebit_margin = [(ebit / dt) * 100 if dt != 0 else 0 for ebit, dt in zip(ebit_values, doanh_thu_thuan_values)]
#VẼ BIỂU ĐỒ:
# Hiển thị biểu đồ
fig_ebit = go.Figure()
fig_ebit.add_trace(go.Bar(
    x=nam_values,
    y=ebit_margin,
    marker_color='blue',
    name='Tỷ lệ lãi EBIT '
))
# Update layout to add labels and title
fig_ebit.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ lệ lãi EBIT'
)
#TÍNH TOÁN TỶ SUẤT SINH LỢI TRÊN DOANH THU THUẦN:
profit_ratio = [(ln / dt) * 100 if dt != 0 else 0 for ln, dt in zip(loi_nhuan_sau_thue_values, doanh_thu_thuan_values)]
fig_ty_le_sl_dtt = go.Figure()
fig_ty_le_sl_dtt.add_trace(go.Bar(
    x=nam_values,
    y=profit_ratio,
    marker_color='blue',
    name='Tỷ suất sinh lợi trên doanh thu thuần'
))
# Update layout to add labels and title
fig_ty_le_sl_dtt.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ suất sinh lợi trên doanh thu thuần'
)
#####NHÓM CHỈ SỐ TĂNG TRƯỞNG
#TÍNH TOÁN TỶ LỆ TĂNG TRƯỞNG DOANH THU:
ty_le_tang_truong_doanh_thu = []
for i in range(1, len(doanh_thu_thuan_values)):
    ty_le_tang_truong_dt = ((doanh_thu_thuan_values[i] - doanh_thu_thuan_values[i - 1]) / doanh_thu_thuan_values[i - 1]) * 100
    ty_le_tang_truong_dt = round (ty_le_tang_truong_dt, 2)
    ty_le_tang_truong_doanh_thu.append(ty_le_tang_truong_dt)
#VẼ BIỂU ĐỒ:
fig_ty_le_tang_truong_doanh_thu = go.Figure()
fig_ty_le_tang_truong_doanh_thu.add_trace(go.Bar(
    x=namm_values,
    y=ty_le_tang_truong_doanh_thu,
    marker_color='blue',
    name='Tỷ lệ tăng trưởng doanh thu'
))
# Update layout to add labels and title
fig_ty_le_tang_truong_doanh_thu.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ lệ tăng trưởng doanh thu'
)
#TÍNH TOÁN TỶ LỆ TĂNG TRƯỞNG LỢI NHUẬN GỘP:
ty_le_tang_truong_loi_nhuan_gop = []
for i in range(1, len(loi_nhuan_gop_values)):
    ty_le_tang_truong_ln = ((loi_nhuan_gop_values[i] - loi_nhuan_gop_values[i - 1]) / loi_nhuan_gop_values[i - 1]) * 100
    ty_le_tang_truong_ln = round(ty_le_tang_truong_ln, 2)
    ty_le_tang_truong_loi_nhuan_gop.append(ty_le_tang_truong_ln)

# VẼ BIỂU ĐỒ:
fig_ty_le_tang_truong_loi_nhuan_gop = go.Figure()
fig_ty_le_tang_truong_loi_nhuan_gop.add_trace(go.Bar(
    x=namm_values,
    y=ty_le_tang_truong_loi_nhuan_gop,
    marker_color='blue',
    name='Tỷ lệ tăng trưởng lợi nhuận gộp '
))
# Update layout to add labels and title
fig_ty_le_tang_truong_loi_nhuan_gop.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ lệ tăng trưởng lợi nhuận gộp'
)
#TÍNH TOÁN TỶ LỆ TĂNG TRƯỞNG LỢI NHUẬN TRƯỚC THUẾ:
ty_le_tang_truong_loi_nhuan_truoc_thue = []
for i in range(1, len(loi_nhuan_gop_values)):
    ty_le_tang_truong_ln_tt = ((loi_nhuan_truoc_thue_values[i] - loi_nhuan_truoc_thue_values[i - 1]) / loi_nhuan_truoc_thue_values[i - 1]) * 100
    ty_le_tang_truong_ln_tt = round(ty_le_tang_truong_ln_tt, 2)
    ty_le_tang_truong_loi_nhuan_truoc_thue.append(ty_le_tang_truong_ln_tt)

#VẼ BIỂU ĐỒ:
fig_ty_le_tang_truong_loi_nhuan_truoc_thue = go.Figure()
fig_ty_le_tang_truong_loi_nhuan_truoc_thue.add_trace(go.Bar(
    x=namm_values,
    y=ty_le_tang_truong_loi_nhuan_truoc_thue,
    marker_color='blue',
    name='Tỷ lệ tăng trưởng lợi nhuận trước thuế '
))
# Update layout to add labels and title
fig_ty_le_tang_truong_loi_nhuan_truoc_thue.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ lệ tăng trưởng lợi nhuận trước thuế'
)

#TÍNH TOÁN CHỈ SỐ ROAA:
ty_le_roaa = []
tts_values = [tsnh + tsdh for tsnh, tsdh in zip (tts_nh_values, tts_dh_values)]
for i in range(1, len(loi_nhuan_sau_thue_values)):
    roaa = loi_nhuan_sau_thue_values[i]  / (((tts_values[i]) + (tts_values[i - 1]))/2) * 100
    roaa = round(roaa, 2)
    ty_le_roaa.append(roaa)
#VẼ BIỂU ĐỒ:
fig_ty_le_roaa = go.Figure()
fig_ty_le_roaa.add_trace(go.Bar(
    x=namm_values,
    y=ty_le_roaa,
    marker_color='blue',
    name='Tỷ lệ ROAA '
))
# Update layout to add labels and title
fig_ty_le_roaa.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ lệ ROAA'
)
#TÍNH TOÁN CHỈ SỐ ROCE:
ty_le_roce = []
for i in range(1, len(ebit_values)):
    roce = ebit_values [i]/ ((((tts_values[i]) + (tts_values[i - 1]))/2) - (((no_nh_values[i]) + (no_nh_values[i - 1]))/2)) * 100
    roce = round( roce, 2)
    ty_le_roce.append(roce)
#VẼ BIỂU ĐỒ:
fig_ty_le_roce = go.Figure()
fig_ty_le_roce.add_trace(go.Bar(
    x=namm_values,
    y=ty_le_roce,
    marker_color='blue',
    name='Tỷ lệ ROCE '
))
# Update layout to add labels and title
fig_ty_le_roce.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ lệ ROCE'
)
#TÍNH TOÁN CHỈ SỐ ROEA:
ty_le_roea = []
for i in range(1, len(cd_ctyme_values)):
    roea = cd_ctyme_values[i] / (((von_csh_values[i]) + (von_csh_values[i - 1])) / 2) * 100
    roea = round(roea, 2)
    ty_le_roea.append(roea)
#VẼ BIỂU ĐỒ:
fig_ty_le_roea = go.Figure()
fig_ty_le_roea.add_trace(go.Bar(
    x=namm_values,
    y=ty_le_roea,
    marker_color='blue',
    name='Tỷ lệ ROEA '
))
# Update layout to add labels and title
fig_ty_le_roea.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ lệ ROEA'
)
#TÍNH TOÁN CHỈ SỐ TĂNG TRƯỞNG TTS:
ty_le_tang_truong_tts= []
for i in range(1, len(tts_values)):
    tang_truong_tts = (tts_values[i] / (tts_values[i - 1]))
    tang_truong_tts = round(tang_truong_tts, 2)
    ty_le_tang_truong_tts.append(tang_truong_tts)
####### NHÓM CHỈ SỐ THANH KHOẢN
#TÍNH TOÁN TỶ SỐ THANH TOÁN BẰNG TIỀN MẶT
ty_le_tt_tm = [(tdt / nnh ) if nnh != 0 else 0 for tdt, nnh in zip(tien_tdt_values, no_nh_values)]
ty_le_tt_tm = [round(values, 2) for values in ty_le_tt_tm]
# Hiển thị biểu đồ
fig_ty_le_tt_tm = go.Figure()
fig_ty_le_tt_tm.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_tt_tm,
    marker_color='blue',
    name='Tỷ số thanh toán bằng tiền mặt'
))
# Update layout to add labels and title
fig_ty_le_tt_tm.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số thanh toán bằng tiền mặt',
    legend=dict(title=''),
)
#TÍNH TOÁN TỶ SỐ THANH TOÁN NHANH:
ty_le_ttn = [((tsnh - htk) / nnh ) if nnh != 0 else 0 for tsnh, htk, nnh in zip(tts_nh_values,htk_values,no_nh_values)]
ty_le_ttn = [round(values, 2) for values in ty_le_ttn]
# Hiển thị biểu đồ
fig_ty_le_ttn = go.Figure()
fig_ty_le_ttn.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_ttn,
    marker_color='blue',
    name='Tỷ số thanh toán nhanh'
))
# Update layout to add labels and title
fig_ty_le_ttn.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số thanh toán nhanh',
    legend=dict(title=''),
)
#TÍNH TOÁN TỶ SỐ THANH TOÁN HIỆN HÀNH:
ty_le_tthh =  [(tsnh / nnh ) if nnh != 0 else 0 for tsnh, nnh in zip(tts_nh_values, no_nh_values)]
ty_le_tthh = [round(values, 2) for values in ty_le_tthh]
# Hiển thị biểu đồ
fig_ty_le_tthh = go.Figure()
fig_ty_le_tthh.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_tthh,
    marker_color='blue',
    name='Tỷ số thanh toán hiện hành'
))
# Update layout to add labels and title
fig_ty_le_tthh.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số thanh toán hiện hành',
    legend=dict(title=''),
)
#TÍNH TOÁN KHẢ NĂNG THANH TOÁN LÃI VAY:
ty_le_ttlv = [((lntt - cplv) / (-cplv) ) if cplv != 0 else 0 for lntt, cplv in zip(loi_nhuan_truoc_thue_values, chi_phi_lai_vay_values)]
ty_le_ttlv = [round(values, 2) for values in ty_le_ttlv]
# Hiển thị biểu đồ
fig_ty_le_ttlv = go.Figure()
fig_ty_le_ttlv.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_ttlv,
    marker_color='blue',
    name='Khả năng thanh toán lãi vay'
))
# Update layout to add labels and title
fig_ty_le_ttlv.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Khả năng thanh toán lãi vay',
    legend=dict(title=''),
)
######NHÓM CHỈ SỐ ĐÒN BẪY TÀI CHÍNH:
#Tỷ số Nợ ngắn hạn trên Tổng nợ phải trả:
ty_le_nnh_npt = [(nnh / npt )*100 if npt != 0 else 0 for nnh, npt in zip(no_nh_values, no_pt_values)]
ty_le_nnh_npt = [round(values, 2) for values in ty_le_nnh_npt]
# Hiển thị biểu đồ
fig_ty_le_nnh_npt = go.Figure()
fig_ty_le_nnh_npt.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_nnh_npt,
    marker_color='blue',
    name='Tỷ số Nợ ngắn hạn trên Tổng nợ phải trả'
))
# Update layout to add labels and title
fig_ty_le_nnh_npt.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số Nợ ngắn hạn trên Tổng nợ phải trả',
    legend=dict(title=''),
)
#Tỷ số Nợ vay trên Tổng tài sản:
ty_le_nv_tts = [( (nvnh+nvdh )/ tts )*100 if tts != 0 else 0 for nvnh, nvdh, tts in zip(no_vay_nh_values, no_vay_dh_values, tts_values)]
ty_le_nv_tts = [round(values, 2) for values in ty_le_nv_tts]
# Hiển thị biểu đồ
fig_ty_le_nv_tts = go.Figure()
fig_ty_le_nv_tts.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_nv_tts,
    marker_color='blue',
    name='Tỷ số Nợ vay trên Tổng tài sản'
))
# Update layout to add labels and title
fig_ty_le_nv_tts.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số Nợ vay trên Tổng tài sản',
    legend=dict(title=''),
)
#Tỷ số Nợ trên Tổng tài sản:
ty_le_no_tts = [ (npt / tts )*100 if tts != 0 else 0 for npt, tts in zip(no_pt_values, tts_values)]
ty_le_no_tts = [round(values, 2) for values in ty_le_no_tts]
# Hiển thị biểu đồ
fig_ty_le_no_tts = go.Figure()
fig_ty_le_no_tts.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_no_tts,
    marker_color='blue',
    name='Tỷ số Nợ trên Tổng tài sản'
))
# Update layout to add labels and title
fig_ty_le_no_tts.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số Nợ trên Tổng tài sản',
    legend=dict(title=''),
)
#Tỷ số Vốn chủ sở hữu trên Tổng tài sản:
ty_le_vcsh_tts = [ ( vcsh / tts )*100 if tts != 0 else 0 for vcsh, tts in zip(von_csh_values, tts_values)]
ty_le_vcsh_tts = [round(values, 2) for values in ty_le_vcsh_tts]
# Hiển thị biểu đồ
fig_ty_le_vcsh_tts = go.Figure()
fig_ty_le_vcsh_tts.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_vcsh_tts,
    marker_color='blue',
    name='Tỷ số Vốn chủ sở hữu trên Tổng tài sản'
))
# Update layout to add labels and title
fig_ty_le_vcsh_tts.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số Vốn chủ sở hữu trên Tổng tài sản',
    legend=dict(title=''),
)

#Tỷ số Nợ ngắn hạn trên Vốn chủ sở hữu:
ty_le_nnh_vcsh = [ ( nnh / vcsh )*100 if vcsh != 0 else 0 for nnh, vcsh in zip(no_nh_values, von_csh_values)]
ty_le_nnh_vcsh = [round(values, 2) for values in ty_le_nnh_vcsh]
# Hiển thị biểu đồ
fig_ty_le_nnh_vcsh = go.Figure()
fig_ty_le_nnh_vcsh.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_nnh_vcsh,
    marker_color='blue',
    name='Tỷ số Nợ ngắn hạn trên Vốn chủ sở hữu'
))
# Update layout to add labels and title
fig_ty_le_nnh_vcsh.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số Nợ ngắn hạn trên Vốn chủ sở hữu',
    legend=dict(title=''),
)
#Tỷ số Nợ vay trên Vốn chủ sở hữu:
ty_le_nv_vcsh = [ ( (nvnh+nvdh ) / vcsh )*100 if vcsh != 0 else 0 for nvnh, nvdh, vcsh in zip(no_vay_nh_values,no_vay_dh_values, von_csh_values)]
ty_le_nv_vcsh = [round(values, 2) for values in ty_le_nv_vcsh]
# Hiển thị biểu đồ
fig_ty_le_nv_vcsh = go.Figure()
fig_ty_le_nv_vcsh.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_nv_vcsh,
    marker_color='blue',
    name='Tỷ số Nợ vay trên Vốn chủ sở hữu'
))
# Update layout to add labels and title
fig_ty_le_nv_vcsh.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số Nợ vay trên Vốn chủ sở hữu',
    legend=dict(title=''),
)
#Tỷ số Nợ trên Vốn chủ sở hữu:
ty_le_no_vcsh = [ ( npt / vcsh )*100 if vcsh != 0 else 0 for npt, vcsh in zip(no_pt_values, von_csh_values)]
ty_le_no_vcsh = [round(values, 2) for values in ty_le_no_vcsh]
# Hiển thị biểu đồ
fig_ty_le_no_vcsh = go.Figure()
fig_ty_le_no_vcsh.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_no_vcsh,
    marker_color='blue',
    name='Tỷ số Nợ trên Vốn chủ sở hữu'
))
# Update layout to add labels and title
fig_ty_le_no_vcsh.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số Nợ trên Vốn chủ sở hữu',
    legend=dict(title=''),
)
######NHÓM CHỈ SỐ DÒNG TIỀN:
#Tỷ số dòng tiền HĐKD trên doanh thu thuần:
ty_le_hdkd_dtt = [ ( hdkd / dtt )*100 if dtt != 0 else 0 for hdkd, dtt in zip(lct_hdkd_values, doanh_thu_thuan_values)]
ty_le_hdkd_dtt = [round(values, 2) for values in ty_le_hdkd_dtt]
#VE BIEU DO:
nam_values = ['2018', '2019', '2020', '2021', '2022']
# Hiển thị biểu đồ
fig_ty_le_hdkd_dtt = go.Figure()
fig_ty_le_hdkd_dtt.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_hdkd_dtt,
    marker_color='blue',
    name='Tỷ số dòng tiền HĐKD trên doanh thu thuần'
))
# Update layout to add labels and title
fig_ty_le_hdkd_dtt.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Tỷ số dòng tiền HĐKD trên doanh thu thuần theo năm',
    legend=dict(title=''),
)
#Khả năng chi trả nợ ngắn hạn từ dòng tiền HĐKD:
ty_le_tra_no_hdkd = [ ( hdkd /nnh )*100 if nnh != 0 else 0 for hdkd, nnh in zip(lct_hdkd_values, no_nh_values)]
ty_le_tra_no_hdkd = [round(values, 2) for values in ty_le_tra_no_hdkd]
#VẼ BIỂU ĐỒ:
# Hiển thị biểu đồ
fig_ty_le_tra_no_hdkd = go.Figure()
fig_ty_le_tra_no_hdkd.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_tra_no_hdkd,
    marker_color='blue',
    name='Khả năng chi trả nợ ngắn hạn từ dòng tiền HĐKD'
))
# Update layout to add labels and title
fig_ty_le_tra_no_hdkd.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Khả năng chi trả nợ ngắn hạn từ dòng tiền HĐKD',
    legend=dict(title=''),
)
#Dòng tiền từ HĐKD trên Tổng tài sản:
ty_le_hdkd_tts = [ ( hdkd /tts )*100 if tts != 0 else 0 for hdkd, tts in zip(lct_hdkd_values, tts_values)]
ty_le_hdkd_tts = [round(values, 2) for values in ty_le_hdkd_tts]
#VẼ BIỂU ĐỒ:
fig_ty_le_hdkd_tts = go.Figure()
fig_ty_le_hdkd_tts.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_hdkd_tts,
    marker_color='blue',
    name='Dòng tiền từ HĐKD trên Tổng tài sản'
))
# Update layout to add labels and title
fig_ty_le_hdkd_tts.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Dòng tiền từ HĐKD trên Tổng tài sản',
    legend=dict(title=''),
)
#Dòng tiền từ HĐKD trên Vốn chủ sở hữu:
ty_le_hdkd_vcsh = [ ( hdkd /vcsh )*100 if vcsh != 0 else 0 for hdkd, vcsh in zip(lct_hdkd_values, von_csh_values)]
ty_le_hdkd_vcsh = [round(values, 2) for values in ty_le_hdkd_vcsh]
#VẼ BIỂU ĐỒ:
fig_ty_le_hdkd_vcsh = go.Figure()
fig_ty_le_hdkd_vcsh.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_hdkd_vcsh,
    marker_color='blue',
    name='Dòng tiền từ HĐKD trên Vốn chủ sở hữu'
))
# Update layout to add labels and title
fig_ty_le_hdkd_vcsh.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Dòng tiền từ HĐKD trên Vốn chủ sở hữu',
    legend=dict(title=''),
)
#Dòng tiền từ HĐKD trên Lợi nhuận thuần từ HĐKD:
ty_le_hdkd_lnt = [ ( hdkd /lnt )*100 if lnt != 0 else 0 for hdkd, lnt in zip(lct_hdkd_values, loi_nhuan_thuan_hdkd_values)]
ty_le_hdkd_lnt = [round(values, 2) for values in ty_le_hdkd_lnt]
#VẼ BIỂU ĐỒ:
fig_ty_le_hdkd_lnt = go.Figure()
fig_ty_le_hdkd_lnt.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_hdkd_lnt,
    marker_color='blue',
    name='Dòng tiền từ HĐKD trên Lợi nhuận thuần từ HĐKD'
))
# Update layout to add labels and title
fig_ty_le_hdkd_lnt.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Dòng tiền từ HĐKD trên Lợi nhuận thuần từ HĐKD',
    legend=dict(title=''),
)
#Khả năng thanh toán nợ từ dòng tiền HĐKD:
ty_le_hdkd_npt = [ ( hdkd /npt )*100 if npt != 0 else 0 for hdkd, npt in zip(lct_hdkd_values, no_pt_values)]
ty_le_hdkd_npt = [round(values, 2) for values in ty_le_hdkd_npt]
#VẼ BIỂU ĐỒ:
fig_ty_le_hdkd_npt = go.Figure()
fig_ty_le_hdkd_npt.add_trace(go.Bar(
    x=nam_values,
    y=ty_le_hdkd_npt,
    marker_color='blue',
    name='Khả năng thanh toán nợ từ dòng tiền HĐKD'
))
# Update layout to add labels and title
fig_ty_le_hdkd_npt.update_layout(
    xaxis=dict(title='Năm'),
    yaxis=dict(title='Tỷ số(%)'),
    title='Biểu đồ Khả năng thanh toán nợ từ dòng tiền HĐKD',
    legend=dict(title=''),
)

# Tạo biểu đồ DOANH THU THUẦN
fig_dt = go.Figure()
# Thêm dữ liệu vào biểu đồ với giá trị của cột 'Doanh thu thuần' làm giá trị trục y
fig_dt.add_trace(go.Bar(x=list(range(2018, 2023)), y=doanh_thu_thuan_values,
                     name="HPG",
                     width=0.4
                     ))

# Thiết lập layout cho biểu đồ
fig_dt.update_layout(title='Doanh thu thuần',
                  xaxis_title='Năm',
                  yaxis_title='Doanh thu thuần',
                  xaxis=dict(
                      tickvals=list(range(2018, 2023)),
                      ticktext=[str(year) for year in range(2018, 2023)]
                  ),
                  )
fig_dt.update_layout(
    bargap=0.4
)

# Tạo biểu đồ LỢI NHUẬN SAU THUẾ
fig_ln = go.Figure()
fig_ln.add_trace(go.Bar(x=list(range(2018, 2023)), y=loi_nhuan_sau_thue_values,
                    name="HPG",
                    width=0.4,
                    marker_color='green'
                    ))
fig_ln.update_layout(title='Lợi nhuận sau thuế',
                 xaxis_title='Năm',
                 yaxis_title='Lợi nhuận',
                 xaxis=dict(
                     tickvals=list(range(2018, 2023)),
                     ticktext=[str(year) for year in range(2018, 2023)]
                 ),
                 )
fig_ln.update_layout(
   bargap=0.4  # hoặc thử các giá trị lớn hơn nếu cần
)

#TẠO BIỂU ĐỒ GHÉP DOANH THU THUẦN - LỢI NHUẬN SAU THUẾ:
fig_dtt_ln = go.Figure()
# Thêm cột doanh thu thuần
fig_dtt_ln.add_trace(go.Bar(x=[year for year in range(2018, 2023)], y=doanh_thu_thuan_values,
                              name="Doanh thu thuần",
                              width=0.4,
                              marker_color='blue'  # Màu sắc của cột
                              ))

# Thêm cột lợi nhuận sau thuế
fig_dtt_ln.add_trace(go.Bar(x=[year for year in range(2018, 2023)], y=loi_nhuan_sau_thue_values,
                              name="Lợi nhuận sau thuế",
                              width=0.4,
                              marker_color='green'  # Màu sắc của cột
                              ))

# Thiết lập layout cho biểu đồ ghép
fig_dtt_ln.update_layout(title='Doanh thu thuần và Lợi nhuận sau thuế',
                           xaxis_title='Năm',
                           yaxis_title='Giá trị',
                           xaxis=dict(
                               tickvals=[year for year in range(2018, 2023)],
                               ticktext=[str(year) for year in range(2018, 2023)]
                           ),
                           barmode='group'
                           )


# Tạo biểu đồ đường cho tỷ suất lợi nhuận gộp biên
fig_margin = go.Figure()
fig_margin.add_trace(go.Scatter(x=list(range(2018, 2023)), y=gross_profit_margin,
                         mode='lines+markers',
                         name='Tỷ suất lợi nhuận gộp biên',
                         line_shape='spline'))

fig_margin.add_trace(go.Scatter(x=list(range(2018, 2023)), y=ebitda_margin,
                         mode='lines+markers',
                         name='Tỷ lệ lãi EBITDA',
                         line_shape='spline'))
fig_margin.add_trace(go.Scatter(x=list(range(2018, 2023)), y=profit_ratio,
                         mode='lines+markers',
                         name='Tỷ suất sinh lợi trên doanh thu thuần',
                         line_shape='spline'))
# Thiết lập layout cho biểu đồ
fig_margin.update_layout(title='Biên lợi nhuận',
                  xaxis_title='Năm',
                  yaxis_title='Tỷ suất (%)',
                  xaxis=dict(
                      tickvals=list(range(2018, 2023)),
                      ticktext=[str(year) for year in range(2018, 2023)]
                  ),
                  legend=dict(
                      x=0, y=0
                  )
                  )

#####################





#TÍNH TOÁN VẼ ĐƯỜNG CẤU TRÚC TÀI SẢN
# Tính tỷ số nợ vay trên tổng tài sản
ty_so1 = [(nnh + ndh) / (tsnh + tsdh)*100 for nnh, ndh, tsnh, tsdh in zip(no_vay_nh_values, no_vay_dh_values, tts_nh_values, tts_dh_values)]
ty_so2 = [npt / (tsnh +tsdh)*100 for npt, tsnh, tsdh in zip(no_pt_values, tts_nh_values, tts_dh_values)]
# Chuyển đổi range thành danh sách
years = list(range(2018, 2023))

# Vẽ biểu đồ
fig_ts = go.Figure()

# Thêm đường cho tỷ số nợ vay trên tổng tài sản
fig_ts.add_trace(go.Scatter(x=years, y=ty_so1, mode='lines+markers', name='Tỷ số nợ vay/Tổng tài sản', line_shape='spline', line=dict(color = 'green')))
# Add the second line to the existing plot
fig_ts.add_trace(go.Scatter(x=years, y=ty_so2, mode='lines+markers', name='Tỷ số nợ/Tổng tài sản', line_shape='spline', line=dict(color='red')))

# Update layout
fig_ts.update_layout( title='Cấu trúc tài sản',
    xaxis_title='Năm',
    yaxis_title='Tỷ suất (%)',
    xaxis=dict(
        tickvals=years,
        ticktext=[str(year) for year in years],
        dtick = 4
    ),
legend=dict(
                      x=1, y=0 ))

#####TỔNG QUAN NGÀNH:
df_ins = pd.read_excel(industry_path, header=1)
hpg_2022 = df_ins[df_ins['Mã'] == 'HPG']
doanh_thu_thuan_n_values = []
doanh_thu_thuan_tn_values = []
tts_nh_n_values = []
tts_dh_n_values = []
htk_n_values = []
doanh_thu_thuan_hpg_values = []
#VẼ BIỂU ĐỒ THỊ PHẦN LỢI NHUẬN SAU THUẾ TOÀN NGÀNH
# Tìm tên cột chứa "KQKD. Lợi nhuận sau thuế"
loi_nhuan_sau_thue_n_col = df_ins.columns[df_ins.columns.str.contains('KQKD. Lợi nhuận sau thuế', regex=True)].tolist()
# Kiểm tra xem có cột nào chứa từ khóa không
if loi_nhuan_sau_thue_n_col:
    # Lấy tên cột đầu tiên nếu có nhiều cột chứa từ khóa
    loi_nhuan_sau_thue_n_col = loi_nhuan_sau_thue_n_col[0]

    # Gom nhóm dữ liệu theo cột "Ngành ICB - cấp 1" và tính tổng lợi nhuận sau thuế
    grouped_df = df_ins.groupby("Ngành ICB - cấp 1")[loi_nhuan_sau_thue_n_col].sum().reset_index()

    # Kiểm tra và xử lý giá trị âm
    if any(grouped_df[loi_nhuan_sau_thue_n_col] < 0):
        grouped_df[loi_nhuan_sau_thue_n_col] = grouped_df[loi_nhuan_sau_thue_n_col].apply(lambda x: max(0, x))

    # Chia giá trị cho 1 tỷ để đổi đơn vị thành tỷ đồng
    grouped_df[loi_nhuan_sau_thue_n_col] /= 1e9

    # Lọc ra các dòng có giá trị phần trăm khác 0%
    non_zero_percentages = grouped_df[grouped_df[loi_nhuan_sau_thue_n_col] != 0]

    # Kiểm tra xem có dữ liệu nào để vẽ biểu đồ không
    if not non_zero_percentages.empty:
        # Vẽ biểu đồ hình tròn sử dụng plotly.graph_objects
        fig_ln_n = go.Figure(data=[go.Pie(labels=non_zero_percentages["Ngành ICB - cấp 1"],
                                          values=non_zero_percentages[loi_nhuan_sau_thue_n_col])])

        fig_ln_n.update_layout(title='Thị phần Lợi nhuận sau thuế theo ngành năm 2022')

        # Định dạng hiển thị giá trị trên biểu đồ thành tỷ đồng và thêm thông tin phần trăm
        fig_ln_n.update_traces(hoverinfo='label+percent',
                               textinfo='percent',
                               hovertemplate='%{label}: %{value:.2f} tỷ đồng<br>%{percent}')

#VẼ BIỂU ĐỒ TOP5 CTY THÉP CÓ DOANH THU CAO NHẤT
df_nganh = df_ins[df_ins['Ngành ICB - cấp 4'] == 'Thép và sản phẩm thép']
doanh_thu_thuan_n_col = df_ins.columns[df_ins.columns.str.contains('KQKD. Doanh thu thuần', regex=True)][0]
htk_n_col = df_ins.columns[df_ins.columns.str.contains('CĐKT. Hàng tồn kho', regex=True)][0]
tts_nh_n_col = [col for col in df_nganh.columns if 'CĐKT. TÀI SẢN NGẮN HẠN' in col][0]
tts_dh_n_col = [col for col in df_nganh.columns if 'CĐKT. TÀI SẢN DÀI HẠN' in col][0]
doanh_thu_thuan_tn_col = [col for col in df_nganh.columns if 'KQKD. Doanh thu thuần' in col][0]
doanh_thu_thuan_hpg_col = hpg_2022.columns[hpg_2022.columns.str.contains('KQKD. Doanh thu thuần', regex=True)][0]
if not df_nganh.empty:
    # Include all columns in the select_columns list
    select_columns = df_ins.columns.tolist()
    # Extract the desired columns from the filtered DataFrame
    selected_data = df_nganh[select_columns]
    # Sort the DataFrame based on 'KQKD. Lợi nhuận thuần từ hoạt động kinh doanh' column
    selected_data = selected_data.sort_values(by=doanh_thu_thuan_n_col, ascending=False)
    # Select the top 5 rows
    top5_data = selected_data.head(5)
    # Append the top 5 values to the list
    doanh_thu_thuan_n_values.extend(top5_data[doanh_thu_thuan_n_col].tolist())
    doanh_thu_thuan_tn_values.extend(df_nganh[doanh_thu_thuan_tn_col].tolist())
if not hpg_2022.empty:
    # Chỉ thêm giá trị nếu doanh_thu_thuan_hpg_values rỗng
    if not doanh_thu_thuan_hpg_values:
        doanh_thu_thuan_hpg_values.extend(hpg_2022[doanh_thu_thuan_hpg_col].tolist())
###VẼ BIỂU ĐỒ TREEMAP:
df_new = pd.DataFrame({
    'Mã': df_nganh["Mã"],
    'Doanh thu thuần': df_nganh[doanh_thu_thuan_tn_col]
})
fig_tree_map = px.treemap(df_new,
                          path=['Mã'],
                          values='Doanh thu thuần',
                          title='Biểu đồ Tree Map Doanh thu thuần theo Công ty trong ngành Thép',
                          color='Doanh thu thuần',
                          color_continuous_scale='Viridis'
)
#vẽ biểu đồ top5 dtt:
fig_industry = go.Figure()
fig_industry.add_trace(go.Bar(
    x=top5_data['Mã'],
    y=top5_data[doanh_thu_thuan_n_col],
    marker_color='blue',
    name='Doanh thu từ hoạt động kinh doanh '
))
# Update layout to add labels and title
fig_industry.update_layout(
    xaxis=dict(title=''),
    yaxis=dict(title='(VNĐ)'),
    title='Top 5 doanh nghiệp trong ngành Thép có doanh thu cao nhất năm 2022',
    legend=dict(title=''),
)
#VẼ BIỂU ĐỒ LỢI NHUẬN HPG SO VỚI NGÀNH THÉP:
tong_dt_nganh = df_nganh[doanh_thu_thuan_tn_col].sum()
ty_le_dt_hpg = doanh_thu_thuan_hpg_values[0] / tong_dt_nganh * 100  # Đây là giả định, bạn cần thay thế bằng cách tính của bạn
phan_con_lai = 100 - ty_le_dt_hpg

# Tạo biểu đồ
fig_ln_hpg = go.Figure(data=[go.Pie(labels=['Hòa Phát Group', 'Các công ty thép còn lại'],
                                    values=[ty_le_dt_hpg, phan_con_lai],
                                    hoverinfo='label+percent+value',
                                    textinfo='percent')])
# Tính giá trị còn lại của ngành sau khi loại trừ doanh thu thuần của HPG
cong_ty_con_lai_value = tong_dt_nganh - doanh_thu_thuan_hpg_values[0]
doanh_thu_thuan_hpg_values[0] /= 1e9
cong_ty_con_lai_value /= 1e9
# Cập nhật hovertemplate cho biểu đồ
fig_ln_hpg.update_traces(hovertemplate=[
    'HPG: %{value:.2f}%<br>Doanh thu thuần: ' + str(doanh_thu_thuan_hpg_values[0]) + ' Tỷ VNĐ',
    'Công ty thép còn lại: %{value:.2f}%<br>Doanh thu thuần: ' + str(cong_ty_con_lai_value) + 'Tỷ VNĐ'
])
# Cấu hình tiêu đề của biểu đồ
fig_ln_hpg.update_layout(title_text='Tỷ lệ Doanh thu thuần của HPG so với tổng ngành thép năm 2022')

if selected == "Tổng quan ngành":
    st.plotly_chart (fig_tree_map, use_container_width=True)
    st.plotly_chart(fig_ln_n, use_container_width=True)
    st.plotly_chart(fig_ln_hpg, use_container_width=True)
    st.plotly_chart(fig_industry, use_container_width=True)

######CHỈ SỐ TÀI CHÍNH
import pandas as pd
data_sl1 = {
    'Năm': ['2018', '2019', '2020', '2021', '2022'],
    'Tỷ suất lợi nhuận gộp biên (%)': gross_profit_margin,
    'Tỷ lệ lãi EBIT (%)': ebit_margin,
    'Tỷ lệ lãi EBITDA (%)': ebitda_margin,
    'Tỷ suất sinh lợi trên doanh thu thuần (%)': profit_ratio
}
data_sl2 = {
    'Năm': [ '2019', '2020', '2021', '2022'],
    'Tỷ số ROAA (%)': ty_le_roaa,
    'Tỷ số ROCE (%)': ty_le_roce,
    'Tỷ số ROEA (%)': ty_le_roea
}
# Create a DataFrame from the dictionary
df_chiso_tc1 = pd.DataFrame(data_sl1)
df_chiso_tc1.index.name = None
df_chiso_tc1 = df_chiso_tc1.round(2)
df_chiso_tc1 = df_chiso_tc1.transpose()
df_chiso_tc2 = pd.DataFrame(data_sl2)
df_chiso_tc2.index.name = None
df_chiso_tc2 = df_chiso_tc2.transpose()
data_tt = {
    'Năm': ['2019', '2020', '2021', '2022'],
    'Tăng trưởng doanh thu (%)': ty_le_tang_truong_doanh_thu,
    'Tăng trưởng lợi nhuận gộp (%)': ty_le_tang_truong_loi_nhuan_gop,
    'Tăng trưởng lợi nhuận trước thuế (%)': ty_le_tang_truong_loi_nhuan_truoc_thue
}
df_tyle_tt = pd.DataFrame(data_tt)
df_tyle_tt.index.name = None
df_tyle_tt = df_tyle_tt.transpose()
data_tk = {
    'Năm': ['2018','2019', '2020', '2021', '2022'],
    'Tỷ số thanh toán bằng tiền mặt (Lần)': ty_le_tt_tm,
    'Tỷ số thanh toán nhanh (Lần)': ty_le_ttn,
    'Tỷ số thanh toán hiện hành (ngắn hạn) (Lần)': ty_le_tthh,
    'Khả năng thanh toán lãi vay': ty_le_ttlv
}
df_tyle_tk = pd.DataFrame(data_tk)
df_tyle_tk.index.name = None
df_tyle_tk= df_tyle_tk.transpose()
data_dbtc = {
    'Năm': ['2018','2019', '2020', '2021', '2022'],
    'Tỷ số Nợ ngắn hạn trên Nợ phải trả ': ty_le_nnh_npt,
    'Tỷ số Nợ vay trên Tổng tài sản': ty_le_nv_tts,
    'Tỷ số Nợ trên Tổng tài sản': ty_le_no_tts,
    'Tỷ số Vốn chủ sở hữu trên Tổng tài sản': ty_le_vcsh_tts,
    'Tỷ số Nợ ngắn hạn trên Vốn chủ sở hữu': ty_le_nnh_vcsh,
    'Tỷ số Nợ vay trên Vốn chủ sở hữu': ty_le_nv_vcsh,
    'Tỷ số Nợ trên Vốn chủ sở hữu' : ty_le_no_vcsh
}
df_tyle_dbtc = pd.DataFrame(data_dbtc)
df_tyle_dbtc.index.name = None
df_tyle_dbtc= df_tyle_dbtc.transpose()
data_dongtien = {
    'Năm': ['2018','2019', '2020', '2021', '2022'],
    'Tỷ số dòng tiền HĐKD trên doanh thu thuần': ty_le_hdkd_dtt,
    'Khả năng chi trả nợ ngắn hạn từ dòng tiền HĐKD': ty_le_tra_no_hdkd,
    'Dòng tiền từ HĐKD trên Tổng tài sản': ty_le_hdkd_tts,
    'Dòng tiền từ HĐKD trên Vốn chủ sở hữu': ty_le_hdkd_vcsh,
    'Dòng tiền từ HĐKD trên Lợi nhuận thuần từ HĐKD': ty_le_hdkd_lnt,
    'Khả năng thanh toán nợ từ dòng tiền HĐKD:': ty_le_hdkd_npt
}
df_tyle_dongtien = pd.DataFrame(data_dongtien)
df_tyle_dongtien.index.name = None
df_tyle_dongtien= df_tyle_dongtien.transpose()
if selected == "Tài chính":
    if selected_sub_category_fi == "None":
        st.empty()
    elif selected_sub_category_fi == "Biểu đồ tài chính":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(fig_dt, use_container_width=True)  # use_container_width để tự động điều chỉnh chiều rộng
        with col2:
            st.plotly_chart(fig_ln, use_container_width=True)
        with col3:
            st.plotly_chart(fig_dtt_ln, use_container_width=True )
        col4, col5, col6 = st.columns(3)
        with col4:
            st.plotly_chart(fig_margin, use_container_width=True)
        with col5:
            st.plotly_chart(fig_ts)
        with col6:
            st.empty()
    elif selected_sub_category_fi == "Chỉ số tài chính":
        chart_sl = False
        st.markdown('# <span style="color: blue; font-size: 20px;">NHÓM CHỈ SỐ SINH LỢI:</span>',
                    unsafe_allow_html=True)
        if st.button('VẼ BIỂU ĐỒ CHỈ SỐ SINH LỢI'):
            st.empty()
            chart_sl = True
        st.write(df_chiso_tc1)
        st.write(df_chiso_tc2)
        if chart_sl:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_ty_le_lngb, use_container_width=True)
            with col2:
                st.plotly_chart(fig_ebitda, use_container_width=True)
            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(fig_ebit, use_container_width=True)
            with col4:
                st.plotly_chart(fig_ty_le_sl_dtt, use_container_width=True)
            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(fig_ty_le_roaa, use_container_width=True)
            with col6:
                st.plotly_chart(fig_ty_le_roce, use_container_width=True)
            col7, col8 = st.columns(2)
            with col7:
                st.plotly_chart(fig_ty_le_roea, use_container_width=True)
            with col8:
                st.empty()
        chart_tt = False
        st.markdown('# <span style="color: blue; font-size: 20px;">NHÓM CHỈ SỐ TĂNG TRƯỞNG:</span>',
                    unsafe_allow_html=True)
        if st.button('VẼ BIỂU ĐỒ CHỈ SỐ TĂNG TRƯỞNG'):
            st.empty()
            chart_tt = True
        st.write(df_tyle_tt)
        if chart_tt:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.plotly_chart(fig_ty_le_tang_truong_doanh_thu, use_container_width=True)
            with col2:
                st.plotly_chart(fig_ty_le_tang_truong_loi_nhuan_gop, use_container_width=True)
            with col3:
                st.plotly_chart(fig_ty_le_tang_truong_loi_nhuan_truoc_thue, use_container_width=True)
        #####NHÓM CHỈ SỐ THANH KHOẢN VÀ VẼ BIỂU ĐỒ KHI CẦN:
        chart_tk = False
        st.markdown('# <span style="color: blue; font-size: 20px;">NHÓM CHỈ SỐ THANH KHOẢN:</span>',
                    unsafe_allow_html=True)
        if st.button('VẼ BIỂU ĐỒ CHỈ SỐ THANH KHOẢN'):
            st.empty()
            chart_tk = True
        st.write(df_tyle_tk)
        if chart_tk:
            # If the button is clicked, plot the chart
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_ty_le_tt_tm, use_container_width=True)
            with col2:
                st.plotly_chart(fig_ty_le_ttn, use_container_width=True)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(fig_ty_le_tthh, use_container_width=True)
            with col4:
                st.plotly_chart(fig_ty_le_ttlv, use_container_width=True)
#####NHÓM CHỈ SỐ ĐÒN BẪY TÀI CHÍNH VÀ VẼ BIỂU ĐỒ KHI CẦN:
        chart_dbtc = False
        st.markdown('# <span style="color: blue; font-size: 20px;">NHÓM CHỈ SỐ ĐÒN BẨY TÀI CHÍNH:</span>',
                    unsafe_allow_html=True)
        if st.button('VẼ BIỂU ĐỒ CHỈ SỐ ĐÒN BẨY TÀI CHÍNH'):
            st.empty()
            chart_dbtc = True
        st.write(df_tyle_dbtc)
        if chart_dbtc:
            # If the button is clicked, plot the chart
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_ty_le_nnh_npt, use_container_width=True)
            with col2:
                st.plotly_chart(fig_ty_le_nv_tts, use_container_width=True)

            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(fig_ty_le_no_tts, use_container_width=True)
            with col4:
                st.plotly_chart(fig_ty_le_vcsh_tts, use_container_width=True)

            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(fig_ty_le_nnh_vcsh, use_container_width=True)
            with col6:
                st.plotly_chart(fig_ty_le_nv_vcsh, use_container_width=True)
            col7, col8 = st.columns(2)
            with col7:
                st.plotly_chart(fig_ty_le_no_vcsh, use_container_width=True)
            with col8:
                st.write('')
#####NHÓM CHỈ SỐ DÒNG TIỀN VÀ VẼ BIỂU ĐỒ KHI CẦN:
        chart_dt = False
        st.markdown('# <span style="color: blue; font-size: 20px;">NHÓM CHỈ SỐ DÒNG TIỀN:</span>',
                    unsafe_allow_html=True)
        if st.button('VẼ BIỂU ĐỒ CHỈ SỐ DÒNG TIỀN'):
            # Set the visibility to True when the button is clicked
            chart_dt = True
        st.write(df_tyle_dongtien)
        if chart_dt:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_ty_le_hdkd_dtt, use_container_width=True)
            with col2:
                st.plotly_chart(fig_ty_le_tra_no_hdkd, use_container_width=True)
            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(fig_ty_le_hdkd_tts, use_container_width=True)
            with col4:
                st.plotly_chart(fig_ty_le_hdkd_vcsh, use_container_width=True)
            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(fig_ty_le_hdkd_lnt, use_container_width=True)
            with col6:
                st.plotly_chart(fig_ty_le_hdkd_npt, use_container_width=True)









