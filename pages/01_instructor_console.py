import streamlit as st
import numpy as np
import pandas as pd
import time

# --- CONFIG & SECURITY ---
st.set_page_config(layout="wide", page_title="Teacher Console v4.0")
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

# --- APP LAYOUT ---
st.title("👨‍🏫 Teacher Console: Command Center (v4.0)")

# --- 1. STRATEGY REGISTRATION ---
with st.expander("📝 Register Student Cutoffs", expanded=True):
    if 'student_data' not in st.session_state:
        # Standardizing on "Student" to prevent KeyErrors
        st.session_state.student_data = pd.DataFrame([
            {"Student": "Alice (Optimal)", "N": 37},
            {"Student": "Bob (Aggressive)", "N": 10},
            {"Student": "Charlie (Cautious)", "N": 65}
        ])
    
    # We use a static key to ensure the editor doesn't lose state on rerun
    st.session_state.student_data = st.data_editor(
        st.session_state.student_data,
        num_rows="dynamic",
        use_container_width=True,
        key="strategy_editor_v4"
    )

# --- 2. THE DRAMA ENGINE: THE TICKER ---
st.divider()
st.header("🏁 The Drama Engine: Live Market Ticker")
st.caption("Step-by-step reveal of 100 venues. Watch the students 'Leap' in real-time.")

if st.button("🚀 Start Live Ticker Race"):
    # Re-fetch the dataframe to ensure we have the latest edits
    df = st.session_state.student_data
    
    if "Student" not in df.columns or "N" not in df.columns:
        st.error("Error: Ensure columns are named 'Student' and 'N'.")
        st.stop()

    market = np.random.permutation(np.arange(1, 101))
    best_at = np.where(market == 100)[0][0] + 1
    
    ticker_col, info_col = st.columns([1, 2])
    ticker_metric = ticker_col.empty()
    market_truth = info_col.empty()
    
    status_container = st.container()
    
    names = df["Student"].tolist()
    ns = df["N"].fillna(0).astype(int).tolist()
    
    results = {name: {"booked": False, "val": 0, "pos": 0} for name in names}
    
    # Pre-calculate benchmarks based on the Research Phase (N) for each student
    benchmarks = {}
    for i, name in enumerate(names):
        cutoff = ns[i]
        benchmarks[name] = np.max(market[:cutoff]) if cutoff > 0 else 0

    for t in range(1, 101):
        curr_val = market[t-1]
        
        # Update Ticker Display
        ticker_metric.metric("Current Venue Position", f"#{t}", f"Value: {curr_val}")
        market_truth.info(f"The Best Venue (#100) is hidden at Position: **{best_at}**")
        
        # Update Individual Statuses in a grid
        with status_container:
            # Create a flexible grid based on student count
            cols = st.columns(3)
            for i, name in enumerate(names):
                col = cols[i % 3]
                n = ns[i]
                
                if results[name]["booked"]:
                    icon = "🏆" if results[name]["val"] == 100 else "💼"
                    col.markdown(f"**{icon} {name}** \nBooked: Rank #{101 - results[name]['val']} (Pos {results[name]['pos']})")
                elif t <= n:
                    col.markdown(f"**🔍 {name}** \nResearching... (N={n})")
                else:
                    if curr_val > benchmarks[name] or t == 100:
                        results[name]["booked"] = True
                        results[name]["val"] = curr_val
                        results[name]["pos"] = t
                        col.success(f"**⚡ {name} LEAPED!** \nVenue #{t} | Val: {curr_val}")
                    else:
                        col.warning(f"**👀 {name}** \nSearching...")
        
        time.sleep(0.1) 
    
    if any(res["val"] == 100 for res in results.values()):
        st.balloons()

# --- 3. THE TRUTH ENGINE: THE SHUFFLE RACE ---
st.divider()
st.header("🧪 The Truth Engine: 2,000-Trial Shuffle Race")
st.caption("Auto-sorting bar chart updating every 40 trials to show statistical convergence.")

if st.button("📊 Start Convergence Race"):
    df = st.session_state.student_data
    if "Student" not in df.columns:
        st.error("Error: 'Student' column missing.")
        st.stop()

    TOTAL_TRIALS = 2000
    BATCH_SIZE = 40
    
    names = df["Student"].tolist()
    ns = df["N"].fillna(0).astype(int).tolist()
    wins = np.zeros(len(names))
    
    progress_bar = st.progress(0)
    chart_holder = st.empty()
    
    for trial in range(BATCH_SIZE, TOTAL_TRIALS + BATCH_SIZE, BATCH_SIZE):
        # Optimized Simulation Batch
        for i, n in enumerate(ns):
            for _ in range(BATCH_SIZE):
                s = np.random.permutation(np.arange(1, 101))
                b = np.max(s[:n]) if n > 0 else 0
                p = s[-1]
                for v in s[n:]:
                    if v > b:
                        p = v
                        break
                if p == 100:
                    wins[i] += 1
        
        # Win rates for current batch
        wr = (wins / trial) * 100
        plot_df = pd.DataFrame({
            "Student": names,
            "Win Rate %": wr
        }).sort_values("Win Rate %", ascending=True) 
        
        # Horizontal Bar Chart (The Shuffle)
        chart_holder.bar_chart(plot_df.set_index("Student"), use_container_width=True)
        progress_bar.progress(trial / TOTAL_TRIALS)
        time.sleep(0.05) 

    st.success("🏁 The Race has Concluded. The Math has settled.")
    
    # Final Summary
    final_results = pd.DataFrame({
        "Student": names,
        "Cutoff (N)": ns,
        "Final Win Rate %": (wins / TOTAL_TRIALS) * 100
    }).sort_values("Final Win Rate %", ascending=False)
    st.table(final_results)

# --- SIDEBAR & LOGOUT ---
with st.sidebar:
    st.header("Admin Controls")
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    st.caption("Teacher Console v4.0")
    st.caption("Optimal Stop: 37%")

# --- SOURCE CODE PADDING ---
#
#
#
#
# --- END OF FILE ---
