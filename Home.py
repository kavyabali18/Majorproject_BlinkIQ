import streamlit as st
import pandas as pd
from utils import load_css

st.set_page_config(
    page_title="BlinkIQ",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
    
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
# ================= HERO SECTION =================

left, right = st.columns([1.2, 1], gap="large")

with left:

    st.markdown("""
    <h1 style="
    font-size:64px;
    font-weight:800;
    color:white;
    margin-bottom:5px;">
    BlinkIQ
    </h1>

    <h3 style="
    color:#22c55e;
    font-weight:600;">
    AI-Powered Retail Intelligence Platform
    </h3>

    <p style="
    font-size:19px;
    color:#cbd5e1;
    line-height:1.8;
    max-width:650px;">
    Transform retail sales data into actionable business insights using
    interactive dashboards, advanced analytics and AI-powered
    recommendations.
    </p>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns(2)

    with b1:
        if st.button("🚀 Explore Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")

    with b2:
        if st.button("📈 View Analytics", use_container_width=True):
            st.switch_page("pages/2_Sales_Insights.py")

products = df["Item_Identifier"].nunique()
outlets = df["Outlet_Identifier"].nunique()
revenue = df["Item_Outlet_Sales"].sum()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        label="📦 Products",
        value=f"{products:,}"
    )

with c2:
    st.metric(
        label="🏪 Outlets",
        value=f"{outlets}"
    )

with c3:
    st.metric(
        label="💰 Revenue",
        value=f"${revenue/1e6:.2f} M"
    )

with right:
    st.markdown("<div style='margin-top:75px;'></div>", unsafe_allow_html=True)
    st.image(
        "assets/hero.png",
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("✨ Platform Features")

features = [
    (
        "📊",
        "Interactive Dashboard",
        "Monitor KPIs, revenue and outlet performance in real time.",
        "Dashboard",
        "pages/1_Dashboard.py"
    ),

    (
        "📈",
        "Sales Insights",
        "Analyze sales trends, top-performing products and revenue.",
        "Sales",
        "pages/2_Sales_Insights.py"
    ),

    (
        "📉",
        "Business Analytics",
        "Explore operational KPIs with interactive visualizations.",
        "Business",
        "pages/3_Business_Analytics.py"
    ),

    (
        "🤖",
        "AI Recommendations",
        "Receive AI-driven recommendations for business growth.",
        "Recommendation",
        "pages/4_Recommendations.py"
    )
]

c1, c2 = st.columns(2)

for i in range(0, len(features), 2):

    for col, feature in zip([c1, c2], features[i:i+2]):

        icon, title, desc, key, page = feature

        with col:

            st.markdown(f"""
<div style="
background:#1f2937;
padding:22px;
border-radius:16px;
border:1px solid #374151;
margin-bottom:18px;
">

<div style="
display:flex;
align-items:center;
gap:14px;
">

<div style="
font-size:34px;
">
{icon}
</div>

<div>

<h3 style="
margin:0;
color:white;
">
{title}
</h3>

</div>

</div>

<p style="
margin-top:15px;
color:#cbd5e1;
line-height:1.7;
font-size:15px;
">
{desc}
</p>
</div>
""", unsafe_allow_html=True)
if st.button(
    f"Open {title}",
    key=key,
    use_container_width=True
):
    st.switch_page(page)

st.subheader("📊 Project Statistics")

products = df["Item_Identifier"].nunique()
outlets = df["Outlet_Identifier"].nunique()
revenue = df["Item_Outlet_Sales"].sum()
locations = df["Outlet_Location_Type"].nunique()

c1, c2, c3, c4 = st.columns(4)

stats = [
    ("📦 Products", f"{products:,}"),
    ("🏪 Outlets", f"{outlets}"),
    ("💰 Revenue", f"${revenue/1e6:.2f} M"),
    ("📍 Locations", f"{locations}")
]

for col, (title, value) in zip([c1,c2,c3,c4], stats):
    with col:
        st.markdown(f"""
<div style="
background:#1f2937;
padding:20px;
border-radius:18px;
border:1px solid #374151;
text-align:center;
">

<h4 style="color:#9ca3af;">{title}</h4>

<h2 style="color:white;font-size:30px;">
{value}
</h2>

</div>
""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🚀 Why BlinkIQ?")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("""
### ⚡ Fast Decisions

Analyze thousands of retail records instantly using interactive dashboards.
""")

with c2:
    st.info("""
### 🤖 AI Powered

Receive intelligent recommendations based on sales trends and business KPIs.
""")

with c3:
    st.info("""
### 📈 Better Growth

Identify high-performing outlets, products and optimize inventory.
""")
    
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🛠 Technology Stack")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.success("🐍 Python")

with c2:
    st.success("⚡ Streamlit")

with c3:
    st.success("📊 Plotly")

with c4:
    st.success("🧠 Pandas")
st.markdown("---")

st.markdown("""
<div style="text-align:center; color:#9ca3af; padding:20px;">

<h3 style="color:white;">BlinkIQ</h3>

AI-Powered Retail Intelligence Platform

Built using <b>Python • Streamlit • Pandas • Plotly</b>

Major Internship Project • 2026

</div>
""", unsafe_allow_html=True)