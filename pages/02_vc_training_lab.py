import streamlit as st
import pandas as pd
import numpy as np
import importlib.util
import os

# --- 1. MODULE LOADING ---
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

# --- 2. SESSION STATE MANAGEMENT ---
if 'audit_p' not in st.session_state: st.session_state.audit_p = None
if 'p_verified' not in st.session_state: st.session_state.p_verified = False
if 'simulation_history' not in st.session_state: st.session_state.simulation_history = []

# --- 3. UI SETUP ---
st.set_page_config(page_title="VC Training Lab", layout="wide")
st.title("💼 Venture Capital Training Lab")
st.markdown(nav.LAB_INTRODUCTION)

tab1, tab2, tab3 = st.tabs(["🔍 Phase 1: Probability Audit", "📊 Phase 2: Success Intuition", "💰 Phase 3: Strategy Selection"])

# --- TAB 1: AUDIT & VERIFICATION ---
with tab1:
    st.header("Determine Market Probability")
    c1, c2 = st.columns(2)
    
    with c1:
        sector = st.selectbox("Sector", list(nav.TYPE_STORY.keys()))
        market = st.selectbox("Market", list(nav.MARKET_STORIES.keys()))
        if st.button("Generate Audit Memo"):
            # Fixed p for training context (e.g., 0.74)
            st.session_state.audit_p = 0.74 
            successes = 37 # 37/50 = 0.74
            failures = 13
            ef, mf = 8, 5
            st.session_state.memo = nav.MEMO_TEMPLATE.format(sector=sector, market=market, ef=ef, mf=mf)
    
    with c2:
        if 'memo' in st.session_state:
            st.info(st.session_state.memo)
            user_p = st.number_input("Enter the probability (p) based on this history:", 0.0, 1.0, step=0.01)
            if st.button("Verify Probability"):
                if abs(user_p - st.session_state.audit_p) < 0.001:
                    st.success("Correct! You may now proceed to Phase 2.")
                    st.session_state.p_verified = True
                else:
                    st.error("The probability does not match the memo records. Re-calculate (Successes / 50).")

# --- TAB 2: INTUITION (Red/Green Squares) ---
with tab2:
    st.header("Building Intuition: Variance in Action")
    if not st.session_state.p_verified:
        st.warning("Please verify the probability in Phase 1 before running intuition trials.")
    else:
        if st.button("Run 100-Trial History"):
            # Generate 100 trials
            trials = np.random.choice([1, 0], size=100, p=[st.session_state.audit_p, 1-st.session_state.audit_p])
            
            # Calculate runs
            runs = "".join(trials.astype(str)).split('1')
            max_fail_run = len(max(runs, key=len))
            
            # Record for history
            trial_record = {
                "id": len(st.session_state.simulation_history) + 1,
                "trials": trials,
                "successes": sum(trials),
                "failures": 100 - sum(trials),
                "max_fail": max_fail_run
            }
            st.session_state.simulation_history.insert(0, trial_record)

        # Display History in Expanders
        for record in st.session_state.simulation_history:
            with st.expander(f"Run #{record['id']}: {record['successes']} Wins / {record['failures']} Losses"):
                # Display Grid
                cols = st.columns(20)
                for i, t in enumerate(record['trials']):
                    color = "🟩" if t == 1 else "🟥"
                    cols[i % 20].write(color)
                
                st.write(f"**Longest losing streak in this universe:** {record['max_fail']} consecutive failures.")

# --- TAB 3: STRATEGY ---
with tab3:
    st.header("Select Reinvestment Strategy")
    if not st.session_state.p_verified:
        st.warning("Please complete Phase 1 first.")
    else:
        f_final = st.slider("Target Allocation (f)", 0.0, 1.0, 0.1, 0.01)
        if st.button("Run Strategy Simulation"):
            b = nav.B_VALS[sector]
            res = engine.run_simulation(f_final, st.session_state.audit_p, b)
            st.metric("Median Ending Wealth", f"${res['Median']:,.0f}")
            st.metric("Insolvency Rate", f"{res['Insolvency Rate']:.1%}")
