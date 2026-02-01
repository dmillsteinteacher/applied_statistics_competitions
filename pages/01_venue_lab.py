import streamlit as st
import numpy as np
import pandas as pd

# --- 1. INITIALIZE SESSION STATE ---
if 'lab_market' not in st.session_state:
    st.session_state.lab_market = np.random.permutation(np.arange(1, 101))
    st.session_state.current_index = 0
    st.session_state.benchmark = 0
    st.session_state.choice_made = False
    st.session_state.final_choice = None

# --- 2. CONFIG ---
st.set_page_config(page_title="Strategy Training Lab", layout="wide")

st.title("🧪 Strategy Training Lab")
st.markdown("""
**The Objective:** Find the Rank 100 venue among a sequence of 100 hidden values.
1. **Look Phase (N)**: You must observe these venues to set a benchmark. You cannot pick them.
2. **Search Phase**: The first venue that **beats** your benchmark is automatically selected.
""")

# --- 3. SETTINGS & SIDEBAR ---
with st.sidebar:
    st.header("Lab Configuration")
    # Integer only: 1 to 100 venues.
    n_look = st.slider(
        "Look Phase (N Venues)", 
        min_value=1, 
        max_value=100, 
        value=1
    )
    
    if st.button("♻️ Reset Lab / New Market"):
        st.session_state.lab_market = np.random.permutation(np.arange(1, 101))
        st.session_state.current_index = 0
        st.session_state.benchmark = 0
        st.session_state.choice_made = False
        st.session_state.final_choice = None
        st.rerun()

market = st.session_state.lab_market

# --- 4. THE INTERACTIVE INTERFACE ---
col_ctrl, col_log = st.columns([1, 2])

with col_ctrl:
    st.subheader("Controls")
    curr_idx = st.session_state.current_index
    
    # Phase Status
    if not st.session_state.choice_made:
        if curr_idx < n_look:
            st.warning(f"PHASE: LOOKING (Venue {curr_idx + 1} of {n_look})")
        else:
            st.success(f"PHASE: SEARCHING (Must beat {st.session_state.benchmark})")
    else:
        st.info("PROCESS COMPLETE")

    # Action Buttons
    if not st.session_state.choice_made and curr_idx < 100:
        btn_col1, btn_col2 = st.columns(2)
        
        if btn_col1.button("➡️ Next Venue", type="primary", use_container_width=True):
            val = market[curr_idx]
            if curr_idx < n_look:
                if val > st.session_state.benchmark:
                    st.session_state.benchmark = val
            else:
                if val > st.session_state.benchmark:
                    st.session_state.choice_made = True
                    st.session_state.final_choice = (curr_idx + 1, val)
            
            if not st.session_state.choice_made and curr_idx == 99:
                st.session_state.choice_made = True
                st.session_state.final_choice = (100, market[99])
            
            st.session_state.current_index += 1
            st.rerun()

        if btn_col2.button("⏩ Fast Forward", use_container_width=True):
            # Automated logic to find where the strategy would stop
            bench = np.max(market[:n_look])
            found = False
            for i in range(n_look, 100):
                if market[i] > bench:
                    st.session_state.final_choice = (i + 1, market[i])
                    st.session_state.current_index = i + 1
                    found = True
                    break
            if not found:
                st.session_state.final_choice = (100, market[99])
                st.session_state.current_index = 100
            
            st.session_state.benchmark = bench
            st.session_state.choice_made = True
            st.rerun()

    # Results Display
    if st.session_state.choice_made:
        loc, val = st.session_state.final_choice
        st.divider()
        st.metric("Your Selection", f"Rank {val}", f"At Position #{loc}")
        
        best_pos = np.where(market == 100)[0][0] + 1
        if val == 100:
            st.balloons()
            st.success("Perfect! You found the Rank 100 venue.")
        else:
            st.error(f"The Rank 100 venue was at Position #{best_pos}.")

with col_log:
    st.subheader("Activity Log")
    
    history = []
    for i in range(st.session_state.current_index):
        val = market[i]
        is_choice = st.session_state.choice_made and (i == st.session_state.final_choice[0] - 1)
        phase_label = "LOOK" if i < n_look else "SEARCH"
        note = "⭐ Benchmark" if (i < n_look and val == st.session_state.benchmark) else ("🎯 PICKED" if is_choice else "")
            
        history.append({"Venue": i + 1, "Rank": val, "Phase": phase_label, "Note": note})
    
    if history:
        st.table(pd.DataFrame(history).iloc[::-1].set_index("Venue"))
    else:
        st.info("Observe venues to see results here.")

# --- 5. AUDIT ---
if st.session_state.choice_made:
    with st.expander("🔍 Full Market Audit"):
        st.dataframe(pd.DataFrame({
            "Position": range(1, 101),
            "Value": market,
            "Phase": ["LOOK" if i < n_look else "SEARCH" for i in range(100)]
        }), use_container_width=True)

# --- PADDING ---
#
#
#
#
#
#
# --- END OF FILE ---
