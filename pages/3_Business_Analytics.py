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
left, right = st.columns([4,1])

with left:
    st.title("📊 Business Analytics")
    st.caption("Operational Performance Dashboard")

with right:
    st.write("")
    st.write("")
    st.button("Refresh Analytics")
    total_products = df["Item_Identifier"].nunique()

avg_mrp = df["Item_MRP"].mean()

avg_visibility = df["Item_Visibility"].mean()

avg_sales = df["Item_Outlet_Sales"].mean()
k1,k2,k3,k4 = st.columns(4)

metrics = [

("📦 Products",f"{total_products:,}"),

("💲 Avg MRP",f"${avg_mrp:,.2f}"),

("👀 Visibility",f"{avg_visibility:.3f}"),

("📈 Avg Sales",f"${avg_sales:,.0f}")

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
#left chart1
fig1 = px.histogram(
    df,
    x="Item_MRP",
    nbins=30,
    color_discrete_sequence=["#22c55e"]
)

fig1.update_layout(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",

    height=500,

    margin=dict(
        l=60,
        r=30,
        t=60,
        b=60
    ),

    title={
        "text": "Product Price Distribution",
        "font": {"size": 22, "color": "white"}
    },

    bargap=0.05
)

chart1.plotly_chart(
    fig1,
    width="stretch",
    config={"displayModeBar":False}
)
#right chart 1
size = (
    df.groupby("Outlet_Size")
      .size()
      .reset_index(name="Count")
)

fig2 = px.pie(
    size,
    values="Count",
    names="Outlet_Size",
    hole=0.60,
    color_discrete_sequence=px.colors.sequential.Tealgrn
)

fig2.update_layout(
    title={
        "text":"Outlet Size Analysis",
        "font":{"size":22,"color":"white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    height=430
)

chart2.plotly_chart(
    fig2,
    width="stretch",
    config={"displayModeBar":False}
)

st.markdown("<br>", unsafe_allow_html=True)

chart3, chart4 = st.columns(2, gap="large")
#leftchart2
fig3 = px.scatter(
    df,
    x="Item_Visibility",
    y="Item_Outlet_Sales",
    color="Item_MRP",
    color_continuous_scale="Viridis",
    hover_data=["Item_Type"]
)

fig3.update_layout(
    title={
        "text":"Visibility vs Sales",
        "font":{"size":22,"color":"white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    coloraxis_colorbar=dict(title="MRP"),
    height=430
)

chart3.plotly_chart(
    fig3,
    width="stretch",
    config={"displayModeBar":False}
)

#rightchart2
outlet = (
    df.groupby("Outlet_Type")["Item_Outlet_Sales"]
      .sum()
      .reset_index()
)

fig4 = px.bar(
    outlet,
    x="Outlet_Type",
    y="Item_Outlet_Sales",
    color="Item_Outlet_Sales",
    color_continuous_scale="Greens"
)

fig4.update_layout(
    title={
        "text": "Revenue by Outlet Type",
        "font": {"size": 22, "color": "white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",

    coloraxis_showscale=False,

    xaxis_title="",
    yaxis_title="Revenue",

    height=430,

    margin=dict(
        l=20,
        r=50,   # Increased right margin
        t=60,
        b=80    # More space for x-axis labels
    ),

    xaxis=dict(
        tickangle=-15,
        automargin=True
    )
)

chart4.plotly_chart(
    fig4,
    width="stretch",
    config={"displayModeBar":False}
)

#executive summary'
st.markdown("---")

best_outlet = (
    df.groupby("Outlet_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

best_size = (
    df.groupby("Outlet_Size")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

best_location = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

highest_mrp = df["Item_MRP"].max()
avg_visibility = df["Item_Visibility"].mean()
st.markdown(
    f"""
<div style="
background:#1f2937;
padding:28px;
border-radius:18px;
border-left:6px solid #22c55e;
border:1px solid #374151;
margin-bottom:20px;
">

<h3 style="color:white;">
📊 Executive Summary
</h3>

<p style="font-size:17px;color:#d1d5db;line-height:1.9;">

✅ <b>{best_outlet}</b> is the highest revenue generating outlet type.<br><br>

✅ <b>{best_size}</b> outlets contribute the largest share of business.<br><br>

✅ <b>{best_location}</b> delivers the strongest regional performance.<br><br>

✅ Highest product MRP in current selection is <b>${highest_mrp:,.2f}</b>.<br><br>

✅ Average product visibility is <b>{avg_visibility:.3f}</b>.<br><br>

<b style="color:#22c55e;">
📈 Business Decision:<br>
Focus inventory expansion in {best_location} through {best_outlet} outlets while maintaining high-visibility premium products to maximize profitability.
</b>

</p>

</div>
""",
    unsafe_allow_html=True,
)