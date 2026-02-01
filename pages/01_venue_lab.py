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
**The Objective:** Find the Rank 100 venue among 100 hidden values.
1. **Look Phase (N)**: Observe these to set a benchmark. You cannot pick them.
2. **Search Phase**: The first venue that **beats** your benchmark is yours!
""")

# --- 3. SETTINGS & SIDEBAR ---
with st.sidebar:
    st.header("Lab Configuration")
    n_look = st.slider("Look Phase (N Venues)", 1, 100, 1)
    
    if st.button("♻️ Reset Lab / New Market"):
        st.session_state.lab_market = np.random.permutation(np.arange(1, 101))
        st.session_state.current_index = 0
        st.session_state.benchmark = 0
        st.session_state.choice_made = False
        st.session_state.final_choice = None
        st.rerun()

market = st.session_state.lab_market
curr_idx = st.session_state.current_index

# --- 4. THE INTERACTIVE INTERFACE ---
col_ctrl, col_log = st.columns([1, 2])

with col_ctrl:
    st.subheader("Controls")
    
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
        # Top Row: Single Step
        if st.button("➡️ Reveal Next Venue", type="primary", use_container_width=True):
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

        # Bottom Row: Fast Forwards
        f_col1, f_col2 = st.columns(2)
        
        # FF to Search (Only active during Look phase)
        can_ff_search = curr_idx < n_look
        if f_col1.button("⏩ Jump to Search", use_container_width=True, disabled=not can_ff_search):
            # Calculate benchmark up to n_look immediately
            st.session_state.benchmark = np.max(market[:n_look])
            st.session_state.current_index = n_look
            st.rerun()

        # FF to Result
        if f_col2.button("🏁 Leap to Result", use_container_width=True):
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
            # Contextual error message
            if best_pos <= n_look:
                st.error(f"The Rank 100 venue was at Position #{best_pos}—inside your Look Group! You never had a chance to pick it.")
            else:
                st.error(f"The Rank 100 venue was at Position #{best_pos}. You settled for Rank {val} at Position #{loc}.")

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
        st.info("Use controls to start.")

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
