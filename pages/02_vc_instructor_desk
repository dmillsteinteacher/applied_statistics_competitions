import streamlit as st
import pandas as pd
import numpy as np
import importlib.util
import os

# --- 1. SET PAGE CONFIG (MUST BE ABSOLUTELY FIRST) ---
st.set_page_config(page_title="VC Instructor Desk", layout="wide")

# --- 2. MODULE LOADING ---
def load_mod(name):
    # Check if we are in the pages directory or root
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, name)
    
    # If not found in current dir, check parent dir
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(base_dir), name)
        
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Safe loading to prevent menu-hide on failure
nav = load_mod("02_vc_lab_narrative.py")
inst_eng = load_mod("02_vc_instructor_engine.py")

if nav is None or inst_eng is None:
    st.error("Missing critical helper files (Narrative or Engine).")
    st.stop()

st.title("🏆 VC Competition: Strategy Leaderboard")

# --- 3. SECURITY & LOGIC ---
pwd = st.sidebar.text_input("Instructor Password", type="password")

if pwd == "VC_LEADER":
    with st.expander("🛠️ Secret Scenario Configuration", expanded=True):
        col1, col2 = st.columns(2)
        m_sel = col1.selectbox("Set Secret Market", list(nav.MARKET_STORIES.keys()))
        
        day_seed_input = col2.text_input("Day Seed (Student Lab ID)", value="LAB123")
        day_seed = sum(ord(c) for c in day_seed_input)
        np.random.seed(day_seed)
        
        m_base = {"Market A: The Boom": 0.9, "Market B: The Squeeze": 0.7, "Market C: Rule Change": 0.8}
        s_mult = {"Type 1: The Basics": 1.0, "Type 2: Tech Apps": 0.6, "Type 3: Big Science": 0.2}
        p_matrix = {m: {s: np.clip(p*s_mult[s] + np.random.normal(0,0.02), 0.01, 0.99) 
                       for s in nav.TYPE_STORY} for m, p in m_base.items()}

    st.header("📢 Current Market Briefing")
    st.info(f"**Field Report:** {nav.MARKET_STORIES[m_sel]}")
    
    if "contestants" not in st.session_state:
        st.session_state.contestants = []

    with st.form("entry_form", clear_on_submit=True):
        f_col1, f_col2, f_col3 = st.columns([2, 2, 1])
        s_name = f_col1.text_input("Student Name")
        s_sec = f_col2.selectbox("Chosen Sector", list(nav.TYPE_STORY.keys()))
        s_f = f_col3.number_input("Strategy (f)", 0.0, 1.0, 0.1, step=0.01)
        if st.form_submit_button("Add Strategy"):
            if s_name:
                st.session_state.contestants.append({"Name": s_name, "Sector": s_sec, "f": s_f})
                st.rerun()

    if st.session_state.contestants and st.button("🚀 RUN SIMULATION"):
        results = []
        for c in st.session_state.contestants:
            p_true = p_matrix[m_sel][c['Sector']]
            b_val = nav.B_VALS[c['Sector']]
            # Use the correctly loaded engine module
            stats = inst_eng.run_competition_sim(c['f'], p_true, b_val)
            stats.update({"Student": c['Name'], "Sector": c['Sector'], "f": c['f']})
            results.append(stats)
            
        df = pd.DataFrame(results)
        cols = ["Student", "Sector", "f", "Median", "Insolvency Rate", "Min", "Q1", "Q3", "Max", "Mean"]
        st.dataframe(df[cols].sort_values("Median", ascending=False))

    if st.button("Clear Contestants"):
        st.session_state.contestants = []
        st.rerun()
else:
    st.warning("Enter password in sidebar.")

# --- SAFETY PADDING ---
# 1
# 2
# 3
# 4
# 5
# --- END OF FILE ---
