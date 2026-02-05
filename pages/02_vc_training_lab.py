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
if "stress_test_results" not in st.session_state:
    st.session_state.stress_test_results = None

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
            st.session_state.stress_test_results = None
            st.success(f"Lab Initialized: {id_input}")

    if st.session_state.lab_id:
        st.divider()
        market_choice = st.selectbox("Market Environment", list(BASE_P_MATRIX.keys()))
        type_choice = st.selectbox("Fund Type", list(B_VALUES.keys()))
        
        if st.button("Open Research Lab"):
            st.session_state.current_scenario = (market_choice, type_choice)
            st.session_state.audit_report = None
            st.session_state.audit_verified = False
            st.session_state.stress_test_results = None

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
            st.write(f"**Market:** {market}\n\n*{MARKET_STORIES[market]}*")
        with col_t:
            st.write(f"**Sector:** {fund_type}\n\n*{TYPE_STORIES[fund_type]}*")
        st.write(f"**Payout Multiplier:** Successful investments yield a **{b}x** profit multiple.")
    
    tab1, tab2, tab3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with tab1:
        st.subheader("Stage 1: Probability Discovery")
        if st.button("Generate Audit Report"):
            scenario_seed = sum(ord(char) for char in st.session_state.lab_id + market + fund_type)
            np.random.seed(scenario_seed)
            outcomes = ["SUCCESS" if np.random.random() < student_p else "FAILURE" for _ in range(50)]
            wins = outcomes.count("SUCCESS")
            st.session_state.audit_report = {"wins": wins, "fail_a": int((50-wins)*0.6), "fail_b": (50-wins)-int((50-wins)*0.6), "total": 50, "p": wins/50}
            st.session_state.audit_verified = False

        if st.session_state.audit_report:
            report = st.session_state.audit_report
            st.info(f"### 🕵️ INTERNAL AUDIT MEMO\n\nOut of {report['total']} cases, **{report['fail_a']}** failed due to execution and **{report['fail_b']}** failed due to competition. The rest succeeded.")
            user_p = st.number_input("What is the Win Probability (p)?", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
            if st.button("Verify Findings"):
                if abs(user_p - report['p']) < 0.001:
                    st.session_state.audit_verified = True
                    st.success(f"Correct. p = {report['p']:.2f}")
                else:
                    st.error("Incorrect calculation.")

    with tab2:
        st.subheader("Stage 2: Volatility Stress Test")
        if not st.session_state.audit_verified:
            st.info("🔒 Complete and Verify the Stage 1 Audit to unlock.")
        else:
            st.markdown(f"**Target Probability:** $p = {st.session_state.audit_report['p']:.2f}$")
            st.write("Even with a known success rate, luck arrives in clusters. Running 100 trials to simulate a full career cycle...")
            
            if st.button("Simulate 100-Trial Career"):
                # Use a different seed from Audit to ensure new randomness
                career_seed = sum(ord(char) for char in st.session_state.lab_id + market + fund_type) + 999
                np.random.seed(career_seed)
                career_outcomes = ["SUCCESS" if np.random.random() < st.session_state.audit_report['p'] else "FAILURE" for _ in range(100)]
                
                # Calculate streaks
                max_loss_streak = 0
                current_streak = 0
                for res in career_outcomes:
                    if res == "FAILURE":
                        current_streak += 1
                        max_loss_streak = max(max_loss_streak, current_streak)
                    else:
                        current_streak = 0
                
                st.session_state.stress_test_results = {
                    "outcomes": career_outcomes,
                    "max_loss_streak": max_loss_streak,
                    "win_count": career_outcomes.count("SUCCESS")
                }

            if st.session_state.stress_test_results:
                res = st.session_state.stress_test_results
                
                col1, col2 = st.columns(2)
                col1.metric("Actual Wins", f"{res['win_count']}/100")
                col2.metric("Longest Losing Streak", f"{res['max_loss_streak']} in a row", delta="High Risk!" if res['max_loss_streak'] > 4 else None, delta_color="inverse")
                
                st.write("**Visual Career Path (100 Trials):**")
                icons = ["🟩" if r == "SUCCESS" else "🟥" for r in res['outcomes']]
                # Grid display
                for i in range(0, 100, 20):
                    st.write(" ".join(icons[i:i+20]))
                
                st.warning(f"**The Sizing Lesson:** If you had invested 25% of your fund in every deal, a losing streak of **{res['max_loss_streak']}** would have likely wiped you out completely. Think about this when you reach Stage 3.")

    with tab3:
        st.subheader("Stage 3: Calibration")
        if st.session_state.stress_test_results is None:
            st.info("🔒 Complete the Stage 2 Stress Test to unlock.")
        else:
            st.write("Use the slider to find an investment size ($f$) that maximizes your fund.")

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
