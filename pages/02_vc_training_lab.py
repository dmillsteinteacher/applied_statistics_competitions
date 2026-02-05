import streamlit as st
import numpy as np

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="VC Training Lab", layout="wide")

# --- 2. THE SECRET TRUTH ---
B_VALUES = {
    "Type 1: The Basics": 0.5,
    "Type 2: Tech Apps": 2.0,
    "Type 3: Big Science": 8.0
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
# Stage 1 Audit results
if "audit_results" not in st.session_state:
    st.session_state.audit_results = []

# --- 4. HELPER FUNCTIONS ---
def initialize_student_matrix(lab_id):
    """Generates a unique p-matrix for the student using Gaussian noise."""
    # Seed based on Lab ID for persistence
    seed = sum(ord(char) for char in lab_id)
    np.random.seed(seed)
    
    new_matrix = {}
    for market, types in BASE_P_MATRIX.items():
        new_matrix[market] = {}
        for fund_type, base_p in types.items():
            # Add Gaussian noise (mean=0, std_dev=0.02)
            noise = np.random.normal(0, 0.02)
            new_matrix[market][fund_type] = np.clip(base_p + noise, 0.01, 0.99)
    return new_matrix

# --- 5. SIDEBAR: GATEKEEPER LOGIC ---
with st.sidebar:
    st.title("👨‍💼 VC Research Desk")
    
    # Lab ID entry is the primary gate
    id_input = st.text_input("Enter Lab ID to Initialize:", value=st.session_state.lab_id)
    
    if id_input != st.session_state.lab_id:
        st.session_state.lab_id = id_input
        if id_input:
            st.session_state.p_matrix = initialize_student_matrix(id_input)
            st.session_state.audit_results = [] # Clear any previous audit data
            st.success(f"Lab Environment Initialized: {id_input}")

    # Only show scenario selection if Lab ID is present
    if st.session_state.lab_id:
        st.divider()
        st.subheader("Select Research Cell")
        market_choice = st.selectbox("Market Environment", list(BASE_P_MATRIX.keys()))
        type_choice = st.selectbox("Fund Type", list(B_VALUES.keys()))
        
        if st.button("Open Research Lab"):
            st.session_state.current_scenario = (market_choice, type_choice)
            st.session_state.audit_results = [] # Reset audit results when switching cells

# --- 6. MAIN INTERFACE ---
st.title("Venture Capital Lab")

# Gating logic for the main UI
if not st.session_state.lab_id:
    st.warning("⚠️ Access Denied: Please enter your **Lab ID** in the sidebar to initialize the research environment.")
    st.info("Your Lab ID ensures your data persists across multiple sessions.")
elif not st.session_state.current_scenario:
    st.info("Select a **Market Environment** and **Fund Type** in the sidebar to begin your audit.")
else:
    market, fund_type = st.session_state.current_scenario
    student_p = st.session_state.p_matrix[market][fund_type]
    b = B_VALUES[fund_type]
    
    st.header(f"Investigating: {fund_type}")
    st.caption(f"Context: {market} | Payout Multiple: {b}x")
    
    tab1, tab2, tab3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with tab1:
        st.subheader("Industry Audit: Historical Records")
        st.markdown(f"Analyze the last **50 companies** in this sector to determine the success rate ($p$).")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Audit Logic: Click to generate next result
            can_audit = len(st.session_state.audit_results) < 50
            if st.button("Analyze Next Company", disabled=not can_audit):
                # Unique seed for this specific company flip
                scenario_seed = sum(ord(char) for char in st.session_state.lab_id + market + fund_type)
                np.random.seed(scenario_seed + len(st.session_state.audit_results))
                
                result = "SUCCESS" if np.random.random() < student_p else "FAILURE"
                st.session_state.audit_results.append(result)
            
            if not can_audit:
                st.success("✅ Audit Complete. 50/50 cases reviewed.")
                st.write("Please record your findings in your Research Log.")
            
            st.write(f"**Progress:** {len(st.session_state.audit_results)} / 50")
            
        with col2:
            if st.session_state.audit_results:
                wins = st.session_state.audit_results.count("SUCCESS")
                losses = st.session_state.audit_results.count("FAILURE")
                
                st.write(f"✅ Successes: **{wins}** | ❌ Failures: **{losses}**")
                
                # Visual Ticker
                history_icons = ["🟩" if r == "SUCCESS" else "🟥" for r in st.session_state.audit_results]
                # Break icons into rows of 10 for better scannability
                for i in range(0, len(history_icons), 10):
                    st.write(" ".join(history_icons[i:i+10]))

    with tab2:
        st.write("### Stage 2: Volatility Stress Test")
        if len(st.session_state.audit_results) < 50:
            st.lock("Please complete the Stage 1 Audit to unlock.")
        else:
            st.write("Ready to observe 100 consecutive outcomes.")

    with tab3:
        st.write("### Stage 3: Calibration")
        st.lock("Please complete the Stage 2 Stress Test to unlock.")

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
