import streamlit as st
import importlib.util
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="VC Training Lab", layout="wide")

# --- 2. MODULE LOADING ---
def load_mod(name):
    current_dir = Path(__file__).parent
    root_dir = current_dir.parent
    path = root_dir / name
    
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {name} at {path}")

    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

try:
    nav = load_mod("02_vc_lab_narrative.py")
    eng = load_mod("02_vc_lab_engine.py")
except Exception as e:
    st.error(f"❌ Module Load Error: {e}")
    st.stop()

# --- 3. SESSION STATE ---
for k in ["cur_scen", "audit", "verified", "history"]:
    if k not in st.session_state:
        st.session_state[k] = [] if k == "history" else None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("👨‍💼 VC Research Desk")
    
    if st.button("🔄 Start New Scenario (Reset All)"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    st.divider()
    m_sel = st.selectbox("Market Environment", list(nav.MARKET_STORIES.keys()))
    t_sel = st.selectbox("Sector Type", list(nav.TYPE_STORY.keys()))
    
    current = st.session_state.cur_scen
    if st.button("Open Research Lab") or (current and (m_sel != current[0] or t_sel != current[1])):
        if not current or (m_sel != current[0] or t_sel != current[1]):
            st.session_state.cur_scen = (m_sel, t_sel)
            st.session_state.audit, st.session_state.verified, st.session_state.history = None, False, []
            st.rerun()

# --- 5. MAIN INTERFACE ---
if not st.session_state.cur_scen:
    st.info("👋 Welcome. Select a scenario in the sidebar to begin.")
else:
    mkt, sec = st.session_state.cur_scen
    p_true = nav.P_MATRIX[mkt][sec]
    b = nav.B_VALS[sec]
    
    with st.expander("📄 Intelligence Briefing", expanded=True):
        st.write(f"**Current Context:** {nav.MARKET_STORIES[mkt]}")
        st.write(f"**Sector Profile:** {nav.TYPE_STORY[sec]}")
        st.write(f"**Payout Terms:** Success yields a **{b}x** multiple on investment.")

    t1, t2, t3 = st.tabs(["Stage 1: Audit", "Stage 2: Stress Test", "Stage 3: Sizing"])
    
    with t1:
        st.subheader("Probability Discovery")
        if st.button("Request Audit Report"):
            st.session_state.audit = eng.run_audit(mkt, sec, p_true)
            st.session_state.verified = False
        
        if st.session_state.audit:
            r = st.session_state.audit
            st.info(nav.MEMO_TEMPLATE.format(
                n=r['n'], 
                ef=r['ef'], 
                mf=r['mf'], 
                sector=sec, 
                market=mkt
            ))
            
            u_p = st.number_input("Enter your calculated Success Rate (p):", 0.0, 1.0, step=0.001, format="%.3f")
            
            if st.button("Verify Audit"):
                if abs(u_p - r['p_observed']) < 0.005:
                    st.session_state.verified = True
                    st.success(f"✅ Verified. Research confirms p = {r['p_observed']:.3f}")
                else: 
                    st.error("❌ Verification failed. Math: (Total Cases - Failures) / Total Cases.")

    with t2:
        st.subheader("Stage 2: Stress Test & Career Volatility")
        if not st.session_state.verified: 
            st.warning("🔒 Please verify the Audit in Stage 1.")
        else:
            p_val = st.session_state.audit['p_observed']
            st.info(f"**Research Goal:** Investigating failure streaks with a **{p_val:.3f}** success probability.")

            if st.button("Simulate 100-Deal Career"):
                st.session_state.history.append(eng.simulate_career(p_val))
            
            if st.session_state.history:
                lt = st.session_state.history[-1]
                m_col1, m_col2 = st.columns(2)
                m_col1.metric("Total Wins", f"{lt['Wins']}/100")
                m_col2.metric("Max Consecutive Failures", f"{lt['Max_Streak']}")
                st.write("### Sequence of Outcomes")
                st.write(" ".join(["🟩" if x else "🟥" for x in lt['raw']]))

    with t3:
        st.subheader("Capital Deployment Simulation")
        if not st.session_state.history: 
            st.warning("🔒 Complete Stage 2.")
        else:
            p_val = st.session_state.audit['p_observed']
            st.markdown(f"**Target p:** {p_val:.3f} | **Payback b:** {b}x")
            f = st.slider("Investment Size (f) as % of Remaining Fund", 0.0, 1.0, 0.1, 0.01)
            
            if st.button("Deploy Capital"):
                res = eng.run_simulation(f, p_val, b)
                history_matrix = res['History']
                random_idx = np.random.randint(0, history_matrix.shape[0])
                path = history_matrix[random_idx, :]
                
                st.write(f"#### Fund Journey (Simulated Universe #{random_idx})")
                
                fig, ax = plt.subplots(figsize=(10, 4))
                p_color = "#e74c3c" if path[-1] <= 1.0 else "#2ecc71"
                ax.plot(path, color=p_color, linewidth=2)
                ax.fill_between(range(len(path)), path, color=p_color, alpha=0.1)
                ax.set_yscale('log')
                ax.set_ylabel("Wealth (Log Scale)")
                ax.grid(True, which="both", ls="-", alpha=0.1)
                st.pyplot(fig)
                plt.close(fig)

                st.divider()
                st.write("#### Strategy Statistics (Batch of 100 Simulations)")
                c1, c2 = st.columns(2)
                c1.metric("Median Final Wealth", f"${res['Median']:,.0f}")
                c2.metric("Insolvency Rate", f"{res['Insolvency Rate']:.1%}")
