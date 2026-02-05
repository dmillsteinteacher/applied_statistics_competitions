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
            st.success(f"Lab Environment Initialized: {id_input}")

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
    st.info("Select a **Market Environment** and **Fund Type** in the sidebar to begin.")
else:
    market, fund_type = st.session_state.current_scenario
    student_p = st.session_state.p_matrix[market][fund_type]
    b = B_VALUES[fund_type]
    
    st.header(f"Investigating: {fund_type}")
    st.caption(f"Context: {market} | Payout Multiple: {b}x")
    
    tab1, tab2, tab3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with tab1:
        st.subheader("Industry Audit: Data Retrieval")
        st.markdown("Download the last 50 historical records. Count the number of **Successes** to verify the sector's win rate.")
        
        if st.button("Fetch Historical Records"):
            # Fixed seed for this specific scenario and student
            scenario_seed = sum(ord(char) for char in st.session_state.lab_id + market + fund_type)
            np.random.seed(scenario_seed)
            # Generate all 50 at once
            st.session_state.audit_data = ["SUCCESS" if np.random.random() < student_p else "FAILURE" for _ in range(50)]
            st.session_state.audit_verified = False

        if st.session_state.audit_data:
            # Display the data in a visually "raw" format
            icons = ["🟩" if r == "SUCCESS" else "🟥" for r in st.session_state.audit_data]
            actual_wins = st.session_state.audit_data.count("SUCCESS")
            
            st.write("---")
            # Create 5 rows of 10
            for i in range(0, 50, 10):
                st.write(" ".join(icons[i:i+10]))
            st.write("---")
            
            # The Verification Step
            user_count = st.number_input("How many SUCCESSES (🟩) did you count?", min_value=0, max_value=50, step=1)
            
            if st.button("Verify Audit"):
                if user_count == actual_wins:
                    st.session_state.audit_verified = True
                    st.success(f"Audit Verified. Calculated p = {actual_wins/50:.2f}. Stage 2 Unlocked.")
                else:
                    st.error("Count incorrect. Please recount the green records.")

    with tab2:
        st.subheader("Stage 2: Volatility Stress Test")
        if not st.session_state.audit_verified:
            st.info("🔒 Complete and Verify the Stage 1 Audit to unlock this section.")
        else:
            st.write("In this stage, you will observe a sequence of 100 consecutive outcomes to understand how variance feels.")
            # Placeholder for the 100-flip logic

    with tab3:
        st.subheader("Stage 3: Calibration")
        if not st.session_state.audit_verified:
            st.info("🔒 Complete and Verify the Stage 1 Audit to unlock this section.")
        else:
            st.write("Research Phase: Determine your optimal investment size ($f$).")

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
