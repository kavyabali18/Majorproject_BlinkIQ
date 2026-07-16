import streamlit as st
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
from utils import load_css

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="BlinkIQ AI Assistant",
    page_icon="🤖",
    layout="wide"
)

load_css()

# -----------------------------
# LOAD ENVIRONMENT
# -----------------------------
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/blinkit_cleaned.csv")

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# BUSINESS METRICS
# -----------------------------
total_revenue = df["Item_Outlet_Sales"].sum()

average_sales = df["Item_Outlet_Sales"].mean()

average_mrp = df["Item_MRP"].mean()

total_products = df["Item_Identifier"].nunique()

total_outlets = df["Outlet_Identifier"].nunique()

top_outlet = (
    df.groupby("Outlet_Identifier")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

top_outlet_sales = (
    df.groupby("Outlet_Identifier")["Item_Outlet_Sales"]
      .sum()
      .max()
)

lowest_outlet = (
    df.groupby("Outlet_Identifier")["Item_Outlet_Sales"]
      .sum()
      .idxmin()
)

lowest_outlet_sales = (
    df.groupby("Outlet_Identifier")["Item_Outlet_Sales"]
      .sum()
      .min()
)

best_category = (
    df.groupby("Item_Type")["Item_Outlet_Sales"]
      .sum()
      .idxmax()
)

category_sales = (
    df.groupby("Item_Type")["Item_Outlet_Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .to_string()
)

outlet_sales = (
    df.groupby("Outlet_Identifier")["Item_Outlet_Sales"]
      .sum()
      .sort_values(ascending=False)
      .to_string()
)

fat_sales = (
    df.groupby("Item_Fat_Content")["Item_Outlet_Sales"]
      .sum()
      .to_string()
)

location_sales = (
    df.groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
      .sum()
      .to_string()
)

size_sales = (
    df.groupby("Outlet_Size")["Item_Outlet_Sales"]
      .sum()
      .to_string()
)

# -----------------------------
# HEADER
# -----------------------------
left, right = st.columns([6,1])

with left:
    st.title("🤖 BlinkIQ Copilot")
    st.caption(
    "Retail Intelligence Assistant • Powered by Groq Llama 3.3 70B"
)
with right:
    if st.button("🗑 Clear Chat", key="clear_chat_btn"):

        st.session_state.messages = []

        st.rerun()

st.markdown(
    "Ask questions about your retail dataset and receive AI-powered business insights."
)

# -----------------------------
# TABS
# -----------------------------

tab1, tab2 = st.tabs(
    [
        "💬 AI Assistant",
        "📈 Sales Prediction"
    ]
)
# -----------------------------
# AI ASSISTANT
# -----------------------------
with tab1:

    st.subheader("💬 Ask BlinkIQ AI")

    st.info(
        "You can ask questions such as:\n"
        "- Which outlet performs the best?\n"
        "- Give business recommendations.\n"
        "- Summarize the dashboard.\n"
        "- Which category generates the highest sales?"
    )

    # Display previous conversation
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    question = st.chat_input(
        "Ask anything about your retail business..."
    )

    if question:

        # Show user message immediately
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        system_prompt = f"""
You are BlinkIQ Copilot.

You are a Senior Retail Business Analyst.

Never say you are ChatGPT.

Never mention LLMs or AI models.

Only answer using the retail information provided.

If the user asks for recommendations,
provide practical retail suggestions.

If data is unavailable,
politely mention it instead of inventing facts.

====================

Business Overview

Total Revenue:
${total_revenue:,.2f}

Average Sales:
${average_sales:,.2f}

Average Product MRP:
${average_mrp:.2f}

Products:
{total_products}

Outlets:
{total_outlets}

Highest Performing Outlet:
{top_outlet}
Revenue:
${top_outlet_sales:,.2f}

Lowest Performing Outlet:
{lowest_outlet}
Revenue:
${lowest_outlet_sales:,.2f}

Best Category:
{best_category}

Outlet Sales

{outlet_sales}

Category Sales

{category_sales}

Fat Content Sales

{fat_sales}

Outlet Size Sales

{size_sales}

Outlet Location Sales

{location_sales}

====================

User Question:

{question}
"""

        with st.chat_message("assistant"):

            with st.spinner("🧠 Thinking like a Retail Analyst..."):

                response = client.chat.completions.create(

                    model="llama-3.3-70b-versatile",

                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        }
                    ]
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
# ----------------------------------------
# DATASET OVERVIEW
# ----------------------------------------

st.markdown("---")

st.subheader("📊 Dataset Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "💰 Revenue",
        f"${total_revenue:,.0f}"
    )

with k2:
    st.metric(
        "🏪 Outlets",
        total_outlets
    )

with k3:
    st.metric(
        "📦 Products",
        total_products
    )

with k4:
    st.metric(
        "💲 Avg MRP",
        f"${average_mrp:.2f}"
    )

# ----------------------------------------
# DOWNLOAD CHAT
# ----------------------------------------

if len(st.session_state.messages) > 0:

    history = ""

    for msg in st.session_state.messages:

        history += (
            f"{msg['role'].upper()}:\n"
            f"{msg['content']}\n\n"
        )

    st.download_button(
        "📥 Download Chat",
        history,
        file_name="BlinkIQ_AI_Conversation.txt",
        mime="text/plain"
    )

# ----------------------------------------
# SALES PREDICTION
# ----------------------------------------

with tab2:

    st.subheader("📈 AI Sales Prediction")

    st.info(
        "🚀 This module predicts expected sales based on product attributes.\n\n"
        "Currently this is Version 1.\n"
        "Future versions can integrate Machine Learning models "
        "such as XGBoost, Random Forest, or LightGBM."
    )

    c1, c2 = st.columns(2)

    with c1:

        outlet = st.selectbox(
            "Outlet",
            sorted(df["Outlet_Identifier"].unique())
        )

        category = st.selectbox(
            "Category",
            sorted(df["Item_Type"].unique())
        )

        fat = st.selectbox(
            "Fat Content",
            sorted(df["Item_Fat_Content"].unique())
        )

    with c2:

        mrp = st.number_input(
            "Product MRP",
            min_value=0.0,
            value=100.0
        )

        visibility = st.slider(
            "Visibility",
            0.0,
            0.35,
            0.08
        )

    if st.button("🔮 Predict Sales"):

        outlet_avg = df[
            df["Outlet_Identifier"] == outlet
        ]["Item_Outlet_Sales"].mean()

        category_avg = df[
            df["Item_Type"] == category
        ]["Item_Outlet_Sales"].mean()

        prediction = (
            outlet_avg * 0.55 +
            category_avg * 0.35 +
            mrp * 0.10
        )

        st.success(
            f"Estimated Sales: ${prediction:,.2f}"
        )

        st.progress(
            min(
                prediction / 5000,
                1.0
            )
        )

        st.caption(
            "This prediction is generated using historical business averages."
        )

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;color:#94a3b8;'>

<b>BlinkIQ Copilot</b><br>

Retail Intelligence Assistant

Powered by Groq • Llama 3.3 70B

Major Internship Project • 2026

</div>
""",
unsafe_allow_html=True
)