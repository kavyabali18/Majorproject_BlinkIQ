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
df = df[
    (df["Outlet_Size"].isin(outlet)) &
    (df["Item_Fat_Content"].isin(fat)) &
    (df["Outlet_Location_Type"].isin(location))
]

if df.empty:
    st.warning("⚠ No data available for the selected filters.")
    st.stop()
#header
left, right = st.columns([4,1])

with left:
    st.title("🤖 AI Recommendations")
    st.caption("Decision Support & Business Strategy")

with right:
    st.write("")
    st.write("")
    st.button("Generate Insights")

best_category = (
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

best_category = category_map.get(best_category, best_category)
worst_category = (
    df.groupby("Item_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmin()
)
worst_category = category_map.get(worst_category, worst_category)
best_location = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

best_outlet = (
    df.groupby("Outlet_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

total_sales = df["Item_Outlet_Sales"].sum()
k1,k2,k3,k4 = st.columns(4)

metrics = [

("🚀 Growth Area", best_location),

("🏆 Best Category", best_category),

("⚠ Improve", worst_category),

("💰 Revenue", f"${total_sales/1e6:.2f} M")

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
font-size:18px;
font-weight:650;
">{value}</h2>

</div>
""",
            unsafe_allow_html=True,
        )
#revencue chart
chart1, chart2 = st.columns(2, gap="large")
category_map = {
    "Fruits and Vegetables": "Fruits & Veg.",
    "Health and Hygiene": "Health & Hygiene",
    "Frozen Foods": "Frozen Foods",
    "Soft Drinks": "Soft Drinks"
}

df_chart = df.copy()
df_chart["Item_Type"] = df_chart["Item_Type"].replace(category_map)
revenue = (
    df_chart.groupby("Item_Type")["Item_Outlet_Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(8)
      .reset_index()
)

fig1 = px.bar(
    revenue,
    x="Item_Type",
    y="Item_Outlet_Sales",
    color="Item_Outlet_Sales",
    color_continuous_scale="Greens"
)
fig1.update_layout(
    title={
        "text": "Revenue Opportunities",
        "font": {"size": 22, "color": "white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    coloraxis_showscale=False,
    height=430,
    xaxis_tickangle=-30,
    margin=dict(l=20, r=20, t=60, b=90)
)

chart1.plotly_chart(
    fig1,
    width="stretch",
    config={"displayModeBar":False}
)
#inventaory optimiazation
inventory = (
    df.groupby("Item_Fat_Content")["Item_Outlet_Sales"]
      .sum()
      .reset_index()
)

fig2 = px.pie(
    inventory,
    values="Item_Outlet_Sales",
    names="Item_Fat_Content",
    hole=0.68,
    color_discrete_sequence=["#22c55e", "#84cc16"]
)

fig2.update_traces(
    textposition="inside",
    textinfo="label+percent",
    pull=[0.03, 0]
)

fig2.update_layout(
    title={
        "text": "Inventory Optimization",
        "font": {"size": 22, "color": "white"}
    },
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    height=430,

    legend=dict(
        orientation="h",
        y=-0.15,
        x=0.25
    ),

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=60
    )
)

chart2.plotly_chart(
    fig2,
    width="stretch",
    config={"displayModeBar":False}
)
#buisness health score
sales_ratio = df["Item_Outlet_Sales"].sum() / 18591163

health_score = min(100, max(60, int(sales_ratio * 100)))
st.markdown("---")

st.markdown(
f"""
<div style="
background:#1f2937;
padding:30px;
border-radius:20px;
border-left:8px solid #22c55e;
border:1px solid #374151;
">

<h2 style="color:white;">
💚 Business Health Score
</h2>

<h1 style="font-size:58px;color:#22c55e;">
{health_score}%
</h1>

<p style="font-size:18px;color:#d1d5db;">

{"Excellent" if health_score>=90 else "Good" if health_score>=75 else "Needs Improvement"} Business Performance

Revenue is concentrated in <b>{best_category}</b>.

<b>{best_location}</b> continues to outperform other regions.

Investment should focus on expanding <b>{best_outlet}</b> outlets.

Inventory for <b>{worst_category}</b> should be optimized.

</p>

</div>
""",
unsafe_allow_html=True
)
#AI Recommendation Panel
st.markdown("---")

st.markdown(
f"""
<div style="
background:#1f2937;
padding:30px;
border-radius:20px;
border-left:8px solid #22c55e;
border:1px solid #374151;
">

<h2 style="color:white;">
🤖 AI Business Recommendations
</h2>

<p style="font-size:18px;color:#d1d5db;line-height:2;">

✅ Expand inventory of <b>{best_category}</b>.

<br><br>

✅ Increase investment in <b>{best_location}</b> outlets.

<br><br>

✅ Prioritize <b>{best_outlet}</b> for future expansion.

<br><br>

✅ Reduce inventory of <b>{worst_category}</b> and replace shelf space with high-demand products.

<br><br>

✅ Current filtered data indicates strong business growth potential.

</p>

</div>
""",
unsafe_allow_html=True
)
st.markdown("---")
st.subheader("📥 Export AI Recommendations")

report = f"""
BlinkIQ AI Recommendation Report

Business Health Score : {health_score}%

Best Category : {best_category}

Best Location : {best_location}

Best Outlet : {best_outlet}

Category to Improve : {worst_category}

Recommendation:

- Expand {best_category}
- Focus on {best_location}
- Invest in {best_outlet}
- Optimize {worst_category}
"""

st.download_button(
    "⬇ Download Recommendation Report",
    report,
    file_name="BlinkIQ_AI_Recommendations.txt"
)