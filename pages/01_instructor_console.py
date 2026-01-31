import streamlit as st
import numpy as np
import pandas as pd
import time

# --- CONFIG & SECURITY ---
st.set_page_config(layout="wide", page_title="Market Master Console v6.5")
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
if 'sim_total_trials' not in st.session_state:
    st.session_state.sim_total_trials = 0
if 'sim_total_wins' not in st.session_state:
    st.session_state.sim_total_wins = {}

# --- 1. STRATEGY REGISTRATION ---
st.title("👨‍🏫 Teacher Console: Market Auctioneer")

with st.expander("📝 Register Student Cutoffs", expanded=(st.session_state.market_list is None)):
    if 'student_data' not in st.session_state:
        st.session_state.student_data = pd.DataFrame([
            {"Student": "Alice", "N": 37},
            {"Student": "Bob", "N": 10},
            {"Student": "Charlie", "N": 65},
            {"Student": "Diana", "N": 25}
        ])
    
    st.session_state.student_data = st.data_editor(
        st.session_state.student_data,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_v6_5"
    )

# --- 2. THE MANUAL REVEAL ENGINE ---
st.divider()
st.header("🏁 The Manual Reveal (Single Race)")

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

        status_list = []
        for _, row in df.iterrows():
            name = str(row["Student"])
            n = int(row["N"])
            benchmark = np.max(market[:n]) if n > 0 else 0
            
            if name in st.session_state.student_results:
                res = st.session_state.student_results[name]
                status = f"✅ BOOKED (Loc: #{res.get('Location')}, Val: {res.get('Value')}, Rank: {res.get('Rank')})"
            elif step <= n:
                status = f"🔍 Researching (Target: {np.max(market[:step]) if step > 0 else 0})"
            else:
                status = f"👀 Searching (Target: >{benchmark})"
            
            status_list.append({"Student": f"{name} (N={n})", "Status": status})

        st.table(pd.DataFrame(status_list))
    else:
        st.info("Market Ready.")

# --- 3. THE TRUTH ENGINE (LABELLED STRATEGIES) ---
st.divider()
st.header("🧪 The Truth Engine (Limit: 10,000 Trials)")

sim_col1, sim_col2, sim_col3 = st.columns([1, 1, 2])
remaining = max(0, 10000 - st.session_state.sim_total_trials)
batch_to_add = sim_col1.number_input("Trials to Add:", min_value=1, max_value=min(5000, remaining) if remaining > 0 else 1, value=min(100, remaining) if remaining > 0 else 1, step=10)

if remaining > 0:
    if sim_col2.button("🏁 Run Next Batch", use_container_width=True, type="primary"):
        df = st.session_state.student_data.copy()
        if len(df.columns) >= 2: df.columns = ["Student", "N"] + list(df.columns[2:])
        
        # We store simulation wins by name, but we will display name + (N=x)
        names, ns = df["Student"].tolist(), pd.to_numeric(df["N"]).fillna(0).astype(int).tolist()
        
        for name in names:
            if name not in st.session_state.sim_total_wins:
                st.session_state.sim_total_wins[name] = 0

        for _ in range(batch_to_add):
            for i, n in enumerate(ns):
                s = np.random.permutation(np.arange(1, 101))
                b = np.max(s[:n]) if n > 0 else 0
                p = s[-1]
                for v in s[n:]:
                    if v > b: p = v; break
                if p == 100:
                    st.session_state.sim_total_wins[names[i]] += 1
        
        st.session_state.sim_total_trials += batch_to_add
        st.rerun()
else:
    sim_col2.success("Simulation Complete!")

if sim_col3.button("🗑️ Reset Simulation Data", use_container_width=True):
    st.session_state.sim_total_trials = 0
    st.session_state.sim_total_wins = {}
    st.rerun()

if st.session_state.sim_total_trials > 0:
    res_data = []
    # Create a lookup for N values
    n_lookup = dict(zip(st.session_state.student_data["Student"], st.session_state.student_data["N"]))
    
    for name, wins in st.session_state.sim_total_wins.items():
        n_val = n_lookup.get(name, "?")
        res_data.append({
            "Label": f"{name} (N={n_val})",
            "Win Rate %": (wins / st.session_state.sim_total_trials) * 100
        })
    plot_df = pd.DataFrame(res_data).sort_values("Win Rate %", ascending=True)
    
    st.vega_lite_chart(plot_df, {
        "mark": {"type": "bar", "height": 18},
        "encoding": {
            "y": {"field": "Label", "type": "nominal", "sort": "-x", "title": ""},
            "x": {"field": "Win Rate %", "type": "quantitative", "scale": {"domain": [0, 100]}, "title": "Observed Win Rate (%)"},
            "color": {"field": "Label", "type": "nominal", "legend": None, "scale": {"scheme": "category20"}}
        }
    }, use_container_width=True)

# --- MARKET TRUTH ---
st.divider()
if st.session_state.market_list is not None:
    with st.expander("🕵️ Private Market Intel"):
        best_pos = np.where(st.session_state.market_list == 100)[0][0] + 1
        st.write(f"The #1 Venue is at Position: **{best_pos}**")

# --- SOURCE CODE PADDING ---
with st.sidebar:
    if st.button("Log Out"): st.session_state.authenticated = False; st.rerun()
    st.caption("Auctioneer Mode v6.5")

#
#
#
#
#
#
# --- END OF FILE ---
