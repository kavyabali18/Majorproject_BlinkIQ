import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_css, kpi_card

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Sales Insights",
    page_icon="📈",
    layout="wide"
)

load_css()
st.sidebar.markdown("""
<div style="
padding:8px 5px 18px 5px;
">

<h2 style="
color:white;
font-size:26px;
font-weight:700;
margin-bottom:0;">
<span style="color:#22c55e;">🛒</span> BlinkIQ
</h2>

<p style="
color:#22c55e;
margin-top:2px;
font-size:13px;
">
Retail Intelligence Platform
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
df = pd.read_csv("data/blinkit_cleaned.csv")



# ---------------- SIDEBAR ----------------

st.sidebar.markdown("---")
st.sidebar.header("Filters")

outlet = st.sidebar.multiselect(
    "Outlet Size",
    options=sorted(df["Outlet_Size"].dropna().unique()),
    default=sorted(df["Outlet_Size"].dropna().unique())
)

fat = st.sidebar.multiselect(
    "Fat Content",
    options=sorted(df["Item_Fat_Content"].dropna().unique()),
    default=sorted(df["Item_Fat_Content"].dropna().unique())
)

location = st.sidebar.multiselect(
    "Location",
    options=sorted(df["Outlet_Location_Type"].dropna().unique()),
    default=sorted(df["Outlet_Location_Type"].dropna().unique())
)

df = df[
    (df["Outlet_Size"].isin(outlet)) &
    (df["Item_Fat_Content"].isin(fat)) &
    (df["Outlet_Location_Type"].isin(location))
]

left, right = st.columns([4, 1])

with left:
    st.title("📈 Sales Insights")
    st.caption("Retail Performance Analytics")

with right:
    st.write("")
    st.write("")
    st.button("Refresh Insights")

   # ================= KPI Calculations =================

# ================= KPI VALUES =================

best_outlet = (
    df.groupby("Outlet_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

top_category = (
    df.groupby("Item_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)
category_map = {
    "Fruits and Vegetables": "Fruits & Veg.",
    "Health and Hygiene": "Health & Hygiene",
    "Soft Drinks": "Soft Drinks",
    "Frozen Foods": "Frozen Foods"
}

top_category = category_map.get(top_category, top_category)
top_location = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

highest_revenue = (
    df.groupby("Outlet_Type")["Item_Outlet_Sales"]
      .sum()
      .max()
)
k1, k2, k3, k4 = st.columns(4)

metrics = [

    ("🏪 Best Outlet",
     best_outlet.replace("Supermarket ", "")),

    ("🥇 Top Category",
     top_category),

    ("📍 Top Location",
     top_location),

    ("💰 Revenue",
     f"${highest_revenue/1e6:.2f} M")

]

for col, (title, value) in zip([k1, k2, k3, k4], metrics):

    with col:

        st.markdown(
            f"""
<div style="background:#1f2937;
padding:18px;
border-radius:18px;
border:1px solid #374151;
box-shadow:0 8px 20px rgba(0,0,0,0.25);">

<h4 style="margin:0;color:#9ca3af;">{title}</h4>

<h2 style="
margin-top:10px;
color:white;
font-size:26px;
font-weight:700;
">{value}</h2>

</div>
""",
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)
chart1, chart2 = st.columns(2, gap="large")
location_sales = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
      .reset_index()
)

fig1 = px.bar(
    location_sales,
    x="Item_Outlet_Sales",
    y="Outlet_Location_Type",
    orientation="h",
    color="Item_Outlet_Sales",
    color_continuous_scale="Tealgrn"
)

fig1.update_layout(

    title={
        "text":"Revenue by Outlet Type",
        "font":{"size":22,"color":"white"}
    },

    paper_bgcolor="#111827",
    plot_bgcolor="#111827",

    font_color="white",

    coloraxis_showscale=False,

    xaxis_title="Revenue",

    yaxis_title="",

    margin=dict(l=20,r=20,t=60,b=20),

    height=430
)

chart1.plotly_chart(
    fig1,
    width="stretch",
    config={"displayModeBar":False}
)
#right horizontal bar chart
size_sales = (
    df.groupby("Outlet_Size")["Item_Outlet_Sales"]
      .mean()
      .reset_index()
)

fig2 = px.bar(
    size_sales,
    x="Outlet_Size",
    y="Item_Outlet_Sales",
    color="Item_Outlet_Sales",
    color_continuous_scale="Viridis"
)

fig2.update_layout(

    title={
        "text":"Category Performance",
        "font":{"size":22,"color":"white"}
    },

    paper_bgcolor="#111827",

    plot_bgcolor="#111827",

    font_color="white",

    coloraxis_showscale=False,

    xaxis_title="",

    yaxis_title="Revenue",

    margin=dict(l=20,r=20,t=60,b=20),

    height=430
)

chart2.plotly_chart(
    fig2,
    width="stretch",
    config={"displayModeBar":False}
)
st.markdown("###")

chart3, chart4 = st.columns(2, gap="large")
location_sales = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
      .reset_index()
)

fig3 = px.pie(
    location_sales,
    values="Item_Outlet_Sales",
    names="Outlet_Location_Type",
    hole=0.60,
    color_discrete_sequence=px.colors.sequential.Tealgrn
)

fig3.update_layout(
    title={
        "text": "Revenue by Location",
        "font": {"size":22, "color":"white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    legend_title="",
    height=430
)

chart3.plotly_chart(
    fig3,
    width="stretch",
    config={"displayModeBar":False}
)
year_sales = (
    df.groupby("Outlet_Establishment_Year")["Item_Outlet_Sales"]
      .sum()
      .reset_index()
      .sort_values("Outlet_Establishment_Year")
)

# Outlet Establishment Revenue

year_sales = (
    df.groupby("Outlet_Establishment_Year")["Item_Outlet_Sales"]
      .sum()
      .reset_index()
      .sort_values("Outlet_Establishment_Year")
)

fig4 = px.bar(
    year_sales,
    x="Outlet_Establishment_Year",
    y="Item_Outlet_Sales",
    color="Item_Outlet_Sales",
    color_continuous_scale="Viridis"
)

fig4.update_layout(

    title={
        "text":"Revenue by Establishment Year",
        "font":{"size":22,"color":"white"}
    },

    paper_bgcolor="#111827",
    plot_bgcolor="#111827",

    font_color="white",

    coloraxis_showscale=False,

    xaxis_title="Establishment Year",

    yaxis_title="Revenue",

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    ),

    height=430
)

chart4.plotly_chart(
    fig4,
    width="stretch",
    config={"displayModeBar":False}
)

st.markdown("---")

# Dynamic Insights
best_outlet = (
    df.groupby("Outlet_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

best_category = (
    df.groupby("Item_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

best_location = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

best_year = (
    df.groupby("Outlet_Establishment_Year")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

location_share = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
)

share = (
    location_share.max() /
    location_share.sum()
) * 100

st.markdown(
    f"""
<div style="
background:#1f2937;
padding:28px;
border-radius:18px;
border-left:6px solid #22c55e;
border:1px solid #374151;
">

<h3 style="color:white;">
🧠 Smart Business Recommendations
</h3>

<p style="font-size:17px;color:#d1d5db;line-height:1.9;">

📈 <b>Strongest Outlet</b><br>
{best_outlet} generated the highest revenue.<br><br>

🥇 <b>Best Product Category</b><br>
{best_category} contributes the highest sales.<br><br>

📍 <b>Best Market</b><br>
{best_location} contributes approximately <b>{share:.1f}%</b> of total revenue.<br><br>

📅 <b>Best Establishment Year</b><br>
Outlets established in <b>{best_year}</b> generated the strongest revenue.<br><br>

<hr>

<b style="color:#22c55e;font-size:18px;">
🚀 Recommended Business Action
</b>

<p style="font-size:17px;color:white;">
Increase inventory for <b>{best_category}</b> products in
<b>{best_location}</b> using
<b>{best_outlet}</b> stores to maximize revenue.
</p>

</div>
""",
    unsafe_allow_html=True
)