import streamlit as st
import pandas as pd
import numpy as np
import importlib.util
import os

# --- 1. MODULE LOADING (STRICT PATH UPDATE) ---
def load_mod(name):
    # Get the directory where THIS file is (/pages)
    current_dir = os.path.dirname(__file__)
    # Go up one level to the Root directory
    root_dir = os.path.dirname(current_dir)
    # Target the file in the Root
    path = os.path.join(root_dir, name)
    
    if not os.path.exists(path):
        # Fallback for local testing/different structures
        path = os.path.join(current_dir, name)

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None: return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# These now look in the root folder for the moved files
nav = load_mod("02_vc_lab_narrative.py")
engine = load_mod("02_vc_lab_engine.py")

if nav is None or engine is None:
    st.error("Missing critical helper files in Root. Check file locations.")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="VC Training Lab", layout="wide")
st.title("💼 Venture Capital Training Lab")

# --- 3. AUDIT & PROBABILITY STUDY ---
st.markdown(nav.LAB_INTRODUCTION)

st.header("Phase 1: Internal Audit")
col1, col2 = st.columns(2)

with col1:
    sector = st.selectbox("Select Sector", list(nav.TYPE_STORY.keys()))
    market = st.selectbox("Select Market Environment", list(nav.MARKET_STORIES.keys()))
    if st.button("Generate Audit Memo"):
        # Audit logic: 50 trials
        successes = np.random.binomial(50, 0.7) 
        failures = 50 - successes
        ef = int(failures * 0.6)
        mf = failures - ef
        st.session_state.memo = nav.MEMO_TEMPLATE.format(
            sector=sector, market=market, ef=ef, mf=mf
        )

with col2:
    if 'memo' in st.session_state:
        st.info(st.session_state.memo)

# --- 4. STRATEGY TESTING ---
st.header("Phase 2: Strategy Testing")
f_guess = st.slider("Select your f", 0.0, 1.0, 0.1, 0.01)

if st.button("Run Simulation"):
    b = nav.B_VALS[sector]
    # Standard training p = 0.7
    results = engine.run_simulation(f_guess, 0.7, b)
    
    st.write(f"**Median Result:** ${results['Median']:,.0f}")
    st.write(f"**Insolvency Rate:** {results['Insolvency Rate']:.1%}")

# --- SAFETY PADDING ---
# --- END OF FILE ---
