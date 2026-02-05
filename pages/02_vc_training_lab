import streamlit as st
import numpy as np

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="VC Training Lab", layout="wide")

# --- 2. THE SECRET TRUTH (Master Design Blueprint) ---
# b values (payouts) for each of the 3 Fund Types
B_VALUES = {
    "Type 1: The Basics": 0.5,
    "Type 2: Tech Apps": 2.0,
    "Type 3: Big Science": 8.0
}

# Base p values (probabilities) for the 3x3 matrix
BASE_P_MATRIX = {
    "Market A: The Boom": {"Type 1: The Basics": 0.90, "Type 2: Tech Apps": 0.60, "Type 3: Big Science": 0.25},
    "Market B: The Squeeze": {"Type 1: The Basics": 0.70, "Type 2: Tech Apps": 0.35, "Type 3: Big Science": 0.08},
    "Market C: Rule Change": {"Type 1: The Basics": 0.80, "Type 2: Tech Apps": 0.45, "Type 3: Big Science": 0.15},
}

# --- 3. SESSION STATE INITIALIZATION ---
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "p_matrix" not in st.session_state:
    st.session_state.p_matrix = {}
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = None

# --- 4. HELPER FUNCTIONS ---
def initialize_student_matrix(student_id):
    """Generates a unique p-matrix for the student using Gaussian noise."""
    # Use the student_id string to seed the random number generator for consistency
    seed = sum(ord(char) for char in student_id)
    np.random.seed(seed)
    
    new_matrix = {}
    for market, types in BASE_P_MATRIX.items():
        new_matrix[market] = {}
        for fund_type, base_p in types.items():
            # Add Gaussian noise (mean=0, std_dev=0.02)
            noise = np.random.normal(0, 0.02)
            # Clip to ensure p stays between 0.01 and 0.99
            new_matrix[market][fund_type] = np.clip(base_p + noise, 0.01, 0.99)
    return new_matrix

# --- 5. SIDEBAR: STUDENT LOGIN & SELECTION ---
with st.sidebar:
    st.title("👨‍💼 VC Research Desk")
    id_input = st.text_input("Enter Student ID to Load Progress:", value=st.session_state.student_id)
    
    if id_input != st.session_state.student_id:
        st.session_state.student_id = id_input
        if id_input:
            st.session_state.p_matrix = initialize_student_matrix(id_input)
            st.success(f"Log: Matrix Generated for {id_input}")

    if st.session_state.student_id:
        st.divider()
        st.subheader("Select Research Cell")
        market_choice = st.selectbox("Market Environment", list(BASE_P_MATRIX.keys()))
        type_choice = st.selectbox("Fund Type", list(B_VALUES.keys()))
        
        if st.button("Open Research Lab"):
            st.session_state.current_scenario = (market_choice, type_choice)

# --- 6. MAIN INTERFACE ---
st.title("Venture Capital Simulation: Training Lab")

if not st.session_state.student_id:
    st.info("Please enter your Student ID in the sidebar to begin your research.")
elif not st.session_state.current_scenario:
    st.info("Select a Market and Fund Type in the sidebar to open the Research Lab.")
else:
    market, fund_type = st.session_state.current_scenario
    student_p = st.session_state.p_matrix[market][fund_type]
    b = B_VALUES[fund_type]
    
    st.header(f"Lab: {fund_type}")
    st.subheader(f"Environment: {market}")
    
    # Placeholder for the 3 Stages
    tab1, tab2, tab3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with tab1:
        st.write("### Stage 1: Data Room")
        st.write("This is where the 50-case audit will live.")
        # Debugging view for the 'Vibe' coder:
        # st.write(f"Secret Student P: {student_p:.4f}")
        # st.write(f"Fixed b: {b}")

    with tab2:
        st.write("### Stage 2: Volatility")
        st.write("### Stage 2: Volatility")
        st.write("This is where the 100-flip sequence will live.")

    with tab3:
        st.write("### Stage 3: Optimization")
        st.write("This is where the Parametric Slider will live.")

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
