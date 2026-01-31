import streamlit as st
import numpy as np
import pandas as pd

# --- CONFIG & SECURITY ---
st.set_page_config(layout="wide", page_title="Market Master Console v5.5")
MASTER_PASSWORD = "admin_stats_2026" 

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Market Master Login")
    pwd = st.text_input("Enter Teacher Password:", type="password")
    if st.button("Unlock Console"):
        if pwd == MASTER_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# --- INITIALIZE SESSION STATE ---
if 'market_list' not in st.session_state:
    st.session_state.market_list = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'student_results' not in st.session_state:
    st.session_state.student_results = {}

# --- 1. STRATEGY REGISTRATION ---
st.title("👨‍🏫 Teacher Console: Market Auctioneer")

with st.expander("📝 Register Student Cutoffs", expanded=(st.session_state.market_list is None)):
    if 'student_data' not in st.session_state:
        st.session_state.student_data = pd.DataFrame([
            {"Student": "Alice", "N": 37},
            {"Student": "Bob", "N": 10},
            {"Student": "Charlie", "N": 65}
        ])
    
    st.session_state.student_data = st.data_editor(
        st.session_state.student_data,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_v5_5"
    )

# --- 2. THE MANUAL REVEAL ENGINE ---
st.divider()
st.header("🏁 The Manual Reveal")

col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns([1, 1, 1, 1])

if col_ctrl1.button("🎲 Generate New Market", use_container_width=True):
    st.session_state.market_list = np.random.permutation(np.arange(1, 101))
    st.session_state.current_step = 0
    st.session_state.student_results = {}
    st.rerun()

if st.session_state.market_list is not None:
    if st.session_state.current_step < 100:
        if col_ctrl2.button("➡️ Next Venue", type="primary", use_container_width=True):
            st.session_state.current_step += 1
            st.rerun()
            
        if col_ctrl3.button("⏩ Fast Forward", use_container_width=True):
            st.session_state.current_step = 100
            st.rerun()
    
    if col_ctrl4.button("🔄 Reset This Reveal", use_container_width=True):
        st.session_state.current_step = 0
        st.session_state.student_results = {}
        st.rerun()

    m1, m2, m3 = st.columns(3)
    step = st.session_state.current_step
    market = st.session_state.market_list

    if step > 0:
        curr_val = market[step-1]
        m1.metric("Current Venue", f"#{step}")
        m2.metric("Venue Value", f"{curr_val}")
        
        df = st.session_state.student_data.copy()
        if len(df.columns) >= 2:
            df.columns = ["Student", "N"] + list(df.columns[2:])
        
        # PROCESS LOGIC: Catch up all students to the current step
        for s_idx in range(1, step + 1):
            val_at_s = market[s_idx-1]
            for _, row in df.iterrows():
                name = str(row["Student"])
                n = int(row["N"])
                
                if name not in st.session_state.student_results:
                    benchmark = np.max(market[:n]) if n > 0 else 0
                    if s_idx > n:
                        if val_at_s > benchmark or s_idx == 100:
                            st.session_state.student_results[name] = {
                                "Location": int(s_idx), 
                                "Value": int(val_at_s), 
                                "Rank": int(101 - val_at_s)
                            }

        # BUILD DISPLAY TABLE (Safely handle missing keys with .get)
        status_list = []
        for _, row in df.iterrows():
            name = str(row["Student"])
            n = int(row["N"])
            benchmark = np.max(market[:n]) if n > 0 else 0
            
            if name in st.session_state.student_results:
                res = st.session_state.student_results[name]
                loc = res.get("Location", "N/A")
                val = res.get("Value", "N/A")
                rnk = res.get("Rank", "N/A")
                status = f"✅ BOOKED (Loc: #{loc}, Val: {val}, Rank: {rnk})"
            elif step <= n:
                status = f"🔍 Researching (Benchmark: {np.max(market[:step]) if step > 0 else 0})"
            else:
                status = f"👀 Searching (Target: >{benchmark})"
            
            status_list.append({"Student": name, "Status": status})

        st.table(pd.DataFrame(status_list))
    else:
        st.info("Market Ready. Click 'Next Venue' or 'Fast Forward' to begin.")

# --- 3. POST-RACE SUMMARY ---
if st.session_state.current_step == 100:
    st.divider()
    st.header("📊 Post-Race Summary")
    winners = [name for name, res in st.session_state.student_results.items() if res.get("Rank") == 1]
    
    if winners:
        st.success(f"🏆 Winners who found the #1 Venue: {', '.join(winners)}")
    else:
        st.warning("📉 No one found the #1 Venue this round.")
    
    summary_df = pd.DataFrame.from_dict(st.session_state.student_results, orient='index').reset_index()
    if not summary_df.empty:
        summary_df.columns = ["Student", "Location", "Value", "Rank"]
        st.dataframe(summary_df.sort_values("Rank"), use_container_width=True)

# --- 4. THE TRUTH ENGINE ---
st.divider()
st.header("🧪 The Truth Engine (2,000 Trials)")
if st.button("📊 Run Simulation Race"):
    df = st.session_state.student_data.copy()
    if len(df.columns) >= 2: df.columns = ["Student", "N"] + list(df.columns[2:])
    names, ns = df["Student"].tolist(), pd.to_numeric(df["N"]).fillna(0).astype(int).tolist()
    wins = np.zeros(len(names))
    
    chart_holder = st.empty()
    for trial in range(40, 2040, 40):
        for i, n in enumerate(ns):
            for _ in range(40):
                s = np.random.permutation(np.arange(1, 101))
                b = np.max(s[:n]) if n > 0 else 0
                p = s[-1]
                for v in s[n:]:
                    if v > b: p = v; break
                if p == 100: wins[i] += 1
        
        plot_df = pd.DataFrame({"Student": names, "Win Rate %": (wins/trial)*100}).sort_values("Win Rate %")
        chart_holder.bar_chart(plot_df.set_index("Student"))

# --- MARKET TRUTH ---
if st.session_state.market_list is not None:
    with st.expander("🕵️ Private Market Intel"):
        best_pos = np.where(st.session_state.market_list == 100)[0][0] + 1
        st.write(f"The #1 Venue is at Position: **{best_pos}**")

# --- SOURCE CODE PADDING ---
with st.sidebar:
    if st.button("Log Out"): st.session_state.authenticated = False; st.rerun()
    st.caption("Auctioneer Mode v5.5")

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# --- END OF FILE ---
