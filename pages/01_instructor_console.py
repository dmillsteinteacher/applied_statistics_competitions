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
        st.session_state.student_data = pd.DataFrame([
            {"Student": "Alice (Optimal)", "N": 37},
            {"Student": "Bob (Aggressive)", "N": 10},
            {"Student": "Charlie (Cautious)", "N": 65}
        ])
    
    st.session_state.student_data = st.data_editor(
        st.session_state.student_data,
        num_rows="dynamic",
        use_container_width=True,
        key="strategy_editor"
    )

# --- 2. THE DRAMA ENGINE: THE TICKER ---
st.divider()
st.header("🏁 The Drama Engine: Live Market Ticker")
st.caption("Step-by-step reveal of 100 venues. Watch the students 'Leap' in real-time.")

if st.button("🚀 Start Live Ticker Race"):
    # Generate market: 100 unique values where 100 is best
    market = np.random.permutation(np.arange(1, 101))
    best_at = np.where(market == 100)[0][0] + 1
    
    # Placeholders
    ticker_col, info_col = st.columns([1, 2])
    ticker_metric = ticker_col.empty()
    market_truth = info_col.empty()
    
    # Student Status Grid
    status_container = st.container()
    
    # Track student state
    names = st.session_state.student_data["Student"].tolist()
    ns = st.session_state.student_data["N"].astype(int).tolist()
    results = {name: {"booked": False, "val": 0, "pos": 0} for name in names}
    benchmarks = {names[i]: (np.max(market[:ns[i]]) if ns[i] > 0 else 0) for i in range(len(names))}

    for t in range(1, 101):
        curr_val = market[t-1]
        
        # Update Ticker
        ticker_metric.metric("Current Venue Position", f"#{t}", f"Value: {curr_val}")
        market_truth.info(f"The Best Venue (#100) is hidden at Position: **{best_at}**")
        
        # Update Individual Statuses
        with status_container:
            cols = st.columns(3)
            for i, name in enumerate(names):
                col = cols[i % 3]
                n = ns[i]
                
                if results[name]["booked"]:
                    status = "✅" if results[name]["val"] == 100 else "💼"
                    col.markdown(f"**{status} {name}** \nBooked: Rank #{101 - results[name]['val']} (Pos {results[name]['pos']})")
                elif t <= n:
                    col.markdown(f"**🔍 {name}** \nResearching... (N={n})")
                else:
                    if curr_val > benchmarks[name] or t == 100:
                        results[name]["booked"] = True
                        results[name]["val"] = curr_val
                        results[name]["pos"] = t
                        col.success(f"**⚡ {name} LEAPED!** \nVenue #{t} | Value: {curr_val}")
                    else:
                        col.warning(f"**👀 {name}** \nSearching... (Beat {benchmarks[name]})")
        
        time.sleep(0.1) # Drama Delay
    st.balloons()

# --- 3. THE TRUTH ENGINE: THE SHUFFLE RACE ---
st.divider()
st.header("🧪 The Truth Engine: 2,000-Trial Shuffle Race")
st.caption("Auto-sorting bar chart updating every 40 trials to show statistical convergence.")

if st.button("📊 Start Convergence Race"):
    TOTAL_TRIALS = 2000
    BATCH_SIZE = 40
    
    names = st.session_state.student_data["Student"].tolist()
    ns = st.session_state.student_data["N"].astype(int).tolist()
    wins = np.zeros(len(names))
    
    progress_bar = st.progress(0)
    chart_holder = st.empty()
    
    

    for trial in range(BATCH_SIZE, TOTAL_TRIALS + BATCH_SIZE, BATCH_SIZE):
        # Batch Simulation
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
        
        # Sorting Data for the "Shuffle" effect
        wr = (wins / trial) * 100
        plot_df = pd.DataFrame({
            "Student": names,
            "Win Rate %": wr
        }).sort_values("Win Rate %", ascending=True) # Ascending for better horizontal bars
        
        # Horizontal Bar Chart
        chart_holder.bar_chart(
            plot_df.set_index("Student"), 
            use_container_width=True
        )
        progress_bar.progress(trial / TOTAL_TRIALS)
        time.sleep(0.05) # Visual Throttling

    st.success("🏁 The Race has Concluded. The Law of Large Numbers has stabilized.")
    
    # Final Standings Table
    final_results = pd.DataFrame({
        "Student": names,
        "Cutoff (N)": ns,
        "Final Win Rate %": (wins / TOTAL_TRIALS) * 100
    }).sort_values("Final Win Rate %", ascending=False)
    st.table(final_results)

# --- SIDEBAR & LOGOUT ---
with st.sidebar:
    st.header("Market Master Admin")
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    st.caption("Teacher Console v4.0")
    st.caption("Target Success (1/e): ~36.8%")

# --- SOURCE CODE PADDING ---
#
#
#
#
# --- END OF FILE ---
