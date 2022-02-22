"""
To run this app:

1. cd into this directory
2. Run `streamlit run streamlit_app.py`
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pymongo import MongoClient
import json
import numpy as np
import pandas as pd

# 10 stocks and their tickers
stock_dict = {'AAPL' : 'Apple', 'AMC' : 'AMC', 'AMD' : 'Advanced Micro Devices',
             'AMZN' : 'Amazon', 'BAC' : 'Bank of America', 'FB' : 'Facebook',
             'INTC' : 'Intel', 'MSFT' : 'Microsoft', 'NVDA' : 'Nvidia',
             'TSLA' : 'Tesla'}

ticker = st.selectbox('Please select the ticker of a stock', tuple(stock_dict.keys()))

company = stock_dict[ticker]

# Getting data from MongoDB

username = st.secrets.db_credentials.username
password = st.secrets.db_credentials.password

url = "mongodb+srv://" + username + ":" + password + "@option-eod-price.hr02c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(url)
db = client['options']

# Cast the ticker selected from user to lower case
ticker = ticker.lower()

def get_trade_date(ticker):
    items = list(db[ticker].find({}, {'_id' : 0, 'lastTradeDate' : 1}))
    result = [d['lastTradeDate'] for d in items]
    return result

trade_date = st.selectbox('Please select the trade date', tuple(get_trade_date(ticker)))


def get_expiration_date(ticker, trade_date):
    items = db[ticker].find({'lastTradeDate' : trade_date},
                 {'_id' : 0,
                  'data.expirationDate' : 1})
    result = [d['expirationDate'] for d in list(items)[0]['data']]
    return result

expiration_date = st.selectbox('Please select the expiration date', tuple(get_expiration_date(ticker, trade_date)))

# Uses st.cache to only rerun when the query changes or after 10 min.
#st.cache(ttl=600)
def get_data(ticker, trade_date):
    items = db[ticker].find({'lastTradeDate' : trade_date},
                 {'_id' : 0,
                 'lastTradePrice' : 1,
                 'data.options.CALL.expirationDate' : 1,
                 'data.options.CALL.strike' : 1, 'data.options.CALL.bid' : 1,
                 'data.options.CALL.ask' : 1})
    return list(items)

pre = get_data(ticker, trade_date)

col1, col2 = st.columns(2)
col1.metric("Last Trade Date", trade_date)
col2.metric('Last Trade Price', pre[0]['lastTradePrice'])
#col3.metric("Humidity", "86%", "4%")

# Find the data for a specific expiration date
df_pre = pd.json_normalize(pre[0]['data'])
expiration_list = [x[0]['expirationDate'] for x in df_pre['options.CALL']]
expiration_index = expiration_list.index(expiration_date)

#
df = pd.DataFrame.from_dict(pre[0]['data'][expiration_index]['options']['CALL'])

st.write('### Bid-Ask Price of ', company, ' Call Option')

# Place holder for the chart
chart_placeholder = st.empty()

# Section: slider
values = st.slider('Select a range for Strike Price', min(df.strike), max(df.strike),
                  (min(df.strike), max(df.strike)))

min = values[0]
max = values[1]
condition = (df.strike >= min) & (df.strike <= max)

# Section: Plotting
fig, ax = plt.subplots()

line1 = ax.plot(df.strike[condition], df.bid[condition], label='Bid')
line2 = ax.plot(df.strike[condition], df.ask[condition], label='Ask')
ax.set(xlabel='Strike Price', ylabel='Option Price')
ax.legend()

# Push to chart to the placeholder
chart_placeholder.pyplot(fig)

# Section: Present the raw data table

st.write('### Bid-Ask Price of ', company, ' Call Option')
df.columns = ['Expiration Date', 'Strike Price', 'Bid', 'Ask']
st.dataframe(df[condition])


# Contact form
st.header(":mailbox: Get In Touch With Me!")

contact_form = '''
<form action="https://formsubmit.co/bf6d6425281aad492a3e9abd169e63e6" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
      <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
'''

st.markdown(contact_form, unsafe_allow_html=True)

# Use local CSS File for contact form
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")
