import os
import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='EU banking sector dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# set path
os.chdir("C:/Users/Ilja/OneDrive/MyProjects/EU_banking_sector_dashboard")

# -----------------------------------------------------------------------------
# Declare some useful functions.


# -----------------------------------------------------------------------------
# read the data set
dfc = pd.read_csv('data/dfc.csv')

# -----------------------------------------------------------------------------
# User is choosing bank name

bank_list = dfc['Bank_name'].unique()
selected_bank = st.selectbox("Select a Bank", options=bank_list)

ind = 'NPL_ratio'
chart_data = dfc[(dfc.Bank_name == selected_bank)&(dfc.ind==ind)&(~dfc.sector.str.contains(r'^[A-Z]\s'))].copy() # the last filter is for non NACE codes
chart_data = chart_data[chart_data.Amount > 0]
max_date = chart_data.Period.max()
bank_name = chart_data.Bank_name.unique()[0]
# chart_data = chart_data[chart_data.Amount > 0.001]

# creating wrapped labels
def wrap_labels(label, width=10):
    return "<br>".join(textwrap.wrap(label, width=width))
chart_data['sector'] = chart_data['sector'].apply(lambda x: wrap_labels(x, width=15))

# creating custom sort of groups
custom_sector_order = list(chart_data[chart_data.Period == max_date].groupby('sector')['Amount'].max().sort_values(ascending=False).reset_index().sector.values)
custom_sector_order.remove('Total')
custom_sector_order.append('Total')
chart_data['sector'] = pd.Categorical(chart_data['sector'], categories=custom_sector_order, ordered=True)

# converting data to string
chart_data['Period'] = chart_data['Period'].astype('object')

# making the chart
fig = px.bar(
    chart_data,
    x="sector",
    y="Amount",
    color="Period",
    barmode="group",
    title="NPL ratio by segments, "+bank_name,
    labels={"Amount": ind.replace("_"," "), "sector": "", "Period": "Period"},
    category_orders={
        "sector": custom_sector_order,
        # "Period": custom_period_order
    }
)
fig.update_layout(yaxis_tickformat='.1%')
fig.update_layout(
    width=1200,
    height=740,
    autosize=False,
    template='none'
)

st.plotly_chart(fig, use_container_width=True)