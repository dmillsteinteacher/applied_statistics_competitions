import streamlit as st
import numpy as np
from 02_vc_lab_narrative import B_VALS, MARKET_STORIES, TYPE_STORY, MEMO_TEMPLATE

st.set_page_config(page_title="VC Training Lab", layout="wide")

# --- INITIALIZATION ---
for k in ["lab_id", "p_matrix", "cur_scen", "audit", "verified", "history"]:
    if k not in st.session_state: st.session_state[k] = "" if k=="lab_id" else [] if k=="history" else None

# --- SIDEBAR ---
with st.sidebar:
    st.title("👨‍💼 VC Research Desk")
    id_in = st.text_input("Enter Lab ID:", value=st.session_state.lab_id)
    if id_in != st.session_state.lab_id:
        st.session_state.lab_id = id_in
        np.random.seed(sum(ord(c) for c in id_in))
        base_p = {"Market A: The Boom": 0.9, "Market B: The Squeeze": 0.7, "Market C: Rule Change": 0.8}
        type_p = {"Type 1: The Basics": 1.0, "Type 2: Tech Apps": 0.6, "Type 3: Big Science": 0.2}
        st.session_state.p_matrix = {m: {t: np.clip(p_m*type_p[t] + np.random.normal(0, 0.02), 0.01, 0.99) for t in TYPE_STORY} for m, p_m in base_p.items()}
        st.session_state.audit, st.session_state.verified, st.session_state.history = None, False, []

    if st.session_state.lab_id:
        m_sel = st.selectbox("Market", list(MARKET_STORIES.keys()))
        t_sel = st.selectbox("Sector", list(TYPE_STORY.keys()))
        if st.button("Open Research Lab"):
            st.session_state.cur_scen = (m_sel, t_sel)
            st.session_state.audit, st.session_state.verified, st.session_state.history = None, False, []

# --- MAIN INTERFACE ---
if not st.session_state.lab_id or not st.session_state.cur_scen:
    st.info("Initialize Lab ID and select a scenario in the sidebar.")
else:
    mkt, f_typ = st.session_state.cur_scen
    p_true, b = st.session_state.p_matrix[mkt][f_typ], B_VALS[f_typ]
    
    with st.expander("📄 Intelligence Briefing", expanded=True):
        c1, c2 = st.columns(2)
        c1.write(f"**Market:** {MARKET_STORIES[mkt]}")
        c2.write(f"**Sector:** {TYPE_STORY[f_typ]}")
        st.write(f"**Terms:** Successful exits yield a **{b}x** profit multiple.")

    t1, t2, t3 = st.tabs(["Stage 1: Audit", "Stage 2: Stress Test", "Stage 3: Calibration"])
    
    with t1:
        if st.button("Request Audit Report"):
            np.random.seed(sum(ord(c) for c in st.session_state.lab_id + mkt + f_typ))
            w = sum(1 for _ in range(50) if np.random.random() < p_true)
            st.session_state.audit = {"w": w, "ef": int((50-w)*.4), "mf": (50-w)-int((50-w)*.4), "p": w/50}
        
        if st.session_state.audit:
            r = st.session_state.audit
            st.info(MEMO_TEMPLATE.format(ef=r['ef'], mf=r['mf']))
            u_p = st.number_input("Probability (p):", 0.0, 1.0, step=0.01)
            if st.button("Verify"):
                if abs(u_p - r['p']) < 0.001:
                    st.session_state.verified = True
                    st.success("Verified.")
                else: st.error("Mismatch.")

    with t2:
        if not st.session_state.verified: st.info("🔒 Verify Stage 1.")
        else:
            if st.button("Simulate 100-Deal Career"):
                res = ["SUCCESS" if np.random.random() < st.session_state.audit['p'] else "FAILURE" for _ in range(100)]
                cur, mx = 0, 0
                for x in res:
                    cur = cur + 1 if x == "FAILURE" else 0
                    mx = max(mx, cur)
                st.session_state.history.append({"w": res.count("SUCCESS"), "s": mx, "raw": res})
            
            if st.session_state.history:
                lt = st.session_state.history[-1]
                st.metric("Wins", f"{lt['w']}/100"), st.metric("Max Streak", f"{lt['s']} Losses")
                st.write(" ".join(["🟩" if x=="SUCCESS" else "🟥" for x in lt['raw']]))
                st.table([{"Career #": i+1, "Wins": h['w'], "Streak": h['s']} for i, h in enumerate(st.session_state.history)])

    with t3:
        if not st.session_state.history: st.info("🔒 Complete Stage 2.")
        else:
            f = st.slider("Investment Size (f)", 0.0, 1.0, 0.1)
            if st.button("Run Simulation"):
                bal, hist, fail = 1000.0, [1000.0], False
                for _ in range(50):
                    if bal < 1.0: fail, bal = True, 0
                    else:
                        bet = bal * f
                        bal += (bet * b) if np.random.random() < st.session_state.audit['p'] else -bet
                    hist.append(bal)
                st.write(f"### Final: ${bal:,.2f}")
                if fail: st.error("INSOLVENT")
                st.line_chart(hist)

# --- PADDING ---
# 
# 
# 
# 
# 
# 
# 
# 
# --- END OF FILE ---
