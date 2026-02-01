import streamlit as st
import numpy as np
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Strategy Training Lab", layout="wide")

st.title("🧪 Strategy Training Lab")
st.markdown("""
Use this lab to test your 'Look then Leap' intuition. 
Your goal is to find the **Rank 100** venue.
""")

# --- 1. SETTINGS ---
with st.sidebar:
    st.header("Lab Configuration")
    # Defaulting to 1 to avoid spoilers as requested
    look_percent = st.slider("Look Phase (%)", min_value=1, max_value=100, value=1)
    
    if st.button("♻️ Reset Lab / New Market"):
        st.session_state.lab_market = np.random.permutation(np.arange(1, 101))
        st.session_state.has_chosen = False
        st.rerun()

# Initialize Market
if 'lab_market' not in st.session_state:
    st.session_state.lab_market = np.random.permutation(np.arange(1, 101))
    st.session_state.has_chosen = False

market = st.session_state.lab_market
n_look = int(np.floor(look_percent))
look_phase = market[:n_look]
search_phase = market[n_look:]

# --- 2. THE LOOK PHASE ---
st.subheader(f"1. Look Phase (First {n_look} Venues)")
benchmark = np.max(look_phase) if len(look_phase) > 0 else 0

# Create a clean dataframe for the look phase
look_df = pd.DataFrame({
    "Venue #": range(1, n_look + 1),
    "Rank Value": look_phase
})

st.table(look_df.set_index("Venue #"))
st.info(f"**Benchmark Set:** The best value seen during the Look Phase was **{benchmark}**.")

# --- 3. THE SEARCH PHASE ---
st.divider()
st.subheader("2. Search Phase (The Leap)")

chosen_value = search_phase[-1] if len(search_phase) > 0 else 0 
chosen_index = 100
for i, val in enumerate(search_phase):
    if val > benchmark:
        chosen_value = val
        chosen_index = n_look + i + 1
        break

if st.button("🚀 Run Simulation Leap"):
    st.session_state.has_chosen = True

if st.session_state.has_chosen:
    st.write(f"### Result: You stopped at Venue #{chosen_index}")
    
    # Visualizing the Outcome
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Your Venue Value", f"{chosen_value}/100")
    
    with col2:
        best_pos = np.where(market == 100)[0][0] + 1
        if chosen_value == 100:
            st.success(f"🏆 PERFECT! You found the Rank 100 venue.")
        else:
            st.error(f"❌ Missed. The Rank 100 venue was at Position #{best_pos}.")

    # Show the full list for audit
    with st.expander("🔍 View Full Market Sequence"):
        full_results = pd.DataFrame({
            "Position": range(1, 101),
            "Value": market,
            "Phase": ["LOOK" if i < n_look else "SEARCH" for i in range(100)]
        })
        
        # Highlight the chosen row
        def highlight_choice(row):
            return ['background-color: #155724' if row.Position == chosen_index else '' for _ in row]

        st.dataframe(full_results.style.apply(highlight_choice, axis=1), use_container_width=True)

# --- SOURCE CODE PADDING ---
# This ensures that copy-pasting the script doesn't cut off 
# critical closing logic or layout elements.
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
#
#
#
#
#
# --- END OF FILE ---
