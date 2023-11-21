import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns


st.set_page_config(
    page_title="STOCK ANALYSIS", page_icon="chart_with_upwards_trend", layout="centered"
)
@st.cache_data
def openingPrice(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    main_chart = (
        alt.Chart(data ,title='OPENING PRICE')
        .mark_line()
        .encode(
            x=alt.X("Date", title="DATE"),
            y=alt.Y("open", title="PRICE"),
            color="ticker",
        )
    )
    
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("open", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()
@st.cache_data
def volume(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    main_chart = (
        alt.Chart(data ,title='VOLUME')
        .mark_line()
        .encode(
            x=alt.X("Date", title="DATE"),
            y=alt.Y("volume", title="volume"),
            color="ticker",
        )
    )
    
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("volume", title=""),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()
@st.cache_data
def totalTrade(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    data['total_trade'] = data['open']*data['volume']
    st.dataframe(data)
    main_chart = (
        alt.Chart(data ,title='TOTAL TRADE')
        .mark_line()
        .encode(
            x=alt.X("Date", title="DATE"),
            y=alt.Y("total_trade", title="Total Trade"),
            color="ticker",
        )
    )
    
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("total_trade", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()
@st.cache_data
def MovingAvg(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    main_chart = (
        alt.Chart(data ,title='MOVING AVERAGE')
        .mark_line()
        .encode(
            x=alt.X("Date", title="DATE"),
            y=alt.Y("open", title="PRICE"),
            color="ticker",
        )
    )
    ma50_chart = (
        alt.Chart(data)
        .mark_line()
        .encode(
            x=alt.X("Date"),
            y=alt.Y("ma50"),
            color=alt.value("#FFAA00"),
        )
    )
    ma200_chart = (
        alt.Chart(data)
        .mark_line()
        .encode(
            x=alt.X("Date"),
            y=alt.Y("ma200"),
            color=alt.value("#FFFFFF"),
        )
    )

    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("open", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips+ma50_chart+ ma200_chart).interactive()

@st.cache_data
def scatterMatrix(data):
    main_chart= alt.Chart(data).mark_circle().encode(
    alt.X(alt.repeat("column"), type='quantitative'),
    alt.Y(alt.repeat("row"), type='quantitative'),
    color='Origin:N'
    ).repeat(
    row=[data['open'][data["ticker"]=='GOOGL'],data['open'][data["ticker"]=='TSLA'],data['open'][data["ticker"]=='AMZN']],
    column=[data['open'][data["ticker"]=='AMZN'],data['open'][data["ticker"]=='TSLA'],data['open'][data["ticker"]=='GOOGL']]
    )
    return (main_chart).interactive()

@st.cache_data
def candle(df):
    open_close_color = alt.condition(
    "datum.open <= datum.close",
    alt.value("#06982d"),
    alt.value("#ae1325")
    )

    base = alt.Chart(df).encode(
    alt.X('Date:T')
        .axis(format='%y%m/%d', labelAngle=-45)
        .title('DATE'),
    color=open_close_color
    )
    rule = base.mark_rule().encode(
    alt.Y('low:Q')
        .title('Price')
        .scale(zero=False),
    alt.Y2('high:Q')
    )
    bar = base.mark_bar().encode(
    alt.Y('open:Q'),
    alt.Y2('close:Q')
    )
    return (rule+bar).interactive()

@st.cache_data
def Creturn(df,op):
    l = ((df['close'][df['ticker']==op]/ df['close'][df['ticker']==op].shift(1))-1).to_list()
    l2 = df['Date'][df['ticker']==op].to_list()
    tempDf = pd.DataFrame({
        'return':l
    })
    tempDf['Date'] = l2
    tempDf['creturn'] = (1 +tempDf['return']).cumprod()
    main_chart = (
        alt.Chart(tempDf ,title='CUMMULATIVE RETURNS')
        .mark_line()
        .encode(
            x=alt.X("Date", title="DATE"),
            y=alt.Y("creturn", title="Total Trade"),
            color=alt.value("#FFFFFF"),
        )
    )
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(tempDf)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y='creturn',
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("creturn", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()

@st.cache_data
def volatile(df,op):
    l1 =((df['close'][df['ticker']=='GOOGL']/ df['close'][df['ticker']=='GOOGL'].shift(1))-1).to_list()
    l2 = ((df['close'][df['ticker']=='AMZN']/ df['close'][df['ticker']=='AMZN'].shift(1))-1).to_list()
    l3 = ((df['close'][df['ticker']=='TSLA']/ df['close'][df['ticker']=='TSLA'].shift(1))-1).to_list()
    l4 = ((df['close'][df['ticker']=='AAPL']/ df['close'][df['ticker']=='AAPL'].shift(1))-1).to_list()
    l5 = ((df['close'][df['ticker']=='NFLX']/ df['close'][df['ticker']=='NFLX'].shift(1))-1).to_list()
    l6 = ((df['close'][df['ticker']=='MSFT']/ df['close'][df['ticker']=='MSFT'].shift(1))-1).to_list()
    tempDf = pd.DataFrame({
        'GOOGL':l1,'AMZN':l2,'TLSA':l3,'AAPL':l3,'NFLX':l5,'MSFT':l6
    })    
    
    if op == 'ALL IN ONE':
        main_chart = alt.Chart(tempDf,title='VOLATILITY').transform_fold(
        ['GOOGL','AMZN','TSLA','AAPL','NFLX','MSFT'],
        as_=['Experiment', 'Measurement']
        ).mark_bar(
        opacity=0.4,
        binSpacing=0
        ).encode(
        alt.X('Measurement:Q').bin(maxbins=100),
        alt.Y('count()').stack(None),
        alt.Color('Experiment:N')
        )
    else:
        main_chart = alt.Chart(tempDf,title='VOLATILITY').transform_fold(
        [op],
        as_=['Experiment', 'Measurement']
        ).mark_bar(
        opacity=0.4,
        binSpacing=0
        ).encode(
        alt.X('Measurement:Q').bin(maxbins=100),
        alt.Y('count()').stack(None),
        alt.Color('Experiment:N')
        )

    return main_chart.interactive()

def googlTT(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    data['total_trade'] = data['open']*data['volume']
    main_chart = alt.Chart(data).transform_filter(
        'datum.ticker==="GOOGL"'
        ).mark_area(
        line={'color':'darkgreen'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                   alt.GradientStop(color='darkgreen', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
        ).encode(
        alt.X('Date:T'),
        alt.Y('total_trade:Q')
        )
    
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("total_trade", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()

def aaplTT(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    data['total_trade'] = data['open']*data['volume']
    main_chart = alt.Chart(data).transform_filter(
        'datum.ticker==="AAPL"'
        ).mark_area(
        line={'color':'darkgreen'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                   alt.GradientStop(color='darkgreen', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
        ).encode(
        alt.X('Date:T'),
        alt.Y('total_trade:Q')
        )
    
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("total_trade", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()

def nflxTT(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    data['total_trade'] = data['open']*data['volume']
    main_chart = alt.Chart(data).transform_filter(
        'datum.ticker==="NFLX"'
        ).mark_area(
        line={'color':'darkred'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                   alt.GradientStop(color='darkgreen', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
        ).encode(
        alt.X('Date:T'),
        alt.Y('total_trade:Q')
        )
    
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("total_trade", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()

def tslaTT(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    data['total_trade'] = data['open']*data['volume']
    main_chart = alt.Chart(data).transform_filter(
        'datum.ticker==="TSLA"'
        ).mark_area(
        line={'color':'darkgreen'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                   alt.GradientStop(color='darkgreen', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
        ).encode(
        alt.X('Date:T'),
        alt.Y('total_trade:Q')
        )
    
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("total_trade", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()

def amznTT(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    data['total_trade'] = data['open']*data['volume']
    main_chart = alt.Chart(data).transform_filter(
        'datum.ticker==="AMZN"'
        ).mark_area(
        line={'color':'darkred'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                   alt.GradientStop(color='darkgreen', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
        ).encode(
        alt.X('Date:T'),
        alt.Y('total_trade:Q')
        )
    
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("total_trade", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()

def msftTT(data):
    global hover,tooltips,main_chart
    hover = alt.selection_single(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    data['total_trade'] = data['open']*data['volume']
    main_chart = alt.Chart(data).transform_filter(
        'datum.ticker==="MSFT"'
        ).mark_area(
        line={'color':'darkgreen'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                   alt.GradientStop(color='darkgreen', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
        ).encode(
        alt.X('Date:T'),
        alt.Y('total_trade:Q')
        )
    
    points = main_chart.transform_filter(hover).mark_circle(size=30)
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="open",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("total_trade", title="USD $"),
            ],
        )
        .add_selection(hover)
    )
    return (main_chart +points+ tooltips).interactive()

st.title(":red[STOCK ANALYSIS]")

df = pd.read_csv("Stock Prices.csv")
df["Date"] = pd.to_datetime(df["Date"])
df.drop(df.index[(df["ticker"] == "AAL")],axis=0,inplace=True)


options = st.selectbox(':green[SELECT STOCK]',['WELCOME','MSFT','AMZN','NFLX','AAPL','GOOGL','TSLA','ALL IN ONE'])

if options == 'WELCOME':
    st.header("WELCOME TO :red[STOCK ANALYSIS]")
    st.subheader('PROJECT MADE BY :green[VK KANKERWAL] FOR DATA ANALYSIS AND VISUALIZATION SUBJECT')
    st.write('GMAIL: codevkankerwal@gmail.com')
    st.write("LINKEDIN: [vineetkankerwal](https://www.linkedin.com/in/vineet-kankerwal-11145b260)")

elif options == 'ALL IN ONE':
    
    st.header('DATA')
    st.dataframe(df)

    st.header('OPENING PRICE')
    st.altair_chart(openingPrice(df),use_container_width=True)

    st.header('VOLUME TRADED')
    st.altair_chart(volume(df),use_container_width=True)

    st.header('TOTAL TRADE')
    st.altair_chart(totalTrade(df),use_container_width=True)

    st.header('CANDLE STICK')
    candleComp = st.radio(
        "Which stock's candle-stick do you want to see",
        [":rainbow[GOOGL]", "TLSA", "NFLX","MFST","AAPL","AMZN"],
        )
    if candleComp == ':rainbow[GOOGL]':
        st.altair_chart(candle(df[df['ticker']=='GOOGL']),use_container_width=True)
    elif candleComp=='TLSA':
        st.altair_chart(candle(df[df['ticker']=='TSLA']),use_container_width=True)
    elif candleComp=='NFLX':
        st.altair_chart(candle(df[df['ticker']=='NFLX']),use_container_width=True)
    elif candleComp=='MFST':
        st.altair_chart(candle(df[df['ticker']=='MFST']),use_container_width=True)
    elif candleComp=='AAPL':
        st.altair_chart(candle(df[df['ticker']=='AAPL']),use_container_width=True)
    elif candleComp=='AMZN':
        st.altair_chart(candle(df[df['ticker']=='AMZN']),use_container_width=True)


    st.header('VOLATILITY')
    st.altair_chart(volatile(df,options),use_container_width=True)
    # l =((df['close'][df['ticker']=='GOOGL'] / df['close'][df['ticker']=='GOOGL'].shift(1))-1).to_list() 
    # d = pd.DataFrame(l)
    # st.dataframe(d)

    # df['total_trade'] = df['open']*df['volume']

    st.header('MOVING AVERAGE')
    movingComp = st.radio(
        "Which stock's moving average do you want to see",
        [":rainbow[GOOGL]", "TLSA", "NFLX","MFST","AAPL","AMZN"],
        )
    df['ma50'] = df['open'].rolling(50).mean()
    df['ma200'] = df['open'].rolling(200).mean()
    if movingComp == ':rainbow[GOOGL]':
        st.altair_chart(MovingAvg(df[df['ticker']=='GOOGL']),use_container_width=True)
    elif movingComp=='TLSA':
        st.altair_chart(MovingAvg(df[df['ticker']=='TLSA']),use_container_width=True)
    elif movingComp=='NFLX':
        st.altair_chart(MovingAvg(df[df['ticker']=='NFLX']),use_container_width=True)
    elif movingComp=='MFST':
        st.altair_chart(MovingAvg(df[df['ticker']=='MFST']),use_container_width=True)
    elif movingComp=='AAPL':
        st.altair_chart(MovingAvg(df[df['ticker']=='AAPL']),use_container_width=True)
    elif movingComp=='AMZN':
        st.altair_chart(MovingAvg(df[df['ticker']=='AMZN']),use_container_width=True)


    # comp = pd.concat([df['open'][df["ticker"]=='GOOGL'],df['open'][df["ticker"]=='TSLA'],df['open'][df["ticker"]=='AMZN']],axis=1)
    comp = pd.DataFrame()
    l = df['open'][df['ticker']=='GOOGL'].to_list()
    comp['GOOGL'] = l
    l = df['open'][df["ticker"]=='TSLA'].to_list()
    comp['TSLA'] = l
    l = df['open'][df["ticker"]=='AMZN'].to_list()
    comp['close'] = l
    l = df['open'][df["ticker"]=='NFLX'].to_list()
    comp['NFLX'] =l
    l = df['open'][df["ticker"]=='MSFT'].to_list()
    comp['MFST'] = l
    l = df['open'][df["ticker"]=='AAPL'].to_list()
    comp['AAPL'] =l


    # st.altair_chart(scatterMatrix(df),use_container_width=True)

    # sns.pairplot(df.loc[:,['open','ticker']],hue='ticker')
    st.header('SCATTER MATRIX')
    st.pyplot(sns.pairplot(comp))


if options == 'GOOGL':
    st.header('DATA')
    st.dataframe(df[df['ticker']=='GOOGL'])

    st.header('OPENING PRICE')
    st.altair_chart(openingPrice(df[df['ticker']=='GOOGL']),use_container_width=True)

    st.header('VOLUME TRADED')
    st.altair_chart(volume(df[df['ticker']=='GOOGL']),use_container_width=True)

    st.header('TOTAL TRADE')
    st.altair_chart(googlTT(df[df['ticker']=='GOOGL']),use_container_width=True)

    st.header('CANDLE STICK')
    st.altair_chart(candle(df[df['ticker']=='GOOGL']),use_container_width=True)

    st.header('VOLATILITY')
    st.altair_chart(volatile(df,options),use_container_width=True)
    
    st.header('MOVING AVERAGE')
    df['ma50'] = df['open'].rolling(50).mean()
    df['ma200'] = df['open'].rolling(200).mean()
    st.altair_chart(MovingAvg(df[df['ticker']=='GOOGL']),use_container_width=True)

    st.header('CUMMULATIVE RETURNS')
    st.altair_chart(Creturn(df,options),use_container_width=True)
    
elif options == 'AAPL':
    st.header('DATA')
    st.dataframe(df[df['ticker']=='AAPL'])

    st.header('OPENING PRICE')
    st.altair_chart(openingPrice(df[df['ticker']=='AAPL']),use_container_width=True)

    st.header('VOLUME TRADED')
    st.altair_chart(volume(df[df['ticker']=='AAPL']),use_container_width=True)

    st.header('TOTAL TRADE')
    st.altair_chart(aaplTT(df[df['ticker']=='AAPL']),use_container_width=True)

    st.header('CANDLE STICK')
    st.altair_chart(candle(df[df['ticker']=='AAPL']),use_container_width=True)

    st.header('VOLATILITY')
    st.altair_chart(volatile(df,options),use_container_width=True)
    
    # st.header('MOVING AVERAGE')
    # df['ma50'] = df['open'].rolling(50).mean()
    # df['ma200'] = df['open'].rolling(200).mean()
    # st.altair_chart(MovingAvg(df[df['ticker']=='AAPL']),use_container_width=True)

    st.header('CUMMULATIVE RETURNS')
    st.altair_chart(Creturn(df,options),use_container_width=True)
    

if options == 'NFLX':
    st.header('DATA')
    st.dataframe(df[df['ticker']=='NFLX'])

    st.header('OPENING PRICE')
    st.altair_chart(openingPrice(df[df['ticker']=='NFLX']),use_container_width=True)

    st.header('VOLUME TRADED')
    st.altair_chart(volume(df[df['ticker']=='NFLX']),use_container_width=True)

    st.header('TOTAL TRADE')
    st.altair_chart(nflxTT(df[df['ticker']=='NFLX']),use_container_width=True)

    st.header('CANDLE STICK')
    st.altair_chart(candle(df[df['ticker']=='NFLX']),use_container_width=True)

    st.header('VOLATILITY')
    st.altair_chart(volatile(df,options),use_container_width=True)
    
    st.header('MOVING AVERAGE')
    df['ma50'] = df['open'].rolling(50).mean()
    df['ma200'] = df['open'].rolling(200).mean()
    st.altair_chart(MovingAvg(df[df['ticker']=='NFLX']),use_container_width=True)

    st.header('CUMMULATIVE RETURNS')
    st.altair_chart(Creturn(df,options),use_container_width=True)
    

if options == 'TSLA':
    st.header('DATA')
    st.dataframe(df[df['ticker']=='TSLA'])

    st.header('OPENING PRICE')
    st.altair_chart(openingPrice(df[df['ticker']=='TSLA']),use_container_width=True)

    st.header('VOLUME TRADED')
    st.altair_chart(volume(df[df['ticker']=='TSLA']),use_container_width=True)

    st.header('TOTAL TRADE')
    st.altair_chart(tslaTT(df[df['ticker']=='TSLA']),use_container_width=True)

    st.header('CANDLE STICK')
    st.altair_chart(candle(df[df['ticker']=='TSLA']),use_container_width=True)

    # st.header('VOLATILITY')
    # st.altair_chart(volatile(df,options),use_container_width=True)
    
    st.header('MOVING AVERAGE')
    df['ma50'] = df['open'].rolling(50).mean()
    df['ma200'] = df['open'].rolling(200).mean()
    st.altair_chart(MovingAvg(df[df['ticker']=='TSLA']),use_container_width=True)

    st.header('CUMMULATIVE RETURNS')
    st.altair_chart(Creturn(df,options),use_container_width=True)
    

if options == 'AMZN':
    st.header('DATA')
    st.dataframe(df[df['ticker']=='AMZN'])

    st.header('OPENING PRICE')
    st.altair_chart(openingPrice(df[df['ticker']=='AMZN']),use_container_width=True)

    st.header('VOLUME TRADED')
    st.altair_chart(volume(df[df['ticker']=='AMZN']),use_container_width=True)

    st.header('TOTAL TRADE')
    st.altair_chart(amznTT(df[df['ticker']=='AMZN']),use_container_width=True)

    st.header('CANDLE STICK')
    st.altair_chart(candle(df[df['ticker']=='AMZN']),use_container_width=True)

    st.header('VOLATILITY')
    st.altair_chart(volatile(df,options),use_container_width=True)
    
    st.header('MOVING AVERAGE')
    df['ma50'] = df['open'].rolling(50).mean()
    df['ma200'] = df['open'].rolling(200).mean()
    st.altair_chart(MovingAvg(df[df['ticker']=='AMZN']),use_container_width=True)

    st.header('CUMMULATIVE RETURNS')
    st.altair_chart(Creturn(df,options),use_container_width=True)
    

if options == 'MSFT':
    st.header('DATA')
    st.dataframe(df[df['ticker']=='MSFT'])

    st.header('OPENING PRICE')
    st.altair_chart(openingPrice(df[df['ticker']=='MSFT']),use_container_width=True)

    st.header('VOLUME TRADED')
    st.altair_chart(volume(df[df['ticker']=='MSFT']),use_container_width=True)

    st.header('TOTAL TRADE')
    st.altair_chart(msftTT(df[df['ticker']=='MSFT']),use_container_width=True)

    st.header('CANDLE STICK')
    st.altair_chart(candle(df[df['ticker']=='MSFT']),use_container_width=True)

    st.header('VOLATILITY')
    st.altair_chart(volatile(df,options),use_container_width=True)
    
    st.header('MOVING AVERAGE')
    df['ma50'] = df['open'].rolling(50).mean()
    df['ma200'] = df['open'].rolling(200).mean()
    st.altair_chart(MovingAvg(df[df['ticker']=='MSFT']),use_container_width=True)

    st.header('CUMMULATIVE RETURNS')
    st.altair_chart(Creturn(df,options),use_container_width=True)
    