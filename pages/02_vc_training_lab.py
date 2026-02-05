import streamlit as st
import numpy as np
import time

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="VC Training Lab", layout="wide")

# --- 2. THE SECRET TRUTH & NARRATIVE MAP ---
B_VALUES = {"Type 1: The Basics": 0.5, "Type 2: Tech Apps": 2.0, "Type 3: Big Science": 8.0}

MARKET_STORIES = {
    "Market A: The Boom": "Consumer spending is at an all-time high and credit is nearly free. In this 'Goldilocks' economy, almost any well-run business can find a customer.",
    "Market B: The Squeeze": "Inflation is rampant and store shelves are empty. The 'Stagflation' environment is punishing for companies with high overhead and thin margins.",
    "Market C: Rule Change": "The regulatory landscape has shifted. New government mandates have created massive tailwinds for specific sectors while suddenly bankrupting others."
}

TYPE_STORIES = {
    "Type 1: The Basics": "This fund focuses on 'Utility' plays: infrastructure and essential services. Low growth, but steady demand.",
    "Type 2: Tech Apps": "This fund focuses on scalable digital platforms. High competition, but explosive upside.",
    "Type 3: Big Science": "This fund focuses on frontier technology like experimental AI and rockets. High failure rate, but world-changing payouts."
}

BASE_P_MATRIX = {
    "Market A: The Boom": {"Type 1: The Basics": 0.90, "Type 2: Tech Apps": 0.60, "Type 3: Big Science": 0.25},
    "Market B: The Squeeze": {"Type 1: The Basics": 0.70, "Type 2: Tech Apps": 0.35, "Type 3: Big Science": 0.08},
    "Market C: Rule Change": {"Type 1: The Basics": 0.80, "Type 2: Tech Apps": 0.45, "Type 3: Big Science": 0.15},
}

# --- 3. SESSION STATE INITIALIZATION ---
for key in ["lab_id", "p_matrix", "current_scenario", "audit_report", "audit_verified", "stress_test_history"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key == "lab_id" else [] if key == "stress_test_history" else None

# --- 4. HELPER FUNCTIONS ---
def initialize_student_matrix(lab_id):
    np.random.seed(sum(ord(char) for char in lab_id))
    new_matrix = {}
    for market, types in BASE_P_MATRIX.items():
        new_matrix[market] = {t: np.clip(p + np.random.normal(0, 0.02), 0.01, 0.99) for t, p in types.items()}
    return new_matrix

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("👨‍💼 VC Research Desk")
    id_input = st.text_input("Enter Lab ID:", value=st.session_state.lab_id)
    if id_input != st.session_state.lab_id:
        st.session_state.lab_id = id_input
        st.session_state.p_matrix = initialize_student_matrix(id_input)
        st.session_state.audit_report, st.session_state.audit_verified, st.session_state.stress_test_history = None, False, []

    if st.session_state.lab_id:
        st.divider()
        m_choice = st.selectbox("Market Environment", list(BASE_P_MATRIX.keys()))
        t_choice = st.selectbox("Fund Type", list(B_VALUES.keys()))
        if st.button("Open Research Lab"):
            st.session_state.current_scenario = (m_choice, t_choice)
            st.session_state.audit_report, st.session_state.audit_verified, st.session_state.stress_test_history = None, False, []

# --- 6. MAIN INTERFACE ---
if not st.session_state.lab_id:
    st.warning("⚠️ Access Denied: Please enter your Lab ID in the sidebar.")
elif not st.session_state.current_scenario:
    st.info("Select a Market and Fund Type in the sidebar to begin.")
else:
    market, fund_type = st.session_state.current_scenario
    student_p = st.session_state.p_matrix[market][fund_type]
    b = B_VALUES[fund_type]
    
    with st.expander("📄 Intelligence Briefing", expanded=True):
        st.write(f"**Market:** {MARKET_STORIES[market]}")
        st.write(f"**Sector:** {TYPE_STORIES[fund_type]}")
        st.write(f"**Payout Terms:** Successful exits yield a **{b}x** multiple.")

    tab1, tab2, tab3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with tab1:
        st.subheader("Stage 1: Forensic Audit Analysis")
        if st.button("Request Internal Audit Report"):
            np.random.seed(sum(ord(char) for char in st.session_state.lab_id + market + fund_type))
            wins = sum(1 for _ in range(50) if np.random.random() < student_p)
            st.session_state.audit_report = {"wins": wins, "ex_fail": int((50-wins)*0.4), "ma_fail": (50-wins)-int((50-wins)*0.4), "p": wins/50}
            st.session_state.audit_verified = False

        if st.session_state.audit_report:
            r = st.session_state.audit_report
            st.info(f"### 🕵️ MEMO: Sector Outcome Audit\n\nOur investigation of 50 sample ventures found **{r['ex_fail']} companies** failed due to mismanagement and **{r['ma_fail']} ventures** succumbed to market shifts. The remaining companies were successful.")
            user_p = st.number_input("Determine Win Probability (p):", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
            if st.button("Verify Findings"):
                if abs(user_p - r['p']) < 0.001:
                    st.session_state.audit_verified = True
                    st.success(f"Audit Verified. p = {r['p']:.2f}.")
                else: st.error("Verification failed.")

    with tab2:
        st.subheader("Stage 2: Volatility Stress Test")
        if not st.session_state.audit_verified: st.info("🔒 Verify Stage 1 to unlock.")
        else:
            if st.button("Simulate 100-Deal Career Cycle"):
                career = ["SUCCESS" if np.random.random() < st.session_state.audit_report['p'] else "FAILURE" for _ in range(100)]
                streak, max_s = 0, 0
                for x in career:
                    streak = streak + 1 if x == "FAILURE" else 0
                    max_s = max(max_s, streak)
                st.session_state.stress_test_history.append({"wins": career.count("SUCCESS"), "streak": max_s, "outcomes": career})

            if st.session_state.stress_test_history:
                latest = st.session_state.stress_test_history[-1]
                c1, c2 = st.columns(2)
                c1.metric("Latest Wins", f"{latest['wins']}/100")
                c2.metric("Max Loss Streak", f"{latest['streak']} Deals")
                st.write(" ".join(["🟩" if r == "SUCCESS" else "🟥" for r in latest['outcomes']]))
                if len(st.session_state.stress_test_history) > 1:
                    st.table([{"Career #": i+1, "Wins": h['wins'], "Streak": h['streak']} for i, h in enumerate(st.session_state.stress_test_history)])

    with tab3:
        st.subheader("Stage 3: Capital Calibration")
        if not st.session_state.stress_test_history: st.info("🔒 Complete Stage 2 to unlock.")
        else:
            f = st.slider("Investment Size (f): % of Fund per Deal", 0, 100, 10) / 100
            if st.button("Execute 50-Round Career"):
                bal, history, ruined = 1000.0, [1000.0], False
                for _ in range(50):
                    if bal < 1.0: ruined = True; bal = 0
                    else:
                        bet = bal * f
                        bal = bal + (bet * b) if np.random.random() < st.session_state.audit_report['p'] else bal - bet
                    history.append(bal)
                st.write(f"### Final Fund: ${bal:,.2f}")
                if ruined: st.error("🚨 FUND INSOLVENT")
                st.line_chart(history)

# --- PADDING ---
# 
# 
# 
# 
# 
# 
# 
# --- END OF FILE ---
