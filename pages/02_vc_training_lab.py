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

# Narrative descriptions for the header
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
if "audit_data" not in st.session_state:
    st.session_state.audit_data = None
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
            st.session_state.audit_data = None
            st.session_state.audit_verified = False
            st.success(f"Lab Initialized: {id_input}")

    if st.session_state.lab_id:
        st.divider()
        market_choice = st.selectbox("Market Environment", list(BASE_P_MATRIX.keys()))
        type_choice = st.selectbox("Fund Type", list(B_VALUES.keys()))
        
        if st.button("Open Research Lab"):
            st.session_state.current_scenario = (market_choice, type_choice)
            st.session_state.audit_data = None
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
    
    # (1) COMPREHENSIVE STORY HEADER
    with st.expander("📄 Intelligence Briefing: Sector & Market Analysis", expanded=True):
        col_m, col_t = st.columns(2)
        with col_m:
            st.write(f"**Current Market Conditions:**\n\n*{MARKET_STORIES[market]}*")
        with col_t:
            st.write(f"**Investment Sector:**\n\n*{TYPE_STORIES[fund_type]}*")
        st.write(f"**Payout Multiplier:** If a startup succeeds, it pays out **{b}x** the investment profit.")
    
    tab1, tab2, tab3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with tab1:
        st.subheader("Stage 1: Probability Discovery")
        st.markdown("Your team has audited 50 recent startups in this sector. Review the raw data below to determine the **Win Probability ($p$)**.")
        
        if st.button("Run Audit"):
            scenario_seed = sum(ord(char) for char in st.session_state.lab_id + market + fund_type)
            np.random.seed(scenario_seed)
            st.session_state.audit_data = ["SUCCESS" if np.random.random() < student_p else "FAILURE" for _ in range(50)]
            st.session_state.audit_verified = False

        if st.session_state.audit_data:
            icons = ["🟩" if r == "SUCCESS" else "🟥" for r in st.session_state.audit_data]
            actual_wins = st.session_state.audit_data.count("SUCCESS")
            actual_p = actual_wins / 50
            
            # Displaying the "Problem"
            st.info(f"Audit Results: We found {actual_wins} successes and {50-actual_wins} failures.")
            for i in range(0, 50, 10):
                st.write(" ".join(icons[i:i+10]))
            
            # (2) PROBABILITY PROMPT
            st.write("---")
            user_p = st.number_input("Based on this sample, what is the Probability of Success ($p$)? (Enter as a decimal, e.g. 0.44)", 
                                    min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
            
            if st.button("Verify Probability"):
                if abs(user_p - actual_p) < 0.001:
                    st.session_state.audit_verified = True
                    st.success(f"Correct. The sector has a win rate of {actual_p:.2f}. Stage 2 Unlocked.")
                else:
                    st.error(f"Incorrect. Use the formula: Successes / Total Cases.")

    with tab2:
        st.subheader("Stage 2: Volatility Stress Test")
        if not st.session_state.audit_verified:
            st.info("🔒 Complete and Verify the Stage 1 Audit to unlock.")
        else:
            st.write(f"Now that you know $p = {actual_p:.2f}$, watch how it behaves in a sequence of 100 trials.")
            # Logic for the 100-flip will go here in the next step

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
