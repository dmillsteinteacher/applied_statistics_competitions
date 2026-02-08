import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

# --- TAB 3: REINVESTMENT STRATEGY ---
with tab3:
    st.header("Step 3: Determine Allocation")
    if not st.session_state.p_verified:
        st.warning("Locked: Verify probability in Phase 1.")
    else:
        b_val = nav.B_VALS[sector_choice]
        st.markdown(f"**Environment:** {market_choice} | **Target p:** {st.session_state.current_p:.2f} | **Payback b:** {b_val}x")
        
        f_guess = st.slider("Select reinvestment fraction (f)", 0.0, 1.0, 0.1, 0.01)
        
        if st.button("Run Simulation", key="sim_btn"):
            # 1. Run the simulation batch
            res = engine.run_simulation(f_guess, st.session_state.current_p, b_val, n_steps=50)
            
            # 2. Visualization (The specific journey of ONE fund)
            history = res['History']
            random_idx = np.random.randint(0, history.shape[0])
            latest_path = history[random_idx, :] 
            steps = np.arange(len(latest_path))

            st.subheader(f"Individual Fund Trajectory (Trial #{random_idx})")
            fig, ax = plt.subplots(figsize=(10, 4))
            
            is_insolvent = latest_path[-1] <= 1.0
            path_color = "#e74c3c" if is_insolvent else "#2ecc71"
            
            ax.plot(steps, latest_path, color=path_color, linewidth=2)
            ax.fill_between(steps, latest_path, color=path_color, alpha=0.1)
            
            ax.set_yscale('log')
            ax.set_xlabel("Reinvestment Cycles")
            ax.set_ylabel("Wealth (Log Scale)")
            ax.grid(True, which="both", ls="-", alpha=0.2)
            ax.set_ylim(bottom=0.1) 
            st.pyplot(fig)

            st.divider()

            # 3. Post-Mortem / Batch Statistics (The broader risk context)
            st.subheader("Strategy Post-Mortem")
            st.write("""
                The chart above shows just **one** possible outcome. To understand your true risk, 
                look at the aggregate performance of 100 funds using this exact same strategy:
            """)
            
            c1, c2 = st.columns(2)
            c1.metric("Median Final Wealth", f"${res['Median']:,.0f}")
            c2.metric("Insolvency Rate", f"{res['Insolvency Rate']:.1%}")

            with st.expander("What does the Insolvency Rate mean?"):
                st.write(f"""
                    The **Insolvency Rate of {res['Insolvency Rate']:.1%}** means that in {res['Insolvency Rate']*100:.0f} 
                    out of 100 universes, a manager using your **f={f_guess}** strategy lost the entire fund. 
                    
                    Even if your specific chart above looks successful, a high insolvency rate 
                    suggests you are 'overbetting' and eventually your luck will run out.
                """)
