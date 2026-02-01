import streamlit as st
import pandas as pd

st.title('国内旅行の分析アプリ')

tab1, tab2, tab3 = st.tabs(['概要', '目的', '使い方'])
with tab1:
    st.header('概要')
    st.write('ここではこのアプリケーションの概要を説明します。')
    st.write('このアプリは日本の観光統計をデータの相関関係から分析できるツールです。')
with tab2:
    st.header('目的')
    st.write('ここではこのアプリケーションを作成した目的を説明します。')
    st.write('日本の各地域によって、旅行のスタイルにどのような違いがあるのかを明らかにするために作成しました。' )
    st.write('「お金をかけて長く泊まる旅行が多い地域」や「安く短く楽しむ旅行が多い地域」など、' )
    st.markdown('数字だけではわかりにくい**地域ごとの観光の特性を可視化**します。')
with tab3:
    st.header('使い方')
    st.write('ここではこのアプリケーションの概要を説明します。')
    st.write('1. 比べたい地域をサイドバーから選択することで、')
    st.write('   その地域での旅行で使われるお金にどのような関係があるのかがわかります。')
    st.write('2. 地域を選んだまま時期を切り替えることで季節ごとでの泊数や単価がどう変化するかがわかります。')

df = pd.read_csv('data-travel.csv')

df['旅行単価【円／人回】'] = pd.to_numeric(df['旅行単価【円／人回】'].astype(str).str.replace(',', ''), errors='coerce')
df['平均泊数【泊／人回】'] = pd.to_numeric(df['平均泊数【泊／人回】'], errors='coerce')
df = df.dropna(subset=['旅行単価【円／人回】', '平均泊数【泊／人回】'])

with st.sidebar:
    st.subheader('分析条件')
    season = st.selectbox('時期を選択してください', 
                         df['時間軸（年次、四半期）'].unique())
    place = st.multiselect('地域を選択してください（複数選択可）', 
                                   df['居住地'].unique(),
                                   default=['全国'])
    option = st.radio('表示内容を選択してください',
                      ['散布図（相関）', '棒グラフ（比較）', 'データ一覧'])

df = df[df['居住地'].isin(place)]
df = df[df['時間軸（年次、四半期）'] == season]

if option == '散布図（相関）':
    st.subheader('旅行単価と平均泊数の相関')
    st.scatter_chart(df,
                     x='平均泊数【泊／人回】', 
                     y='旅行単価【円／人回】',
                     color='居住地')

elif option == '棒グラフ（比較）':
    st.subheader('地域別の旅行単価比較')
    st.bar_chart(df,
                 x='居住地',
                 y='旅行単価【円／人回】',
                 color='居住地')

elif option == 'データ一覧':
    st.subheader('詳細データテーブル')
    st.dataframe(df)

avg_price = df['旅行単価【円／人回】'].mean()
max_stay = df['平均泊数【泊／人回】'].max()
total_count = len(df)
overall_avg = 49634
diff = avg_price - overall_avg

col1, col2, col3 = st.columns(3)
col1.metric("平均単価（全国平均との差）",
            f"{avg_price:,.0f} 円",
            f"{diff:,.0f}円")
col2.metric("最大泊数", f"{max_stay:.1f} 泊")
col3.metric("データ件数", f"{total_count} 件")