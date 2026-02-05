import streamlit as st
import numpy as np

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
            st.success(f"Lab Initialized: {id_input}")

    if st.session_state.lab_id:
        st.divider()
        market_choice = st.selectbox("Market Environment", list(BASE_P_MATRIX.keys()))
        type_choice = st.selectbox("Fund Type", list(B_VALUES.keys()))
        
        if st.button("Open Research Lab"):
            st.session_state.current_scenario = (market_choice, type_choice)
            st.session_state.audit_report = None
            st.session_state.audit_verified = False

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
    
    with st.expander("📄 Intelligence Briefing: Sector & Market Analysis", expanded=True):
        col_m, col_t = st.columns(2)
        with col_m:
            st.write(f"**Current Market Conditions:**\n\n*{MARKET_STORIES[market]}*")
        with col_t:
            st.write(f"**Investment Sector:**\n\n*{TYPE_STORIES[fund_type]}*")
        st.write(f"**Payout Multiplier:** Successful investments yield a **{b}x** profit multiple.")
    
    tab1, tab2, tab3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with tab1:
        st.subheader("Stage 1: Probability Discovery")
        st.markdown("Your analyst team has completed a forensic audit of the last **50 ventures** in this specific sector.")
        
        if st.button("Generate Audit Report"):
            scenario_seed = sum(ord(char) for char in st.session_state.lab_id + market + fund_type)
            np.random.seed(scenario_seed)
            outcomes = ["SUCCESS" if np.random.random() < student_p else "FAILURE" for _ in range(50)]
            
            wins = outcomes.count("SUCCESS")
            # Divide failures into narrative categories
            fail_a = int((50 - wins) * 0.6)
            fail_b = (50 - wins) - fail_a
            
            st.session_state.audit_report = {
                "wins": wins,
                "fail_a": fail_a,
                "fail_b": fail_b,
                "total": 50,
                "p": wins / 50
            }
            st.session_state.audit_verified = False

        if st.session_state.audit_report:
            report = st.session_state.audit_report
            st.info("### 🕵️ INTERNAL AUDIT MEMO")
            st.write(f"""
            **Subject:** Sector Performance Review (N={report['total']})
            
            Our investigation into the 50 most recent ventures in this category reveals a complex landscape. 
            Of the total cases reviewed, **{report['fail_a']} companies** were found to have collapsed due to poor management 
            or execution errors. Another **{report['fail_b']} companies** were liquidated following unexpected 
            shifts in the competitive landscape. 
            
            The remaining companies in our study achieved their target exit milestones and are considered successful.
            """)
            st.write("---")
            
            user_p = st.number_input("Based on this internal memo, what is the Win Probability ($p$)?", 
                                    min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
            
            if st.button("Verify Findings"):
                if abs(user_p - report['p']) < 0.001:
                    st.session_state.audit_verified = True
                    st.success(f"Correct. Research phase complete. $p = {report['p']:.2f}$")
                else:
                    st.error("Your probability calculation does not match the audit data. Check your math: (Total - Failures) / Total.")

    with tab2:
        st.subheader("Stage 2: Volatility Stress Test")
        if not st.session_state.audit_verified:
            st.info("🔒 Complete and Verify the Stage 1 Audit to unlock.")
        else:
            st.write(f"With $p = {st.session_state.audit_report['p']:.2f}$, watch how luck clusters over 100 trials.")
            # Ready for 100-flip logic

    with tab3:
        st.subheader("Stage 3: Calibration")
        if not st.session_state.audit_verified:
            st.info("🔒 Complete and Verify the Stage 1 Audit to unlock.")

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
