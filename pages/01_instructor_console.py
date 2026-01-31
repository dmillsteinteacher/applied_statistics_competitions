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
        # Initializing with a clean dictionary to force column names
        st.session_state.student_data = pd.DataFrame([
            {"Student": "Alice (Optimal)", "N": 37},
            {"Student": "Bob (Aggressive)", "N": 10},
            {"Student": "Charlie (Cautious)", "N": 65}
        ])
    
    # Data editor with explicit column configuration to force naming
    st.session_state.student_data = st.data_editor(
        st.session_state.student_data,
        num_rows="dynamic",
        use_container_width=True,
        key="strategy_editor_final",
        column_config={
            "Student": st.column_config.TextColumn("Student", required=True),
            "N": st.column_config.NumberColumn("N", min_value=0, max_value=100, step=1, required=True)
        }
    )

# --- HELPER TO EXTRACT DATA SAFELY ---
def get_clean_data():
    df = st.session_state.student_data.copy()
    # Force column names in case Streamlit dropped them
    if len(df.columns) >= 2:
        df.columns = ["Student", "N"] + list(df.columns[2:])
    return df

# --- 2. THE DRAMA ENGINE: THE TICKER ---
st.divider()
st.header("🏁 The Drama Engine: Live Market Ticker")

if st.button("🚀 Start Live Ticker Race"):
    df = get_clean_data()
    
    market = np.random.permutation(np.arange(1, 101))
    best_at = np.where(market == 100)[0][0] + 1
    
    ticker_col, info_col = st.columns([1, 2])
    ticker_metric = ticker_col.empty()
    market_truth = info_col.empty()
    
    status_container = st.container()
    
    names = df["Student"].astype(str).tolist()
    ns = pd.to_numeric(df["N"], errors='coerce').fillna(0).astype(int).tolist()
    
    results = {name: {"booked": False, "val": 0, "pos": 0} for name in names}
    
    # Pre-calculate benchmarks
    benchmarks = {}
    for i, name in enumerate(names):
        cutoff = ns[i]
        benchmarks[name] = np.max(market[:cutoff]) if cutoff > 0 else 0

    # THE TICKER LOOP
    for t in range(1, 101):
        curr_val = market[t-1]
        ticker_metric.metric("Venue Position", f"#{t}", f"Value: {curr_val}")
        market_truth.info(f"The Best Venue (#100) is hidden at Position: **{best_at}**")
        
        with status_container:
            cols = st.columns(3)
            for i, name in enumerate(names):
                col = cols[i % 3]
                n = ns[i]
                
                if results[name]["booked"]:
                    icon = "🏆" if results[name]["val"] == 100 else "💼"
                    col.markdown(f"**{icon} {name}** \nRank #{101 - results[name]['val']} (Pos {results[name]['pos']})")
                elif t <= n:
                    col.markdown(f"**🔍 {name}** \nResearching (N={n})")
                else:
                    if curr_val > benchmarks[name] or t == 100:
                        results[name]["booked"] = True
                        results[name]["val"] = curr_val
                        results[name]["pos"] = t
                        col.success(f"**⚡ {name} LEAPED!** \nVenue #{t} | Val: {curr_val}")
                    else:
                        col.warning(f"**👀 {name}** \nSearching...")
        
        time.sleep(0.08) 
    
    if any(res["val"] == 100 for res in results.values()):
        st.balloons()

# --- 3. THE TRUTH ENGINE: THE SHUFFLE RACE ---
st.divider()
st.header("🧪 The Truth Engine: 2,000-Trial Shuffle Race")

if st.button("📊 Start Convergence Race"):
    df = get_clean_data()
    TOTAL_TRIALS = 2000
    BATCH_SIZE = 40
    
    names = df["Student"].astype(str).tolist()
    ns = pd.to_numeric(df["N"], errors='coerce').fillna(0).astype(int).tolist()
    wins = np.zeros(len(names))
    
    progress_bar = st.progress(0)
    chart_holder = st.empty()
    
    # 

    for trial in range(BATCH_SIZE, TOTAL_TRIALS + BATCH_SIZE, BATCH_SIZE):
        for i, n in enumerate(ns):
            # Batch of trials
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
        
        wr = (wins / trial) * 100
        plot_df = pd.DataFrame({"Student": names, "Win Rate %": wr}).sort_values("Win Rate %", ascending=True)
        
        chart_holder.bar_chart(plot_df.set_index("Student"), use_container_width=True)
        progress_bar.progress(trial / TOTAL_TRIALS)
        time.sleep(0.02) 

    st.success("🏁 Simulation Complete.")
    final_results = pd.DataFrame({"Student": names, "N": ns, "Win Rate %": (wins/TOTAL_TRIALS)*100}).sort_values("Win Rate %", ascending=False)
    st.table(final_results)

# --- SIDEBAR ---
with st.sidebar:
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()
    st.caption("Teacher Console v4.1 | Optimized for Drama")

# --- SOURCE CODE PADDING ---
#
#
#
#
# --- END OF FILE ---
