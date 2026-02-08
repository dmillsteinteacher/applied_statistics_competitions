import streamlit as st
import pandas as pd
import numpy as np
import importlib.util
import os

# --- 1. MODULE LOADING (Path-Corrected for Root) ---
def load_mod(name):
    current_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(current_dir)
    path = os.path.join(root_dir, name)
    if not os.path.exists(path):
        path = os.path.join(current_dir, name)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None: return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

nav = load_mod("02_vc_lab_narrative.py")
engine = load_mod("02_vc_lab_engine.py")

if nav is None or engine is None:
    st.error("Missing critical helper files in Root directory.")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="VC Training Lab", layout="wide")
st.title("💼 Venture Capital Training Lab")
st.markdown(nav.LAB_INTRODUCTION)

# --- 3. TABBED INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🔍 Phase 1: Internal Audit", "📈 Phase 2: Probability Study", "💰 Phase 3: Reinvestment Strategy"])

with tab1:
    st.header("Step 1: Gather Intelligence")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        sector_choice = st.selectbox("Select Sector", list(nav.TYPE_STORY.keys()))
        market_choice = st.selectbox("Select Market Environment", list(nav.MARKET_STORIES.keys()))
        if st.button("Generate Audit Memo"):
            # Sample 50 ventures
            successes = np.random.binomial(50, 0.74) 
            failures = 50 - successes
            ef = int(failures * 0.6)
            mf = failures - ef
            st.session_state.memo = nav.MEMO_TEMPLATE.format(
                sector=sector_choice, market=market_choice, ef=ef, mf=mf
            )
            
    with col2:
        if 'memo' in st.session_state:
            st.info(st.session_state.memo)
        else:
            st.write("Awaiting audit request...")

with tab2:
    st.header("Step 2: Estimate Success Probability")
    st.write("Based on the data in Phase 1, what is your estimate for $p$?")
    p_est = st.number_input("Estimated Probability (0.0 - 1.0)", 0.0, 1.0, 0.7, step=0.01)
    st.write(f"Your current working hypothesis is that this sector has a **{p_est:.1%}** success rate.")

with tab3:
    st.header("Step 3: Select Reinvestment Strategy")
    st.write("Test your chosen $f$ (fraction of capital) against the sector's payout structure.")
    
    f_val = st.slider("Select your reinvestment fraction (f)", 0.0, 1.0, 0.1, 0.01)
    
    if st.button("Run Simulation"):
        b = nav.B_VALS[sector_choice]
        # Run simulation using the engine
        results = engine.run_simulation(f_val, 0.74, b)
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Median Result", f"${results['Median']:,.0f}")
        col_res2.metric("Insolvency Rate", f"{results['Insolvency Rate']:.1%}")
        
        st.success(f"Final Strategy: Sector {sector_choice} with f={f_val}. Submit this to your instructor.")

# --- END OF FILE ---
