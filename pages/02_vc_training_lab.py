import streamlit as st
import numpy as np
import importlib.util
import os

# --- DYNAMIC IMPORT FOR NUMBERED FILENAMES ---
# This pulls data from your 02_vc_lab_narrative.py file
try:
    spec = importlib.util.spec_from_file_location(
        "narrative_module", 
        os.path.join(os.path.dirname(__file__), "02_vc_lab_narrative.py")
    )
    narrative = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(narrative)
    
    B_VALS = narrative.B_VALS
    MARKET_STORIES = narrative.MARKET_STORIES
    TYPE_STORY = narrative.TYPE_STORY
    MEMO_TEMPLATE = narrative.MEMO_TEMPLATE
except Exception as e:
    st.error(f"Failed to load narrative file: {e}")
    st.stop()

st.set_page_config(page_title="VC Training Lab", layout="wide")

# --- INITIALIZATION ---
for k in ["lab_id", "p_matrix", "cur_scen", "audit", "verified", "history"]:
    if k not in st.session_state: 
        st.session_state[k] = "" if k=="lab_id" else [] if k=="history" else None

# --- SIDEBAR ---
with st.sidebar:
    st.title("👨‍💼 VC Research Desk")
    id_in = st.text_input("Enter Lab ID:", value=st.session_state.lab_id)
    if id_in != st.session_state.lab_id:
        st.session_state.lab_id = id_in
        np.random.seed(sum(ord(c) for c in id_in))
        # Logic seeds for specific market/sector success rates
        base_p = {"Market A: The Boom": 0.9, "Market B: The Squeeze": 0.7, "Market C: Rule Change": 0.8}
        type_p = {"Type 1: The Basics": 1.0, "Type 2: Tech Apps": 0.6, "Type 3: Big Science": 0.2}
        st.session_state.p_matrix = {m: {t: np.clip(p_m*type_p[t] + np.random.normal(0, 0.02), 0.01, 0.99) for t in TYPE_STORY} for m, p_m in base_p.items()}
        st.session_state.audit, st.session_state.verified, st.session_state.history = None, False, []

    if st.session_state.lab_id:
        st.divider()
        m_sel = st.selectbox("Market Environment", list(MARKET_STORIES.keys()))
        t_sel = st.selectbox("Sector Type", list(TYPE_STORY.keys()))
        if st.button("Open Research Lab"):
            st.session_state.cur_scen = (m_sel, t_sel)
            st.session_state.audit, st.session_state.verified, st.session_state.history = None, False, []

# --- MAIN INTERFACE ---
if not st.session_state.lab_id or not st.session_state.cur_scen:
    st.info("Please initialize your Lab ID and select a scenario in the sidebar to begin.")
else:
    mkt, f_typ = st.session_state.cur_scen
    p_true, b = st.session_state.p_matrix[mkt][f_typ], B_VALS[f_typ]
    
    with st.expander("📄 Intelligence Briefing", expanded=True):
        c1, c2 = st.columns(2)
        c1.write(f"**Market Context:**\n\n{MARKET_STORIES[mkt]}")
        c2.write(f"**Sector Profile:**\n\n{TYPE_STORY[f_typ]}")
        st.write(f"**Payout Terms:** Success yields a **{b}x** multiple on deployed capital.")

    t1, t2, t3 = st.tabs(["Stage 1: Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with t1:
        st.subheader("Stage 1: Forensic Probability Discovery")
        if st.button("Request Internal Audit Report"):
            np.random.seed(sum(ord(c) for c in st.session_state.lab_id + mkt + f_typ))
            w = sum(1 for _ in range(50) if np.random.random() < p_true)
            st.session_state.audit = {"w": w, "ef": int((50-w)*.4), "mf": (50-w)-int((50-w)*.4), "p": w/50}
            st.session_state.verified = False
        
        if st.session_state.audit:
            r = st.session_state.audit
            st.info(MEMO_TEMPLATE.format(ef=r['ef'], mf=r['mf']))
            u_p = st.number_input("Based on the Audit, what is $p$?", 0.0, 1.0, step=0.01)
            if st.button("Verify Findings"):
                if abs(u_p - r['p']) < 0.001:
                    st.session_state.verified = True
                    st.success(f"Audit Verified. Fundamental p = {r['p']:.2f}.")
                else: st.error("Verification failed: Data mismatch
