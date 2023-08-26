import pandas as pd
import streamlit as st
import plotly_express as px
import datetime


st.set_page_config(page_title="Salesdashboard", layout='wide')


df=pd.read_excel('supermarket_sales-Sheet1.xlsx')

#---sidebar---  
st.sidebar.header("Please Filter Here: ")
city=st.sidebar.multiselect(
    "Select the City: ",
    options=df["City"].unique(),
    default=df["City"].unique()
)


gender=st.sidebar.multiselect(
    "Select the Gender: ",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City== @city  & Gender== @gender"
)

#---title---
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#---KPI Section---
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:},")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

    st.markdown("---")

#---sales_by_product_line barchart---

sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",


)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#---sales_by_hour_ barchart---

sales_by_hour = df_selection.groupby(by=["Time"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)


sales_by_hour = df_selection.groupby(by=["Time"]).sum()

#---fig_hourly_sales pie chart---

fig_hourly_sales_pie = px.pie(
    sales_by_hour,
    values="Total",
    names=sales_by_hour.index,
    title="<b>Sales distribution by hour</b>",
    template="plotly_white",
)

fig_hourly_sales_pie.update_traces(textposition = 'inside',textinfo="percent+label",)


left_column, middle_column, right_column = st.columns(3)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
middle_column.plotly_chart(fig_hourly_sales_pie, use_container_width=True)
right_column.plotly_chart(fig_hourly_sales, use_container_width=True)














