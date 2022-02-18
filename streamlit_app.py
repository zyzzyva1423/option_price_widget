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

# Getting data

client = MongoClient()
db = client['options']

pre = list(db.tsla.find({'lastTradeDate' : '2022-02-11'},
                 {'_id' : 0,
                  'data.options.CALL.expirationDate' : 1,
                  'data.options.CALL.strike' : 1, 'data.options.CALL.bid' : 1,
                  'data.options.CALL.ask' : 1}))

df = pd.DataFrame.from_dict(pre[0]['data'][0]['options']['CALL'])

### PART 1 - Agenda
#
#st.write('''
## Welcome To Streamlit!
#In this Streamlit app we will cover:
#
#- Markdown
#- Importing data
#- Displaying dataframes
#- Graphing
#- Interactivity with buttons
#- Mapping
#- Making predictions with user input
#''')


## PART 2 - Markdown Syntax
#
#st.write(
#'''
### Markdown Syntax
#You can use Markdown syntax to style your text. For example,
#
## Main Title
### Subtitle
#### Header
#
#**Bold Text**
#
#*Italics*
#
#Ordered List
#
#1. Apples
#2. Oranges
#3. Bananas
#
#[This is a link!](https://docs.streamlit.io/en/stable/getting_started.html)
#
#'''
#)


# PART 3 - Seattle House Prices Table

st.write(
'''
### Bid-Ask Price of Tesla Call Option Expiring on Feb 18 2022
''')

st.dataframe(df)

# PART 4 - Graphing and Buttons

# st.write(
# '''
# ### Bid-Ask Price of Tesla Call Option Expiring on Feb 18 2022
# '''
# )
#
# fig, ax = plt.subplots()
#
# line1 = ax.plot(df['strike'], df['bid'], label='Bid')
# line2 = ax.plot(df['strike'], df['ask'], label='Ask')
# ax.set(xlabel='Strike Price', ylabel='Option Price')
# ax.legend()
# #ax.set_title('Distribution of House Prices in $100,000s')
#
# show_graph = st.checkbox('Show Graph', value=True)
#
# if show_graph:
#     st.pyplot(fig)


# PART 5 - Graphing and Sliders

st.write(
'''
### Bid-Ask Price of Tesla Call Option Expiring on Feb 18 2022
'''
)

#ax.set_title('Distribution of House Prices in $100,000s')

values = st.slider('Select a range for Strike Price', min(df.strike), max(df.strike),
                  (min(df.strike), max(df.strike)))
#st.write('Values:', values)

min = values[0]
max = values[1]

condition = (df.strike >= min) & (df.strike <= max)

fig, ax = plt.subplots()

line1 = ax.plot(df.strike[condition], df.bid[condition], label='Bid')
line2 = ax.plot(df.strike[condition], df.ask[condition], label='Ask')
ax.set(xlabel='Strike Price', ylabel='Option Price')
ax.legend()

st.pyplot(fig)
