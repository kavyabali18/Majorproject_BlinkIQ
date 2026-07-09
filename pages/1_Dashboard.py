import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_css

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="BlinkIQ Dashboard",
    page_icon="🛒",
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

# ---------------- SIDEBAR FILTERS ----------------

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

# Apply Filters
df = df[
    (df["Outlet_Size"].isin(outlet)) &
    (df["Item_Fat_Content"].isin(fat)) &
    (df["Outlet_Location_Type"].isin(location))
]

# ---------------- HEADER ----------------

left, right = st.columns([4, 1])

with left:
    st.title("🛒 BlinkIQ")
    st.caption("Retail Sales Intelligence Dashboard")

with right:
    st.write("")
    st.write("")
    st.button("Refresh Data")

    # ================= KPIs =================

k1, k2, k3, k4 = st.columns(4)

metrics = [
    ("💰 Total Sales", f"${df['Item_Outlet_Sales'].sum()/1e6:.2f} M"),
    ("📈 Avg Sales", f"${df['Item_Outlet_Sales'].mean():,.0f}"),
    ("📦 Products", f"{df['Item_Identifier'].nunique():,}"),
    ("🏪 Outlets", f"{df['Outlet_Identifier'].nunique()}")
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
font-size:24px;
font-weight:650;
">{value}</h2>

</div>
""",
            unsafe_allow_html=True,
        )
st.markdown("<br>", unsafe_allow_html=True)

chart1, chart2 = st.columns(2, gap="large")

#left donutchart 
fat_sales = (
    df.groupby("Item_Fat_Content")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig1 = px.pie(
    fat_sales,
    values="Item_Outlet_Sales",
    names="Item_Fat_Content",
    hole=0.65,
    color_discrete_sequence=["#22c55e", "#fbbf24"]
)

fig1.update_layout(
    title={
        "text":"Sales by Fat Content",
        "font":{"size":22,"color":"white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    legend_title="",
    margin=dict(l=10,r=10,t=60,b=10)
)

chart1.plotly_chart(fig1, width="stretch")
#right horizontal bar chart
top_items = (
    df.groupby("Item_Type")["Item_Outlet_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(8)
)

fig2 = px.bar(
    top_items,
    orientation="h",
    color=top_items.values,
    color_continuous_scale="Greens"
)

fig2.update_layout(
    title={
        "text":"Top Selling Categories",
        "font":{"size":22,"color":"white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    coloraxis_showscale=False,
    margin=dict(l=10,r=10,t=60,b=10)
)

chart2.plotly_chart(fig2, width="stretch")
#sales outlet chart
st.markdown("###")

left, right = st.columns(2)
outlet_sales = (
    df.groupby("Outlet_Identifier")["Item_Outlet_Sales"]
      .sum()
      .reset_index()
)

fig3 = px.bar(
    outlet_sales,
    x="Outlet_Identifier",
    y="Item_Outlet_Sales",
    color="Item_Outlet_Sales",
    color_continuous_scale="Viridis"
)

fig3.update_layout(
    title={
        "text": "Outlet Sales Comparison",
        "font": {"size": 22, "color": "white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",

    xaxis_title="Sales",
    yaxis_title="Outlet",

    showlegend=False,

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    ),

    height=430
)

left.plotly_chart(
    fig3,
    width="stretch",
    config={"displayModeBar": False}
)
#Outlet Size Distribution
size = (
    df.groupby("Outlet_Size")
      .size()
      .reset_index(name="Count")
)

fig4 = px.pie(
    size,
    values="Count",
    names="Outlet_Size",
    hole=0.55,
    color_discrete_sequence=px.colors.sequential.Teal
)

fig4.update_layout(
    title={
        "text":"Outlet Size Distribution",
        "font":{"size":22,"color":"white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white"
)

right.plotly_chart(fig4, width="stretch")
#SALES SUMMARY

st.markdown("---")
st.subheader("📋 Sales Summary")
summary_df = (
    df.groupby("Outlet_Type")
      .agg(
          Total_Sales=("Item_Outlet_Sales", "sum"),
          Average_Sales=("Item_Outlet_Sales", "mean"),
          Products=("Item_Identifier", "count")
      )
      .reset_index()
)
summary_df["Total_Sales"] = summary_df["Total_Sales"].apply(
    lambda x: f"${x:,.0f}"
)

summary_df["Average_Sales"] = summary_df["Average_Sales"].apply(
    lambda x: f"${x:,.2f}"
)

summary_df["Products"] = summary_df["Products"].apply(
    lambda x: f"{x:,}"
)
summary_df.columns = [
    "Outlet Type",
    "Total Sales",
    "Average Sales",
    "Products"
]
st.dataframe(
    summary_df,
    hide_index=True,
    width="stretch"
)
st.markdown("---")
# Highest revenue outlet
st.markdown("---")
st.subheader("🧠 Smart Business Insights")

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

best_fat = (
    df.groupby("Item_Fat_Content")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

best_location = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

best_size = (
    df.groupby("Outlet_Size")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

location_sales = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
)

location_share = (
    location_sales.max() /
    location_sales.sum()
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
🧠 Smart Business Insights
</h3>

<p style="font-size:17px;color:#d1d5db;line-height:1.9;">

🏪 <b>Best Outlet Type</b><br>
{best_outlet} generates the highest revenue.<br><br>

🥇 <b>Top Category</b><br>
{best_category} is currently the highest-selling category.<br><br>

🥛 <b>Preferred Fat Content</b><br>
{best_fat} products contribute the most revenue.<br><br>

📍 <b>Best Market</b><br>
{best_location} contributes nearly <b>{location_share:.1f}%</b> of the selected revenue.<br><br>

🏬 <b>Top Outlet Size</b><br>
{best_size} outlets perform the strongest in the current selection.<br><br>

<hr>

<b style="color:#22c55e;font-size:18px;">
🚀 Business Recommendation
</b>

<p style="font-size:17px;color:white;">
Increase inventory of <b>{best_category}</b> products in
<b>{best_outlet}</b> stores across
<b>{best_location}</b> locations, with a focus on
<b>{best_size}</b> outlets to maximize revenue.
</p>

</div>
""",
    unsafe_allow_html=True
)
st.markdown("---")

st.subheader("📥 Export Dashboard Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv,
    file_name="BlinkIQ_Filtered_Report.csv",
    mime="text/csv",
    use_container_width=True
)