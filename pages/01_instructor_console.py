import streamlit as st
import numpy as np
import pandas as pd
import time

# --- CONFIG & SECURITY ---
st.set_page_config(layout="wide", page_title="Teacher Console | Market Master")

# The password variable as requested in the specs
MASTER_PASSWORD = "admin_stats_2026" 

# --- AUTHENTICATION LAYER ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_auth():
    if st.session_state.password_input == MASTER_PASSWORD:
        st.session_state.authenticated = True
        st.session_state.password_input = "" # Clear input
    else:
        st.error("Invalid credentials.")

if not st.session_state.authenticated:
    st.title("🔒 Market Master Login")
    st.text_input("Enter Teacher Password:", type="password", key="password_input", on_change=check_auth)
    st.info("Access restricted to authorized instructors only.")
    st.stop()

# --- AUTHENTICATED UI ---
st.title("👨‍🏫 Teacher Console: Command Center")

# Sidebar for logout and session info
with st.sidebar:
    st.header("Admin Controls")
    if st.button("Logout of Console"):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    st.caption("Mode: v3.0 Specification")

# --- 1. STRATEGY REGISTRATION (Step 2 & 8) ---
st.header("1. Student Strategy Registration")
if 'student_data' not in st.session_state:
    # Initial seed data
    st.session_state.student_data = pd.DataFrame([
        {"Student Name": "Alice", "Cutoff (N)": 37},
        {"Student Name": "Bob", "Cutoff (N)": 10},
        {"Student Name": "Charlie", "Cutoff (N)": 50}
    ])

# Dynamic Data Editor - Persists in session state
updated_df = st.data_editor(
    st.session_state.student_data,
    num_rows="dynamic",
    use_container_width=True,
    key="strategy_editor"
)
st.session_state.student_data = updated_df

# --- 2. THE DRAMA ENGINE (Steps 3, 5, 7) ---
st.divider()
st.header("2. The Drama Engine: Live Horse Race")
st.markdown("Run a single trial where everyone competes against the same 100 venues.")

if st.button("🏁 Run Live Single Trial", use_container_width=True):
    # Synchronized Market Generation
    # We use 1-100 values where 100 is the "Best"
    market_scores = np.random.permutation(np.arange(1, 101))
    best_value = 100
    best_position = np.where(market_scores == best_value)[0][0] + 1 # 1-indexed
    
    results = []
    
    for _, row in st.session_state.student_data.iterrows():
        name = row["Student Name"]
        n = int(row["Cutoff (N)"])
        
        # Secretary Problem Logic
        # Research Phase (1 to N)
        if n == 0:
            benchmark = 0
        else:
            benchmark = np.max(market_scores[:n])
            
        # Selection Phase (N+1 to 100)
        selected_value = market_scores[-1] # Default to last if none beat benchmark
        for val in market_scores[n:]:
            if val > benchmark:
                selected_value = val
                break
        
        # Translate value to rank (Value 100 = Rank 1, Value 1 = Rank 100)
        true_rank = 101 - selected_value
        results.append({
            "Student": name,
            "Cutoff": n,
            "Venue Rank": true_rank,
            "Result": "🏆 WINNER" if selected_value == 100 else "❌"
        })
    
    # Reveal the Truth
    st.subheader(f"Market Truth: The #1 Venue was at Position #{best_position}")
    
    res_df = pd.DataFrame(results).sort_values("Venue Rank")
    st.table(res_df)
    
    if any(r["Result"] == "🏆 WINNER" for r in results):
        st.balloons()

# --- 3. THE TRUTH ENGINE (Step 9) ---
st.divider()
st.header("3. The Truth Engine: Convergence Race")
st.markdown("Simulate 10,000 trials to see which strategy holds up over time. Updates every 200 trials.")

if st.button("🧪 Start 10,000 Trial Convergence", use_container_width=True):
    TOTAL_TRIALS = 10000
    BATCH_SIZE = 200
    
    # Setup for simulation
    names = st.session_state.student_data["Student Name"].tolist()
    ns = st.session_state.student_data["Cutoff (N)"].astype(int).tolist()
    win_counts = np.zeros(len(names))
    
    # UI Placeholders for animation
    status_text = st.empty()
    progress_bar = st.progress(0)
    chart_holder = st.empty()
    
    for current_trial in range(BATCH_SIZE, TOTAL_TRIALS + BATCH_SIZE, BATCH_SIZE):
        # Run Batch
        for i, n in enumerate(ns):
            # Inner loop for 200 trials
            for _ in range(BATCH_SIZE):
                s = np.random.permutation(np.arange(1, 101))
                b = np.max(s[:n]) if n > 0 else 0
                p = s[-1]
                for v in s[n:]:
                    if v > b:
                        p = v
                        break
                if p == 100:
                    win_counts[i] += 1
        
        # Prepare Data for Charting
        current_rates = (win_counts / current_trial) * 100
        plot_df = pd.DataFrame({
            "Student": names,
            "Win Rate %": current_rates
        })
        
        # Horizontal Bar Chart for the "Race"
        status_text.write(f"**Simulation Progress:** {current_trial} / {TOTAL_TRIALS} trials")
        progress_bar.progress(current_trial / TOTAL_TRIALS)
        chart_holder.bar_chart(plot_df.set_index("Student"), use_container_width=True)
        
        # Small sleep to allow students to see the "Jitter" settle
        time.sleep(0.05)
        
    st.success("🏁 Final Standings after 10,000 trials:")
    final_df = pd.DataFrame({
        "Student": names,
        "Cutoff (N)": ns,
        "Final Win Rate %": (win_counts / TOTAL_TRIALS) * 100
    }).sort_values("Final Win Rate %", ascending=False)
    st.dataframe(final_df, use_container_width=True)

# Footer padding as per previous design preference
# --- SOURCE CODE PADDING ---
#
#
#
#
#
# --- END OF FILE ---
