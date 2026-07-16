# BlinkIQ
### AI-Powered Retail Intelligence Platform

BlinkIQ is an AI-powered retail analytics platform developed using Python, Streamlit, and Plotly to transform retail sales data into meaningful business insights through interactive dashboards, visual analytics, and intelligent recommendations.

This project was developed as part of a **Major Internship Project**.

## Project Overview

Retail businesses generate large amounts of sales data every day. BlinkIQ helps analyze this data through an interactive web application that enables users to monitor sales performance, evaluate operational metrics, identify trends, and receive data-driven business recommendations.

The application combines data analytics, business intelligence, and visualization techniques to support smarter retail decision-making.

## Features

- Modern SaaS-inspired dashboard interface
- Interactive sales analytics dashboard
- Business performance analysis
- AI-based recommendation system
- Revenue and outlet performance monitoring
- Product category insights
- Dynamic KPI cards
- Interactive Plotly visualizations
- Responsive Streamlit web application
- Integrated Power BI dashboard for advanced reporting

## Technology Stack

### Programming Language
- Python

### Libraries
- Streamlit
- Pandas
- NumPy
- Plotly
- Pillow

### Tools
- VS Code
- Jupyter Notebook
- Power BI
- Git
- GitHub

## Project Structure

```text
BlinkIQ_Streamlit/
│
├── Home.py
├── style.css
├── utils.py
│
├── assets/
│   └── hero.png
│
├── data/
│   └── blinkit_cleaned.csv
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Sales_Insights.py
│   ├── 3_Business_Analytics.py
│   └── 4_Recommendations.py
│
├── notebooks/
│
├── power bi/
│   ├── BlinkIQ_Dashboard.pbix
│   └── BlinkIQ_Dashboard.pdf
│
├── sql/
│
├── requirements.txt
└── README.md
```
## Dashboard Modules

### Home
Provides an overview of the platform with key business metrics, project highlights, and navigation.

### Dashboard
Displays retail KPIs including revenue, products, outlets, and sales performance.

### Sales Insights
Analyzes sales trends, outlet performance, product categories, and revenue distribution.

### Business Analytics
Visualizes operational metrics using interactive charts for business decision-making.

### AI Recommendations
Generates actionable business recommendations based on sales patterns and retail insights.

### Power BI Dashboard
Includes an advanced Business Intelligence dashboard for additional visualization and reporting.

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory

```bash
cd BlinkIQ_Streamlit
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run home.py
```

## Author

**Kavya shree Bali**

Major Internship Project

Department of Computer Science & Engineering (AI & ML)

2026

---

## License

This project is developed for educational and internship purposes.
