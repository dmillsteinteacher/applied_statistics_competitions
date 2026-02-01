import streamlit as st
import numpy as np
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Strategy Training Lab", layout="wide")

st.title("🧪 Strategy Training Lab: Interactive Mode")
st.markdown("""
**The Rules:**
1. **Look Phase (N%)**: Observe venues to set a benchmark. You **cannot** stop here.
2. **Search Phase**: The first venue that **beats** your benchmark is automatically selected.
""")

# --- 1. STATE MANAGEMENT ---
if 'lab_market' not in st.session_state:
    st.session_state.lab_market = np.random.permutation(np.arange(1, 101))
    st.session_state.current_index = 0
    st.session_state.benchmark = 0
    st.session_state.choice_made = False
    st.session_state.final_choice = None

# --- 2. SETTINGS ---
with st.sidebar:
    st.header("Lab Configuration")
    # DEFAULT TO 1% - No spoilers.
    look_percent = st.slider("Look Phase (N %)", min_value=1.0, max_value=100.0, value=1.0, step=0.01)
    
    if st.button("♻️ Reset Lab / New Market"):
        st.session_state.lab_market = np.random.permutation(np.arange(1, 101))
        st.session_state.current_index = 0
        st.session_state.benchmark = 0
        st.session_state.choice_made = False
        st.session_state.final_choice = None
        st.rerun()

market = st.session_state.lab_market
n_look_count = int(np.floor(look_percent))

# --- 3. THE INTERACTIVE INTERFACE ---
col_ctrl, col_log = st.columns([1, 2])

with col_ctrl:
    st.subheader("Controls")
    curr_idx = st.session_state.current_index
    
    # Visual Phase Indicator
    if not st.session_state.choice_made:
        if curr_idx < n_look_count:
            st.warning(f"PHASE: LOOKING (Venue {curr_idx + 1} of {n_look_count})")
        else:
            st.success(f"PHASE: SEARCHING (Must beat {st.session_state.benchmark})")
    else:
        st.info("PROCESS COMPLETE")

    # Reveal Logic
    if not st.session_state.choice_made and curr_idx < 100:
        if st.button("➡️ Reveal Next Venue", type="primary", use_container_width=True):
            val = market[curr_idx]
            
            # Logic for Look Phase
            if curr_idx < n_look_count:
                if val > st.session_state.benchmark:
                    st.session_state.benchmark = val
            
            # Logic for Search Phase
            else:
                if val > st.session_state.benchmark:
                    st.session_state.choice_made = True
                    st.session_state.final_choice = (curr_idx + 1, val)
            
            # Logic for the end of the line
            if not st.session_state.choice_made and curr_idx == 99:
                st.session_state.choice_made = True
                st.session_state.final_choice = (100, market[99])
            
            st.session_state.current_index += 1
            st.rerun()

    # Results Display
    if st.session_state.choice_made:
        loc, val = st.session_state.final_choice
        st.divider()
        st.metric("Your Final Choice", f"Rank {val}", f"Found at Venue #{loc}")
        
        if val == 100:
            st.balloons()
            st.success("Perfect! You found the Rank 100 venue.")
        else:
            best_pos = np.where(market == 100)[0][0] + 1
            st.error(f"Missed. The Rank 100 venue was at Position #{best_pos}.")

with col_log:
    st.subheader("Activity Log")
    
    history = []
    for i in range(st.session_state.current_index):
        val = market[i]
        is_choice = st.session_state.choice_made and (i == st.session_state.final_choice[0] - 1)
        
        phase_label = "LOOK" if i < n_look_count else "SEARCH"
        note = ""
        if i < n_look_count and val == st.session_state.benchmark:
            note = "⭐ Benchmark Set"
        if is_choice:
            note = "🎯 PICKED"
            
        history.append({
            "Venue": i + 1,
            "Rank": val,
            "Phase": phase_label,
            "Note": note
        })
    
    if history:
        # Most recent reveal at top for easy reading
        df_hist = pd.DataFrame(history).iloc[::-1]
        st.table(df_hist.set_index("Venue"))
    else:
        st.info("Adjust the slider and click 'Reveal Next' to begin.")

# --- 4. AUDIT ---
if st.session_state.choice_made:
    st.divider()
    with st.expander("🔍 View Full Market Sequence (Post-Game Audit)"):
        audit_df = pd.DataFrame({
            "Position": range(1, 101),
            "Value": market,
            "Phase": ["LOOK" if i < n_look_count else "SEARCH" for i in range(100)]
        })
        st.dataframe(audit_df, use_container_width=True)

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
# --- END OF FILE ---
