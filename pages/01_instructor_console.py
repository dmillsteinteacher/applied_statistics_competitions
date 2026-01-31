import streamlit as st
import numpy as np
import pandas as pd
import time

# --- CONFIG & SECURITY ---
st.set_page_config(layout="wide", page_title="Teacher Console v4.2")
MASTER_PASSWORD = "admin_stats_2026" 

# --- AUTHENTICATION GATE ---
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

# --- 1. STRATEGY REGISTRATION ---
st.title("👨‍🏫 Teacher Console: Command Center")

with st.expander("📝 Register Student Cutoffs", expanded=True):
    if 'student_data' not in st.session_state:
        st.session_state.student_data = pd.DataFrame([
            {"Student": "Alice (Optimal)", "N": 37},
            {"Student": "Bob (Aggressive)", "N": 10},
            {"Student": "Charlie (Cautious)", "N": 65}
        ])
    
    st.session_state.student_data = st.data_editor(
        st.session_state.student_data,
        num_rows="dynamic",
        use_container_width=True,
        key="strategy_editor_v4_2",
        column_config={
            "Student": st.column_config.TextColumn("Student", required=True),
            "N": st.column_config.NumberColumn("N", min_value=0, max_value=100, step=1, required=True)
        }
    )

def get_clean_data():
    df = st.session_state.student_data.copy()
    if len(df.columns) >= 2:
        df.columns = ["Student", "N"] + list(df.columns[2:])
    return df

# --- 2. THE DRAMA ENGINE: RE-ENGINEERED ---
st.divider()
st.header("🏁 The Drama Engine: Live Market Ticker")

if st.button("🚀 Start Live Ticker Race"):
    df = get_clean_data()
    market = np.random.permutation(np.arange(1, 101))
    best_at = np.where(market == 100)[0][0] + 1
    
    # Static UI layout to prevent scrolling
    m1, m2, m3 = st.columns(3)
    ticker_metric = m1.empty()
    best_loc_metric = m2.empty()
    winner_announcement = m3.empty()
    
    # This is the key: One single placeholder for the entire leaderboard
    leaderboard_placeholder = st.empty()
    
    names = df["Student"].astype(str).tolist()
    ns = pd.to_numeric(df["N"], errors='coerce').fillna(0).astype(int).tolist()
    
    # Initialize state
    results = {name: {"status": "🔍 Researching", "val": 0, "pos": 0, "done": False} for name in names}
    benchmarks = {names[i]: (np.max(market[:ns[i]]) if ns[i] > 0 else 0) for i in range(len(names))}

    for t in range(1, 101):
        curr_val = market[t-1]
        
        # 1. Update Top Metrics
        ticker_metric.metric("Venue Position", f"#{t}", f"Value: {curr_val}")
        best_loc_metric.write(f"**Target #100 Location:** Venue {best_at}")
        
        # 2. Update Logic for each student
        for i, name in enumerate(names):
            if not results[name]["done"]:
                if t <= ns[i]:
                    results[name]["status"] = f"🔍 Researching (Target: >{benchmarks[name]})"
                else:
                    if curr_val > benchmarks[name] or t == 100:
                        results[name]["done"] = True
                        results[name]["val"] = curr_val
                        results[name]["pos"] = t
                        results[name]["status"] = f"✅ BOOKED at #{t} (Rank {101-curr_val})"
                        if curr_val == 100:
                            winner_announcement.success(f"🏆 {name} HIT THE #1!")
                    else:
                        results[name]["status"] = f"👀 Searching (Benchmark: {benchmarks[name]})"

        # 3. Render the leaderboard as a clean table (no scrolling)
        display_df = pd.DataFrame([
            {"Student": name, "Current Status": results[name]["status"]} 
            for name in names
        ])
        leaderboard_placeholder.table(display_df)
        
        time.sleep(0.08)
    
    if any(res["val"] == 100 for res in results.values()):
        st.balloons()

# --- 3. THE TRUTH ENGINE (UNCHANGED BUT ROBUST) ---
st.divider()
st.header("🧪 The Truth Engine: 2,000-Trial Shuffle Race")

if st.button("📊 Start Convergence Race"):
    df = get_clean_data()
    names = df["Student"].astype(str).tolist()
    ns = pd.to_numeric(df["N"], errors='coerce').fillna(0).astype(int).tolist()
    wins = np.zeros(len(names))
    
    chart_holder = st.empty()
    
    for trial in range(40, 2040, 40):
        for i, n in enumerate(ns):
            for _ in range(40):
                s = np.random.permutation(np.arange(1, 101))
                b = np.max(s[:n]) if n > 0 else 0
                p = s[-1]
                for v in s[n:]:
                    if v > b:
                        p = v
                        break
                if p == 100: wins[i] += 1
        
        plot_df = pd.DataFrame({"Student": names, "Win Rate %": (wins/trial)*100}).sort_values("Win Rate %", ascending=True)
        chart_holder.bar_chart(plot_df.set_index("Student"), use_container_width=True)
        time.sleep(0.02)

# --- SIDEBAR ---
with st.sidebar:
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()
    st.caption("v4.2 | Clean UI Edition")
