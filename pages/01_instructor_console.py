import streamlit as st
import numpy as np
import pandas as pd

# --- CONFIG & SECURITY ---
st.set_page_config(layout="wide", page_title="Market Master Console v5.0")
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
        key="editor_v5"
    )

# --- 2. THE MANUAL REVEAL ENGINE ---
st.divider()
st.header("🏁 The Manual Reveal")

col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])

if col_ctrl1.button("🎲 Generate New Market", use_container_width=True):
    st.session_state.market_list = np.random.permutation(np.arange(1, 101))
    st.session_state.current_step = 0
    st.session_state.student_results = {}
    st.rerun()

if st.session_state.market_list is not None:
    # Facilitation Controls
    if st.session_state.current_step < 100:
        if col_ctrl2.button("➡️ Next Venue", type="primary", use_container_width=True):
            st.session_state.current_step += 1
            st.rerun()
    
    if col_ctrl3.button("Reset Reveal", use_container_width=True):
        st.session_state.current_step = 0
        st.session_state.student_results = {}
        st.rerun()

    # Dashboard Metrics
    m1, m2, m3 = st.columns(3)
    step = st.session_state.current_step
    market = st.session_state.market_list

    if step > 0:
        curr_val = market[step-1]
        m1.metric("Current Venue", f"#{step}")
        m2.metric("Venue Value", f"{curr_val}")
        
        # Calculate Statuses
        df = st.session_state.student_data.copy()
        if len(df.columns) >= 2:
            df.columns = ["Student", "N"] + list(df.columns[2:])
        
        status_list = []
        for _, row in df.iterrows():
            name = row["Student"]
            n = int(row["N"])
            
            # Logic for persistent booking
            if name not in st.session_state.student_results:
                if step <= n:
                    status = "🔍 Researching"
                else:
                    benchmark = np.max(market[:n]) if n > 0 else 0
                    if curr_val > benchmark or step == 100:
                        st.session_state.student_results[name] = {
                            "Step": step,
                            "Value": curr_val,
                            "Rank": 101 - curr_val
                        }
                        status = f"✅ BOOKED (Rank {101-curr_val})"
                    else:
                        status = "👀 Searching..."
            else:
                res = st.session_state.student_results[name]
                status = f"✅ BOOKED at #{res['Step']} (Rank {res['Rank']})"
            
            status_list.append({"Student": name, "Status": status})

        # Display Status Matrix
        st.table(pd.DataFrame(status_list))

    else:
        st.info("Market generated. Click 'Next Venue' to begin the reveal.")

# --- 3. POST-RACE SUMMARY ---
if st.session_state.current_step == 100 or (st.session_state.student_results and len(st.session_state.student_results) == len(st.session_state.student_data)):
    st.divider()
    st.header("📊 Post-Race Summary")
    
    winners = [name for name, res in st.session_state.student_results.items() if res["Rank"] == 1]
    
    c1, c2 = st.columns(2)
    c1.metric("Found #1 Venue", f"{len(winners)}")
    c2.write("**The Winners:**")
    c2.write(", ".join(winners) if winners else "None this round.")

    summary_df = pd.DataFrame.from_dict(st.session_state.student_results, orient='index').reset_index()
    summary_df.columns = ["Student", "Stop Step", "Venue Value", "Final Rank"]
    st.dataframe(summary_df.sort_values("Final Rank"), use_container_width=True)

# --- 4. THE TRUTH ENGINE ---
st.divider()
st.header("🧪 The Truth Engine (2,000 Trials)")
if st.button("📊 Run Simulation Race"):
    df = st.session_state.student_data.copy()
    if len(df.columns) >= 2:
        df.columns = ["Student", "N"] + list(df.columns[2:])
    names = df["Student"].tolist()
    ns = pd.to_numeric(df["N"]).fillna(0).astype(int).tolist()
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
        
        plot_df = pd.DataFrame({"Student": names, "Win Rate %": (wins/trial)*100}).sort_values("Win Rate %")
        chart_holder.bar_chart(plot_df.set_index("Student"))

with st.sidebar:
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()
    st.caption("Auctioneer Mode v5.0")

# --- SOURCE CODE PADDING ---
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
