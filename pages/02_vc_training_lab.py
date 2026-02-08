import streamlit as st
import pandas as pd
import numpy as np
import importlib.util
import os

# --- 1. MODULE LOADING ---
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
st.set_page_config(page_title="Venture Capital Lab", layout="wide")
st.title("💼 Venture Capital Training Lab")

# --- 3. SESSION STATE ---
if 'research_data' not in st.session_state:
    st.session_state.research_data = {}

# --- 4. SIDEBAR: RESEARCH CONTROLS ---
with st.sidebar:
    st.header("Research Desk")
    selected_sector = st.selectbox("Select Sector to Research", list(nav.TYPE_STORY.keys()))
    
    if st.button("Run 100-Trial Research"):
        # Logic to pull P and B from narrative
        p_base = 0.7  # Simplified base for student side
        b_val = nav.B_VALS[selected_sector]
        
        # Use a fixed f=0.1 just for research purposes
        res = engine.run_simulation(0.1, p_base, b_val, trials=100)
        st.session_state.research_data[selected_sector] = res
        st.success(f"Research complete for {selected_sector}")

# --- 5. MAIN UI ---
st.markdown(nav.LAB_INTRODUCTION)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sector Briefing")
    st.info(nav.TYPE_STORY[selected_sector])

with col2:
    st.subheader("Research Findings")
    if selected_sector in st.session_state.research_data:
        data = st.session_state.research_data[selected_sector]
        st.write(f"**Observed Survival Rate:** {1 - data['Insolvency Rate']:.1%}")
        st.write(f"**Median Fund Growth:** {data['Median']/1000:.2f}x")
    else:
        st.write("No research data yet. Use the sidebar to investigate.")

st.divider()
st.subheader("Final Strategy Submission")
st.write("Based on your research, what fraction of your fund will you commit to this sector?")
final_f = st.slider("Select Strategy (f)", 0.0, 1.0, 0.1, 0.01)

if st.button("Lock In Strategy"):
    st.success(f"Strategy Locked: f={final_f} for {selected_sector}. Provide this to your instructor.")

# --- SAFETY PADDING ---
# 1
# 2
# 3
# --- END OF FILE ---
