import streamlit as st


def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------- Reusable KPI Card ----------

def kpi_card(icon, title, value, subtitle=""):
    st.markdown(
        f"""
        <div style="
            background:#1f2937;
            padding:22px;
            border-radius:18px;
            border:1px solid #374151;
            box-shadow:0 8px 20px rgba(0,0,0,0.25);
            min-height:180px;
        ">

            <div style="font-size:18px;font-weight:600;color:#9ca3af;">
                {icon} {title}
            </div>

            <div style="
                margin-top:30px;
                font-size:40px;
                font-weight:700;
                color:white;
                line-height:1.1;
            ">
                {value}
            </div>

            <div style="
                margin-top:10px;
                font-size:15px;
                color:#9ca3af;
            ">
                {subtitle}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )