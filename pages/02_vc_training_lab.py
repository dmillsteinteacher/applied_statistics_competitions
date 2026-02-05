import streamlit as st
import numpy as np

# --- 1. CONFIG & NARRATIVE DATA ---
st.set_page_config(page_title="VC Training Lab", layout="wide")

B_VALS = {"Type 1: The Basics": 0.5, "Type 2: Tech Apps": 2.0, "Type 3: Big Science": 8.0}

MKT_STORY = {
    "Market A: The Boom": "Consumer spending is at an all-time high and credit is nearly free. In this 'Goldilocks' economy, almost any well-run business can find a customer. The primary risk is over-expansion rather than insolvency.",
    "Market B: The Squeeze": "Inflation is rampant and store shelves are empty. This 'Stagflation' environment is punishing for companies with high overhead. Only the most efficient business models can survive the rising cost of capital.",
    "Market C: Rule Change": "The regulatory landscape has shifted. New government mandates have created massive tailwinds for specific green energy sectors while suddenly bankrupting traditional industrial players."
}

TYPE_STORY = {
    "Type 1: The Basics": "This fund focuses on 'Utility' plays: infrastructure, water, and power. These businesses are boring but essential, providing steady cash flows even during economic downturns.",
    "Type 2: Tech Apps": "This fund focuses on scalable platforms like social media and delivery. Competition is fierce, but the ability to grow at zero marginal cost offers significant upside if the company survives the initial burn.",
    "Type 3: Big Science": "This fund focuses on frontier technology: rocket engines, deep-sea mining, and experimental AI. These ventures face massive 'R&D' risk, but a single success can redefine an entire industry."
}

BASE_P = {
    "Market A: The Boom": {"Type 1: The Basics": 0.90, "Type 2: Tech Apps": 0.60, "Type 3: Big Science": 0.25},
    "Market B: The Squeeze": {"Type 1: The Basics": 0.70, "Type 2: Tech Apps": 0.35, "Type 3: Big Science": 0.08},
    "Market C: Rule Change": {"Type 1: The Basics": 0.80, "Type 2: Tech Apps": 0.45, "Type 3: Big Science": 0.15},
}

# --- 2. SESSION STATE ---
for k in ["lab_id", "p_matrix", "cur_scen", "audit", "verified", "history"]:
    if k not in st.session_state: st.session_state[k] = "" if k=="lab_id" else [] if k=="history" else None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("👨‍💼 VC Research Desk")
    id_in = st.text_input("Enter Lab ID:", value=st.session_state.lab_id)
    if id_in != st.session_state.lab_id:
        st.session_state.lab_id = id_in
        np.random.seed(sum(ord(c) for c in id_in))
        st.session_state.p_matrix = {m: {t: np.clip(p + np.random.normal(0, 0.02), 0.01, 0.99) for t, p in d.items()} for m, d in BASE_P.items()}
        st.session_state.audit, st.session_state.verified, st.session_state.history = None, False, []

    if st.session_state.lab_id:
        m_sel = st.selectbox("Market Environment", list(BASE_P.keys()))
        t_sel = st.selectbox("Fund Type", list(B_VALS.keys()))
        if st.button("Open Research Lab"):
            st.session_state.cur_scen = (m_sel, t_sel)
            st.session_state.audit, st.session_state.verified, st.session_state.history = None, False, []

# --- 4. MAIN INTERFACE ---
if not st.session_state.lab_id:
    st.warning("⚠️ Access Denied: Please enter your Lab ID in the sidebar to begin.")
elif not st.session_state.cur_scen:
    st.info("Select a Market and Fund Type in the sidebar to open the Research Lab.")
else:
    mkt, f_typ = st.session_state.cur_scen
    p_true, b = st.session_state.p_matrix[mkt][f_typ], B_VALS[f_typ]
    
    with st.expander("📄 Intelligence Briefing", expanded=True):
        col1, col2 = st.columns(2)
        col1.write(f"**Market Conditions:**\n\n*{MKT_STORY[mkt]}*")
        col2.write(f"**Sector Profile:**\n\n*{TYPE_STORY[f_typ]}*")
        st.markdown(f"**Payout Terms:** Successful exits yield a **{b}x profit multiple** on capital deployed.")

    t1, t2, t3 = st.tabs(["Stage 1: The Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with t1:
        st.subheader("Stage 1: Forensic Probability Discovery")
        if st.button("Request Internal Audit Report"):
            np.random.seed(sum(ord(c) for c in st.session_state.lab_id + mkt + f_typ))
            w = sum(1 for _ in range(50) if np.random.random() < p_true)
            st.session_state.audit = {"w": w, "ef": int((50-w)*.4), "mf": (50-w)-int((50-w)*.4), "p": w/50}
            st.session_state.verified = False

        if st.session_state.audit:
            r = st.session_state.audit
            st.info("### 🕵️ CONFIDENTIAL MEMO: Internal Sector Audit")
            st.markdown(f"""
            **To:** Managing Partner | **From:** Risk Assessment Division | **Subject:** Review of 50 Sample Ventures

            Our team has concluded its investigation into the last 50 ventures launched within this specific sector and market cycle.

            **Findings:**
            * **Execution Failures:** We identified that **{r['ef']} companies** suffered from fatal internal mismanagement and inability to scale operational staff.
            * **Market Casualties:** An additional **{r['mf']} ventures** were liquidated following unexpected competitive shifts and rising material costs.
            * **Successful Exits:** The remaining companies hit their target exit milestones.

            Establish the success probability ($p$) for our upcoming rounds based on this sample.
            """)
            u_p = st.number_input("Determine Win Probability (p):", 0.0, 1.0, step=0.01, format="%.2f")
            if st.button("Verify Findings"):
                if abs(u_p - r
