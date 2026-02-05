import streamlit as st
import numpy as np
import time

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="VC Training Lab", layout="wide")

# --- 2. THE SECRET TRUTH & NARRATIVE MAP ---
B_VALUES = {
    "Type 1: The Basics": 0.5,
    "Type 2: Tech Apps": 2.0,
    "Type 3: Big Science": 8.0
}

MARKET_STORIES = {
    "Market A: The Boom": "Consumer spending is at an all-time high and credit is nearly free. In this 'Goldilocks' economy, almost any well-run business can find a customer.",
    "Market B: The Squeeze": "Inflation is rampant and store shelves are empty. The 'Stagflation' environment is punishing for companies with high overhead and thin margins.",
    "Market C: Rule Change": "The regulatory landscape has shifted. New government mandates have created massive tailwinds for specific sectors while suddenly bankrupting others."
}

TYPE_STORIES = {
    "Type 1: The Basics": "This fund focuses on 'Utility' plays: water pipes, power lines, and essential infrastructure. Low growth, but steady demand.",
    "Type 2: Tech Apps": "This fund focuses on scalable digital platforms: social media, gaming, and delivery. High competition, but explosive upside.",
    "Type 3: Big Science": "This fund focuses on frontier technology: rocket engines, deep-sea mining, and experimental AI. High failure rate, but world-changing payouts."
}

BASE_P_MATRIX = {
    "Market A: The Boom": {"Type 1: The Basics": 0.90, "Type 2: Tech Apps": 0.60, "Type 3: Big Science": 0.25},
    "Market B: The Squeeze": {"Type 1: The Basics": 0.70, "Type 2: Tech Apps": 0.35, "Type 3: Big Science": 0.08},
    "Market C: Rule Change": {"Type 1: The Basics": 0.80, "Type 2: Tech Apps": 0.45, "Type 3: Big Science": 0.15},
}

# --- 3. SESSION STATE INITIALIZATION ---
if "lab_id" not in st.session_state:
    st.session_state.lab_id = ""
if "p_matrix" not in st.session_state:
    st.session_state.p_matrix = {}
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = None
if "audit_report" not in st.session_state:
    st.session_state.audit_report = None
if "audit_verified" not in st.session_state:
    st.session_state.audit_verified = False
if "stress_test_history" not in st.session_state:
    st.session_state.stress_test_history = []

# --- 4. HELPER FUNCTIONS ---
def initialize_student_matrix(lab_id):
    seed = sum(ord(char) for char in lab_id)
    np.random.seed(seed)
    new_matrix = {}
    for market, types in BASE_P_MATRIX.items():
        new_matrix[market] = {}
        for fund_type, base_p in types.items():
            noise = np.random.normal(0, 0.02)
            new_matrix[market][fund_type] = np.clip(base_p + noise, 0.01, 0.99)
    return new_matrix

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("👨‍💼 VC Research Desk")
    id_input = st.text_input("Enter Lab ID to Initialize:", value=st.session_state.lab_id)
    
    if id_input != st.session_state.lab_id:
        st.session_state.lab_id = id_input
        if id_input:
            st.session_state.p_matrix = initialize_student_matrix(id_input)
            st.session_state.audit_report = None
            st.session_state.audit_verified = False
            st.session_state.stress_test_history = []
            st.success(f"Lab Initialized: {id_input}")

    if st.session_state.lab_id:
        st.divider()
        market_choice = st.selectbox("Market Environment", list(BASE_P_MATRIX.keys()))
        type_choice = st.selectbox("Fund Type", list(B_VALUES.keys()))
        
        if st.button("Open Research Lab"):
            st.session_state.current_scenario = (market_choice, type_choice)
            st.session_state.audit_report = None
            st.session_state.audit_verified = False
            st.session_state.stress_test_history = []

# --- 6. MAIN INTERFACE ---
st.title("Venture Capital Lab")

if not st.session_state.lab_id:
    st.warning("⚠️ Access Denied: Please enter your **Lab ID** in the sidebar to begin.")
elif not st.session_state.current_scenario:
    st.info("Select a Market and Fund Type in the sidebar to open the Research Lab.")
