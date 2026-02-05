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
    "Market A: The Boom": "Consumer spending is at an all-time high and credit is nearly free. Everything feels easy.",
    "Market B: The Squeeze": "Prices are spiking and store shelves are empty. Companies are burning through cash fast.",
    "Market C: Rule Change": "The government just passed a massive law shifting funding toward specific sectors."
}

TYPE_STORIES = {
    "Type 1: The Basics": "This fund focuses on 'Utility' plays: water pipes, power lines, and essential infrastructure.",
    "Type 2: Tech Apps": "This fund focuses on scalable platforms: social media, delivery apps, and online gaming.",
    "Type 3: Big Science": "This fund focuses on frontier tech: new medicines, rocket engines, and experimental AI."
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
    st.info("Select a scenario in the sidebar to begin.")
else:
    market, fund_type = st.session_state.current_scenario
    student_p = st.session_state.p_matrix[market][fund_type]
    b = B_VALUES[fund_type]
    
    with st.expander("📄 Intelligence Briefing", expanded=True):
        col_m, col_t = st.columns(2)
        with col_m:
            st.write(f"**Market Dynamics:**\n\n*{MARKET_STORIES[market]}*")
        with col_t:
            st.write(f"**Sector Profile:**\n\n*{TYPE_STORIES[fund_type]}*")
        st.write(f"**Contractual Terms:** Successful exits are legally bound to a **{b}x** payout on capital deployed.")
    
    tab1, tab2, tab3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with tab1:
        st.subheader("Stage 1: Forensic Audit Analysis")
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
            st.markdown(f"""
            ### 🕵️ Confidential Memo: Sector Performance Review
            **To:** Managing Partner | **From:** Risk Assessment Division
            
            Our investigation into the last 50 ventures shows that **{r['execution_fail']} companies** failed due to execution and **{r['macro_fail']} ventures** failed due to competitive shifts. 
            The remaining ventures successfully hit their target exit milestones.
            """)
            st.divider()
            user_p = st.number_input("Based on the memo, what is the Win Probability ($p$)?", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
            if st.button("Verify Audit Findings"):
                if abs(user_p - r['p']) < 0.001:
                    st.session_state.audit_verified = True
                    st.success(f"Audit Verified. Fundamental Probability established at {r['p']:.2f}.")
                else:
                    st.error("Audit Discrepancy detected.")

    with tab2:
        st.subheader("Stage 2: Volatility Stress Test")
        if not st.session_state.audit_verified:
            st.info("🔒 Research Locked: Verify Stage 1 Audit to unlock.")
        else:
            st.write(f"Current Probability: **{st.session_state.audit_report['p']:.2f}**. Click below to see how different careers play out under these same odds.")
            
            if st.button("Generate New 100-Trial Career"):
                # No fixed seed here, allows "sampling distribution" feel
                career = ["SUCCESS" if np.random.random() < st.session_state.audit_report['p'] else "FAILURE" for _ in range(100)]
                
                streak = 0
                max_streak = 0
                for x in career:
                    if x == "FAILURE":
                        streak += 1
                        max_streak = max(max_streak, streak)
                    else:
                        streak = 0
                
                # Save to history
                trial_data = {"wins": career.count("SUCCESS"), "streak": max_streak, "outcomes": career}
                st.session_state.stress_test_history.append(trial_data)

            if st.session_state.stress_test_history:
                latest = st.session_state.stress_test_history[-1]
                
                c1, c2 = st.columns(2)
                c1.metric("Latest Career Wins", f"{latest['wins']}/100")
                c2.metric("Latest Max Losing Streak", f"{latest['streak']} Deals")
                
                st.write("**Latest Simulated Ticker:**")
                icons = ["🟩" if r == "SUCCESS" else "🟥" for r in latest['outcomes']]
                for i in range(0, 100, 20):
                    st.write(" ".join(icons[i:i+20]))
                
                if len(st.session_state.stress_test_history) > 1:
                    st.divider()
                    st.write("### 📊 Historical Comparison of Careers")
                    st.write("Notice how the 'Longest Streak' varies even though the win probability is the same.")
                    history_df = [{"Career #": i+1, "Wins": h['wins'], "Max Loss Streak": h['streak']} for i, h in enumerate(st.session_state.stress_test_history)]
                    st.table(history_df)

    with tab3:
        st.subheader("Stage 3: Capital Calibration")
        if not st.session_state.stress_test_history:
            st.info("🔒 Research Locked: Run at least one Stress Test in Stage 2 to unlock.")
        else:
            st.markdown("Choose your investment fraction (**$f$**) and simulate a final 50-round career.")
            f = st.slider("Investment Size ($f$): % of fund per deal", 0, 100, 10) / 100
            
            if st.button("Execute 50-Round Career"):
                balance = 1000.0
                history = [balance]
                ruined = False
                
                for _ in range(50):
                    if balance < 1.0:
                        ruined = True
                        balance = 0
                        history.append(balance)
                        continue
                    
                    bet = balance * f
                    if np.random.random() < st.session_state.audit_report['p']:
                        balance += (bet * b)
                    else:
                        balance -= bet
                    history.append(balance)
                
                st.write(f"### Final Fund Balance: **${balance:,.2f}**")
                if ruined: st.error("🚨 FUND INSOLVENT")
                elif balance > 1000: st.success(f"Growth achieved! Profit: ${balance-1000:,.2f}")
                else: st.warning("Net Loss.")
                st.line_chart(history)

# --- PADDING TO PREVENT TRUNCATION ---
# 
# 
# 
# 
# 
# 
# 
# 
# --- END OF FILE ---
