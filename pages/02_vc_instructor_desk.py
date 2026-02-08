import streamlit as st
import pandas as pd
import numpy as np
import importlib.util
import os

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="VC Instructor Desk", layout="wide")

# --- 2. MODULE LOADING ---
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
inst_eng = load_mod("02_vc_instructor_engine.py")

if nav is None or inst_eng is None:
    st.error("Missing critical helper files in Root. Check file locations.")
    st.stop()

# --- 3. HELPER: CURRENCY FORMATTING (K/M notation) ---
def format_currency(value):
    if value == 0: return "$0"
    abs_val = abs(value)
    if abs_val >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    elif abs_val >= 1_000:
        return f"${value / 1_000:.1f}K"
    else:
        return f"${int(value)}"

# --- 4. UI SETUP ---
st.title("🏆 VC Competition: Strategy Leaderboard")

pwd = st.sidebar.text_input("Instructor Password", type="password")

if pwd == "VC_LEADER":
    # SCENARIO CONFIG
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

    # STUDENT ENTRY FORM
    if "contestants" not in st.session_state:
        st.session_state.contestants = []

    st.subheader("Contestant Registration")
    with st.form("entry_form", clear_on_submit=True):
        f_col1, f_col2, f_col3 = st.columns([2, 2, 1])
        s_name = f_col1.text_input("Student Name")
        s_sec = f_col2.selectbox("Chosen Sector", list(nav.TYPE_STORY.keys()))
        s_f = f_col3.number_input("Strategy (f)", 0.0, 1.0, 0.1, step=0.01)
        if st.form_submit_button("Add Strategy"):
            if s_name:
                st.session_state.contestants.append({"Name": s_name, "Sector": s_sec, "f": s_f})
                st.rerun()

    # --- 5. THE LIVE ROSTER ---
    if st.session_state.contestants:
        st.write("### Pending Roster")
        roster_df = pd.DataFrame(st.session_state.contestants)
        st.table(roster_df) 
        
        col_run, col_clear = st.columns([1, 4])
        run_sim = col_run.button("🚀 RUN SIMULATION")
        if col_clear.button("Clear All Contestants"):
            st.session_state.contestants = []
            st.rerun()

        # --- 6. THE COMPETITION RESULTS ---
        if run_sim:
            results = []
            for c in st.session_state.contestants:
                p_true = p_matrix[m_sel][c['Sector']]
                b_val = nav.B_VALS[c['Sector']]
                
                stats = inst_eng.run_competition_sim(c['f'], p_true, b_val)
                
                stats["IQR"] = stats["Q3"] - stats["Q1"]
                stats.update({"Student": c['Name'], "Sector": c['Sector'], "f": c['f']})
                results.append(stats)
            
            df = pd.DataFrame(results)
            
            cols = ["Student", "Sector", "f", "Median", "IQR", "Std Dev", "Insolvency Rate", "Min", "Q1", "Q3", "Max", "Mean"]
            df_display = df[cols].sort_values("Median", ascending=False)
            
            st.header("📊 Final Competition Results")
            st.balloons()
            
            dollar_cols = ["Median", "IQR", "Std Dev", "Min", "Q1", "Q3", "Max", "Mean"]
            formatted_df = df_display.copy()
            for col in dollar_cols:
                formatted_df[col] = formatted_df[col].apply(format_currency)
            
            formatted_df["Insolvency Rate"] = formatted_df["Insolvency Rate"].apply(lambda x: f"{x:.1%}")
            
            st.dataframe(formatted_df, use_container_width=True)
            
            st.success("Analysis: High Std Dev relative to IQR suggests significant 'Outlier' success or heavy tail risk.")

else:
    st.warning("Please enter the Instructor Password in the sidebar.")

# --- SAFETY PADDING ---
# 1
# 2
# 3
# --- END OF FILE ---