else:
    market, fund_type = st.session_state.current_scenario
    student_p = st.session_state.p_matrix[market][fund_type]
    b = B_VALUES[fund_type]
    
    with st.expander("📄 Intelligence Briefing: Sector & Market Analysis", expanded=True):
        col_m, col_t = st.columns(2)
        with col_m:
            st.write(f"**Current Market Conditions:**\n\n*{MARKET_STORIES[market]}*")
        with col_t:
            st.write(f"**Investment Sector:**\n\n*{TYPE_STORIES[fund_type]}*")
        st.markdown(f"**Payout Terms:** Successful exits are contractually bound to yield a **{b}x profit multiple** on capital deployed.")
    
    tab1, tab2, tab3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with tab1:
        st.subheader("Stage 1: Forensic Probability Discovery")
        if st.button("Request Internal Audit Report"):
            scenario_seed = sum(ord(char) for char in st.session_state.lab_id + market + fund_type)
            np.random.seed(scenario_seed)
            outcomes = ["SUCCESS" if np.random.random() < student_p else "FAILURE" for _ in range(50)]
            wins = outcomes.count("SUCCESS")
            
            st.session_state.audit_report = {
                "wins": wins,
                "execution_fail": int((50-wins)*0.4),
                "macro_fail": (50-wins) - int((50-wins)*0.4),
                "total": 50,
                "p": wins/50
            }
            st.session_state.audit_verified = False

        if st.session_state.audit_report:
            r = st.session_state.audit_report
            st.info("### 🕵️ INTERNAL MEMO: Sector Performance Review")
            st.markdown(f"""
            **To:** Managing Partner | **From:** Forensic Risk Division | **Subject:** Outcome Audit for 50 Sample Ventures  

            Our team has completed a deep-dive investigation into the last 50 ventures launched within this sector. The goal was to separate viable business models from those that succumbed to pressures.

            **The Audit reveals the following findings:**
            * **Execution Failures:** We identified that **{r['execution_fail']} companies** suffered from fatal internal mismanagement and inability to scale. 
            * **Market Casualties:** An additional **{r['macro_fail']} ventures** were liquidated following unexpected shifts in the competitive landscape.
            * **Successful Exits:** The remaining companies in the sample successfully hit their target exit milestones.

            Please use these findings to calibrate our success probability ($p$).
            """)
            st.divider()
            user_p = st.number_input("Based on the Memo, what is the Win Probability ($p$)?", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
            if st.button("Verify Findings"):
                if abs(user_p - r['p']) < 0.001:
                    st.session_state.audit_verified = True
                    st.success(f"Audit Verified. Fundamental Probability established at {r['p']:.2f}.")
                else:
                    st.error("Audit Discrepancy detected. Please re-examine the report figures.")

    with tab2:
        st.subheader("Stage 2: Volatility Stress Test")
        if not st.session_state.audit_verified:
            st.info("🔒 Research Locked: You must verify the Forensic Audit in Stage 1.")
        else:
            st.write(f"Fundamental Probability: **{st.session_state.audit_report['p']:.2f}**")
            if st.button("Simulate 100-Deal Career Cycle"):
                career = ["SUCCESS" if np.random.random() < st.session_state.audit_report['p'] else "FAILURE" for _ in range(100)]
                streak = 0
                max_streak = 0
                for x in career:
                    if x == "FAILURE":
                        streak += 1
                        max_streak = max(max_streak, streak)
                    else:
                        streak = 0
                
                trial_data = {"wins": career.count("SUCCESS"), "streak": max_streak, "outcomes": career}
                st.session_state.stress_test_history.append(trial_data)

            if st.session_state.stress_test_history:
                latest = st.session_state.stress_test_history[-1]
                c1, c2 = st.columns(2)
                c1.metric("Wins in Latest Career", f"{latest['wins']}/100")
                c2.metric("Longest Losing Streak", f"{latest['streak']} in a row")
                
                st.write("**Career Ticker (Latest Run):**")
                icons = ["🟩" if r == "SUCCESS" else "🟥" for r in latest['outcomes']]
                for i in range(0, 100, 20):
                    st.write(" ".join(icons[i:i+20]))
                
                if len(st.session_state.stress_test_history) > 1:
                    st.divider()
                    st.write("### 📊 Career Comparison Log")
                    history_df = [{"Career #": i+1, "Wins": h['wins'], "Max Loss Streak": h['streak']} for i, h in enumerate(st.session_state.stress_test_history)]
                    st.table(history_df)

    with tab3:
        st.subheader("Stage 3: Capital Calibration")
        if not st.session_state.stress_test_history:
            st.info("🔒 Research Locked: Run a Stage 2 Stress Test to unlock Calibration.")
        else:
            st.markdown("Choose your investment fraction (**$f$**) and simulate a final 50-round deployment.")
            f = st.slider("Investment Size (f): % of
