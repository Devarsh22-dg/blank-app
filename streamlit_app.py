import streamlit as st
from math import pow
from datetime import datetime

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Retirement Planning Agent", page_icon="💰")
st.title("💰 Simple Retirement Planning Agent")
st.write("This is a simple educational tool — not financial advice.")

# -----------------------------
# Helper Functions
# -----------------------------
def recommend_account(employment, has_401k, income):
    if employment == "Employed" and has_401k:
        return "401(k) — contribute at least enough to get your employer match. Consider a Roth IRA for tax-free withdrawals."
    if employment == "Self-Employed":
        return "SEP IRA or Solo 401(k) — great for business owners."
    if income is None or income < 145000:
        return "Roth IRA (if eligible). If not, consider Traditional IRA or brokerage."
    return "Traditional IRA or taxable brokerage account."

def recommend_allocation(age, risk):
    if age < 30:
        base_stock = 90
    elif age < 40:
        base_stock = 85
    elif age < 50:
        base_stock = 75
    elif age < 60:
        base_stock = 65
    else:
        base_stock = 50
    if risk == "High":
        stock = min(95, base_stock + 10)
    elif risk == "Low":
        stock = max(30, base_stock - 20)
    else:
        stock = base_stock
    bond = 100 - stock
    return stock, bond

def contribution_guidance(income):
    if income is None:
        return "Try to save 10–15% of your income. If unsure, start with what you can and increase over time."
    monthly_10 = round((income * 0.10) / 12)
    monthly_15 = round((income * 0.15) / 12)
    return f"Goal: 10–15% of income → about ${monthly_10}/mo to ${monthly_15}/mo"

def explain_risk(risk):
    if risk == "Low":
        return "Low risk: more bonds. Smaller swings, slower growth."
    if risk == "High":
        return "High risk: more stocks. Bigger swings, higher growth potential."
    return "Medium risk: balance of stocks and bonds."

def project_savings(current_savings, monthly_contribution, years, annual_return):
    r = annual_return / 100 / 12
    months = years * 12
    fv = current_savings * pow(1 + r, months)
    for m in range(1, months + 1):
        fv += monthly_contribution * pow(1 + r, months - m + 1)
    return fv

# -----------------------------
# User Inputs
# -----------------------------
st.header("👤 Personal Information")
age = st.number_input("Current Age", min_value=18, max_value=100, value=30)
retire_age = st.number_input("Target Retirement Age", min_value=age+1, max_value=100, value=65)
employment = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Not Working"])
income = st.number_input("Annual Income ($)", min_value=0, value=80000, step=1000) or None
has_401k = False
if employment == "Employed":
    has_401k = st.radio("Do you have access to a 401(k)?", ["Yes", "No"]) == "Yes"
risk = st.radio("Risk Comfort Level", ["Low", "Medium", "High"])

# -----------------------------
# Generate Retirement Plan
# -----------------------------
if st.button("Generate Retirement Plan"):
    acct = recommend_account(employment, has_401k, income)
    stock, bond = recommend_allocation(age, risk)
    contrib = contribution_guidance(income)
    risk_text = explain_risk(risk)

    st.subheader("📋 Your Retirement Plan")
    st.write(f"**Account Recommendation:** {acct}")
    st.write(f"**Suggested Investment Allocation:** {stock}% Stocks / {bond}% Bonds")
    st.write(f"**Contribution Guidance:** {contrib}")
    st.write(f"**Risk Explanation:** {risk_text}")

    st.info("💡 Consider using a Target Date Fund or a simple 3-fund mix (US Stock, Intl Stock, Bond).")

# -----------------------------
# Savings Calculator
# -----------------------------
st.header("🧮 Retirement Savings Calculator")

current_savings = st.number_input("Current Retirement Savings ($)", min_value=0.0, value=10000.0)
monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0.0, value=500.0)
expected_return = st.slider("Expected Annual Return (%)", 0.0, 15.0, 6.0)
goal = st.number_input("Retirement Savings Goal ($)", min_value=0.0, value=1000000.0)

if st.button("Calculate Savings Projection"):
    years = retire_age - age
    if years <= 0:
        st.error("⚠️ Retirement age must be greater than current age.")
    else:
        projected = project_savings(current_savings, monthly_contribution, years, expected_return)
        st.subheader(f"📊 Projected Savings at Age {retire_age}: ${projected:,.2f}")

        if projected < goal:
            shortfall = goal - projected
            st.error(f"⚠️ Shortfall: You’re projected to fall short by ${shortfall:,.2f}")
            # Calculate how much more to save monthly
            r = expected_return / 100 / 12
            months = years * 12
            future_factor = sum(pow(1 + r, months - m + 1) for m in range(1, months + 1))
            needed_extra = shortfall / future_factor
            st.info(f"💡 To hit your goal, save about **${needed_extra:,.2f} more per month.**")
        else:
            st.success("✅ You’re on track to meet or exceed your goal!")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("⚠️ This tool is for educational purposes only and not financial advice.")

