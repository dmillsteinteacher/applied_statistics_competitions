import streamlit as st
import pandas as pd
import numpy as np
import importlib.util
import os

# --- 1. MODULE LOADING ---
def load_mod(name):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), name)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

nav = load_mod("02_vc_lab_narrative.py")
engine = load_mod("02_vc_lab_engine.py")

# --- 2. SESSION STATE MANAGEMENT ---
if 'p_verified' not in st.session_state: st.session_state.p_verified = False
if 'current_p' not in st.session_state: st.session_state.current_p = 0.0
if 'memo_text' not in st.session_state: st.session_state.memo_text = None
if 'trial_history' not in st.session_state: st.session_state.trial_history = []

# --- 3. PAGE CONFIG ---
st.set_page_config(page_title="VC Training Lab", layout="wide")
st.title("💼 Venture Capital Training Lab")
st.markdown(nav.LAB_INTRODUCTION)

# --- 4. THREE-TAB STRUCTURE ---
tab1, tab2, tab3 = st.tabs([
    "🔍 Phase 1: Internal Audit", 
    "📊 Phase 2: Probability Study", 
    "💰 Phase 3: Reinvestment Strategy"
])

# --- TAB 1: THE AUDIT & VERIFICATION GATE ---
with tab1:
    st.header("Step 1: Audit the Market")
    c1, c2 = st.columns(2)
    
    with c1:
        sector_choice = st.selectbox("Select Investment Sector", list(nav.TYPE_STORY.keys()))
        market_choice = st.selectbox("Select Market Environment", list(nav.MARKET_STORIES.keys()))
        
        if st.button("Generate Audit Memo"):
            base_p = nav.P_MATRIX[market_choice][sector_choice]
            noisy_p = np.clip(np.random.normal(base_p, 0.02), 0.1, 0.9)
            
            successes = int(np.random.binomial(50, noisy_p))
            failures = 50 - successes
            
            st.session_state.current_p = successes / 50.0
            st.session_state.p_verified = False 
            
            ef = int(failures * 0.6)
            mf = failures - ef
            st.session_state.memo_text = nav.MEMO_TEMPLATE.format(
                sector=sector_choice, market=market_choice, ef=ef, mf=mf
            )
            
    with c2:
        if st.session_state.memo_text:
            st.info(st.session_state.memo_text)
            input_p = st.number_input("Determine the probability of success (p):", 0.0, 1.0, step=0.01)
            if st.button("Verify Probability"):
                if abs(input_p - st.session_state.current_p) < 0.001:
                    st.success("✅ Verification successful. You may proceed to Phase 2.")
                    st.session_state.p_verified = True
                else:
                    st.error("❌ Probability incorrect. Review the memo and calculate: Successes / 50.")

# --- TAB 2: PROBABILITY STUDY ---
with tab2:
    st.header("Step 2: Visualize Variance")
    if not st.session_state.p_verified:
        st.warning("Please verify the probability in Phase 1 to unlock this study.")
    else:
        st.write(f"Studying performance for **p = {st.session_state.current_p}**")
        if st.button("Simulate 100 Trials"):
            trials = np.random.choice([1, 0], size=100, p=[st.session_state.current_p, 1-st.session_state.current_p])
            fail_runs = "".join(trials.astype(str)).split('1')
            max_fail = len(max(fail_runs, key=len))
            
            st.session_state.trial_history.insert(0, {
                "id": len(st.session_state.trial_history) + 1,
                "trials": trials,
                "wins": sum(trials),
                "max_fail": max_fail
            })
            
        for run in st.session_state.trial_history:
            with st.expander(f"Trial Set #{run['id']} | Successes: {run['wins']} | Max Consecutive Failures: {run['max_fail']}"):
                cols = st.columns(20)
                for i, result in enumerate(run['trials']):
                    cols[i % 20].write("🟩" if result == 1 else "🟥")

# --- TAB 3: REINVESTMENT STRATEGY (Updated with b-value visibility) ---
with tab3:
    st.header("Step 3: Determine Allocation")
    if not st.session_state.p_verified:
        st.warning("Locked: Verify probability in Phase 1.")
    else:
        # Get the b_val for display and logic
        b_val = nav.B_VALS[sector_choice]
        
        st.subheader(f"Strategic Profile")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Environment", market_choice)
        col_b.metric("Success Prob (p)", f"{st.session_state.current_p:.2f}")
        col_c.metric("Payback Ratio (b)", f"{b_val}x")
        
        st.write(f"Testing strategy for **{sector_choice}**")
        f_guess = st.slider("Select reinvestment fraction (f)", 0.0, 1.0, 0.1, 0.01)
        
        if st.button("Run Simulation"):
            res = engine.run_simulation(f_guess, st.session_state.current_p, b_val)
            
            st.metric("Median Wealth Growth", f"${res['Median']:,.0f}")
            st.metric("Insolvency Rate", f"{res['Insolvency Rate']:.1%}")
            
            if res['Insolvency Rate'] > 0.1:
                st.error(f"High risk of ruin! With b={b_val}, f={f_guess} is too aggressive.")
            else:
                st.success(f"Strategy Validated. You are betting on a {b_val}x payout.")
            if res['Insolvency Rate'] > 0.1:
                st.error("Risk of Ruin is high for this environment. Consider a more conservative f.")
            else:
                st.success(f"Strategy Validated for {market_choice}. Submit f={f_guess} for the contest.")
