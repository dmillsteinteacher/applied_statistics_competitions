import streamlit as st
import importlib.util
import os
import numpy as np
import pandas as pd

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="VC Training Lab", layout="wide")

# --- 2. MODULE LOADING ---
@st.cache_resource
def load_mod(name):
    path = os.path.join(os.path.dirname(__file__), name)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

nav = load_mod("02_vc_lab_narrative.py")
eng = load_mod("02_vc_lab_engine.py")

# --- 3. SESSION STATE ---
for k in ["lab_id", "p_matrix", "cur_scen", "audit", "verified", "history"]:
    if k not in st.session_state:
        st.session_state[k] = "" if k == "lab_id" else [] if k == "history" else None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("👨‍💼 VC Research Desk")
    id_in = st.text_input("Enter Lab ID:", value=st.session_state.lab_id)
    
    if id_in != st.session_state.lab_id:
        st.session_state.lab_id = id_in
        np.random.seed(sum(ord(c) for c in id_in))
        m_base = {"Market A: The Boom": 0.9, "Market B: The Squeeze": 0.7, "Market C: Rule Change": 0.8}
        s_mult = {"Type 1: The Basics": 1.0, "Type 2: Tech Apps": 0.6, "Type 3: Big Science": 0.2}
        st.session_state.p_matrix = {m: {s: np.clip(p*s_mult[s] + np.random.normal(0,0.02), 0.01, 0.99) 
                                       for s in nav.TYPE_STORY} for m, p in m_base.items()}
        st.session_state.audit, st.session_state.verified, st.session_state.history = None, False, []

    if st.session_state.lab_id:
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
if not st.session_state.lab_id or not st.session_state.cur_scen:
    st.info("👋 Welcome. Enter a Lab ID and select a scenario in the sidebar to begin.")
else:
    mkt, sec = st.session_state.cur_scen
    p_true = st.session_state.p_matrix[mkt][sec]
    b = nav.B_VALS[sec]
    
    with st.expander("📄 Intelligence Briefing", expanded=True):
        st.write(f"**Current Context:** {nav.MARKET_STORIES[mkt]}")
        st.write(f"**Sector Profile:** {nav.TYPE_STORY[sec]}")
        st.write(f"**Payout Terms:** Success yields a **{b}x** multiple on investment.")

    t1, t2, t3 = st.tabs(["Stage 1: Audit", "Stage 2: Stress Test", "Stage 3: Sizing"])
    
    with t1:
        if st.button("Request Audit Report"):
            st.session_state.audit = eng.run_audit(st.session_state.lab_id, mkt, sec, p_true)
            st.session_state.verified = False
        
        if st.session_state.audit:
            r = st.session_state.audit
            # THE CRITICAL FIX IS HERE:
            st.info(nav.MEMO_TEMPLATE.format(
                ef=r['exec_fail'], 
                mf=r['mkt_fail'], 
                sector=sec, 
                market=mkt
            ))
            u_p = st.number_input("Enter the calculated p (Success Rate):", 0.0, 1.0, step=0.01)
            if st.button("Verify Audit"):
                if abs(u_p - r['p_observed']) < 0.001:
                    st.session_state.verified = True
                    st.success(f"Verified. Observed p = {r['p_observed']:.2f}")
                else: st.error("Verification failed.")

    with t2:
        if not st.session_state.verified: st.warning("🔒 Please verify Stage 1.")
        else:
            if st.button("Simulate 100-Deal Career"):
                st.session_state.history.append(eng.simulate_career(st.session_state.audit['p_observed']))
            if st.session_state.history:
                lt = st.session_state.history[-1]
                m_col1, m_col2 = st.columns(2)
                m_col1.metric("Wins", f"{lt['Wins']}/100")
                m_col2.metric("Longest Loss Streak", f"{lt['Max_Streak']}")
                st.write("### Sequence of Outcomes")
                st.write(" ".join(["🟩" if x else "🟥" for x in lt['raw']]))
                st.table([{"Run": i+1, "Wins": h['Wins'], "Max Loss Streak": h['Max_Streak']} for i, h in enumerate(st.session_state.history)])

    with t3:
        if not st.session_state.history: st.warning("🔒 Complete Stage 2.")
        else:
            f = st.slider("Investment Size (f) as % of Remaining Fund", 0.0, 1.0, 0.1)
            if st.button("Deploy Capital"):
                bal, hst, fail = eng.run_fund_simulation(f, st.session_state.audit['p_observed'], b)
                st.write(f"### Final Fund Value: ${bal:,.2f}")
                if fail: st.error("🚨 FUND INSOLVENT")
                chart_df = pd.DataFrame(hst, columns=["Portfolio Value"])
                st.line_chart(chart_df)
                st.caption("Y-Axis: Portfolio Value ($) | X-Axis: Investment Round (0-50)")

# --- SAFETY PADDING ---
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
# --- END OF FILE ---
