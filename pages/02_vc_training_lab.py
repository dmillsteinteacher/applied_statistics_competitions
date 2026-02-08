import streamlit as st
from pathlib import Path
import importlib.util
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. SET PAGE CONFIG (MUST BE ABSOLUTE FIRST) ---
if "config_set" not in st.session_state:
    try:
        st.set_page_config(page_title="VC Training Lab", layout="wide")
        st.session_state.config_set = True
    except:
        pass

# --- 2. MODULE LOADING ---
def load_mod(name):
    current_dir = Path(__file__).parent
    root_dir = current_dir.parent
    path = root_dir / name
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

nav = load_mod("02_vc_lab_narrative.py")
eng = load_mod("02_vc_lab_engine.py")

if nav is None or eng is None:
    st.error("❌ Critical Error: Could not load Narrative or Engine files.")
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
            st.info(nav.MEMO_TEMPLATE.format(n=r['n'], ef=r['ef'], mf=r['mf'], sector=sec, market=mkt))
            u_p = st.number_input("Enter your calculated Success Rate (p):", 0.0, 1.0, step=0.001, format="%.3f")
            if st.button("Verify Audit"):
                if abs(u_p - r['p_observed']) < 0.005:
                    st.session_state.verified = True
                    st.success(f"✅ Verified. Research confirms p = {r['p_observed']:.3f}")
                else: 
                    st.error("❌ Verification failed. Check your math: (Total Cases - Failures) / Total Cases.")

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
        st.subheader("Stage 3: Sizing & Capital Deployment")
        if not st.session_state.history: 
            st.warning("🔒 Complete Stage 2 to unlock capital deployment.")
        else:
            # 1. Setup context from previous stages
            p_val = st.session_state.audit['p_observed']
            st.markdown(f"**Research Confidence (p):** {p_val:.3f} | **Payback Multiplier (b):** {b}x")
            
            # 2. Input for Sizing (The 'f' decision)
            f = st.slider("Investment Size (f) per deal", 0.0, 1.0, 0.1, 0.01, 
                         help="What percentage of your current fund do you deploy into every single deal?")
            
            # 3. Execution - One Trial per Click
            if st.button("🚀 Run 50-Deal Simulation"):
                path = eng.run_simulation(f, p_val, b)
                
                st.write(f"#### Fund Journey (1 Trial)")
                fig, ax = plt.subplots(figsize=(10, 4))
                
                # Visual threshold: Green if ending above start, Red if below
                line_color = "#2ecc71" if path[-1] > 100 else "#e74c3c"
                
                # LINEAR PLOT (Visceral discovery of swings)
                ax.plot(path, color=line_color, linewidth=2, label="Fund Value")
                
                # THE $100 REFERENCE LINE
                ax.axhline(100, color="gray", linestyle="--", alpha=0.6, label="Starting Capital ($100)")
                
                # Formatting
                ax.set_ylabel("Wealth ($)")
                ax.set_xlabel("Number of Deals")
                ax.set_title(f"Final Value: ${path[-1]:,.2f}")
                ax.grid(True, axis='y', alpha=0.2)
                ax.legend()
                
                st.pyplot(fig)
                plt.close(fig)

                # 4. Metrics for discovery of risk
                c1, c2, c3 = st.columns(3)
                c1.metric("Peak Wealth", f"${np.max(path):,.2f}")
                c2.metric("Trough (Max Pain)", f"${np.min(path):,.2f}")
                c3.metric("Final Result", f"${path[-1]:,.2f}")
                
                # 5. Pedagogical feedback
                if path[-1] <= 1.0:
                    st.error("💥 **INSOLVENT:** Your fund hit the floor. In this universe, your sizing was too aggressive for the sequence of outcomes.")
                elif path[-1] < 100:
                    st.warning("📉 **UNDERWATER:** You survived, but you finished with less than your starting capital.")
                else:
                    st.success("💰 **SUCCESS:** Your deployment strategy resulted in net growth.")

# --- FINAL PADDING FOR PEDAGOGICAL INTEGRITY ---
# ............................................................................
# ............................................................................
# ............................................................................
# ............................................................................
# ............................................................................
# ............................................................................
# ............................................................................
# ............................................................................
# ............................................................................
# ............................................................................
# ............................................................................
# ............................................................................
# --- END OF FILE ---
