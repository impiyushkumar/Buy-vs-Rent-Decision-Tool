import streamlit as st
import plotly.express as px
from calculations import build_wealth_table

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Buy vs Rent Calculator",
    layout="wide"
)

# ---------------- Title ----------------
st.title("🏠 Buy vs Rent – Financial Decision Tool")

# ---------------- Sidebar Inputs ----------------
st.sidebar.header("Enter Details")

property_price = st.sidebar.number_input(
    "Property Price (₹)", min_value=0, value=5000000, step=100000
)
down_payment = st.sidebar.number_input(
    "Down Payment (₹)", min_value=0, value=1000000, step=50000
)
loan_rate = st.sidebar.slider(
    "Home Loan Interest (%)", 5.0, 15.0, 8.5
)
tenure = st.sidebar.slider(
    "Loan Tenure (years)", 10, 30, 20
)

rent = st.sidebar.number_input(
    "Monthly Rent (₹)", min_value=0, value=20000, step=1000
)
rent_growth = st.sidebar.slider(
    "Annual Rent Increase (%)", 0.0, 10.0, 5.0
)

sip_return = st.sidebar.slider(
    "SIP Return (%)", 5.0, 15.0, 10.0
)
property_growth = st.sidebar.slider(
    "Property Appreciation (%)", 0.0, 10.0, 6.0
)

# ---------------- Core Calculation ----------------
df, summary = build_wealth_table(
    property_price,
    down_payment,
    loan_rate,
    tenure,
    rent,
    rent_growth,
    sip_return,
    property_growth
)

# ---------------- Summary Section ----------------
st.subheader("📌 Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Monthly EMI", f"₹{int(summary['emi']):,}")
col2.metric("Total EMI Paid", f"₹{int(summary['total_emi_paid']):,}")
col3.metric("Total Rent Paid", f"₹{int(summary['total_rent_paid']):,}")

st.divider()

# ---------------- Graph ----------------
st.subheader("📈 Net Worth Comparison Over Time")

fig = px.line(
    df,
    x="Year",
    y=["Rent Net Worth (₹)", "Buy Net Worth (₹)"],
    labels={
        "value": "Net Worth (₹)",
        "variable": "Scenario"
    }
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Table ----------------
st.subheader("📊 Year-wise Wealth Table")
st.dataframe(df, use_container_width=True)

# ---------------- Final Verdict ----------------
st.subheader("✅ Final Verdict")

rent_final = summary["final_rent_net_worth"]
buy_final = summary["final_buy_net_worth"]

if rent_final > buy_final:
    st.success(
        f"🏠 Renting + SIP is better by ₹{int(rent_final - buy_final):,}"
    )
else:
    st.success(
        f"🏡 Buying a home is better by ₹{int(buy_final - rent_final):,}"
    )

if summary["break_even_year"]:
    st.info(f"📈 Break-even occurs in Year {summary['break_even_year']}")
else:
    st.info("📉 No break-even within the selected duration")
