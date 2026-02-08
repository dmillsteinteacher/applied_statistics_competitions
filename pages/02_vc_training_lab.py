import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import importlib.util
import sys

# --- UTILITY: LOAD MODULES ---
def load_mod(file_path):
    spec = importlib.util.spec_from_file_location("engine_mod", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Load the engine and narrative logic
engine = load_mod("02_vc_lab_engine.py")
nav = load_mod("02_vc_lab_narrative.py")

# --- TOP LEVEL RESET ---
# This clears the session state and forces a fresh start
if st.button("🔄 Start New Scenario (Clear All Data)"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.title("VC Training Lab")
st.write("Investigate market probabilities and optimize your reinvestment strategy.")

# Initialize tab structure
tab1, tab2, tab3 = st.tabs(["Phase 1: Audit", "Phase 2: Verification", "Phase 3: Strategy"])

# --- TAB 1: AUDIT ---
with tab1:
    st.header("Step 1: The Sector Audit")
    
    sector = st.selectbox("Choose Investment Sector", list(nav.B_VALS.keys()))
    market = st.selectbox("Choose Market Environment", ["Market A: The Boom", "Market B: The Squeeze", "Market C: Stagnation"])
    
    if st.button("Generate Audit Memo"):
        st.session_state.sector = sector
        st.session_state.market = market
        # Pull p-value from P_MATRIX in narrative
        st.session_state.current_p = nav.P_MATRIX[market][sector]
        st.session_state.p_verified = False 
        
        memo = nav.generate_memo(sector, market)
        st.session_state.memo = memo

    if "memo" in st.session_state:
        st.info("### Internal Memo")
        st.write(st.session_state.memo)

# --- TAB 2: VERIFICATION ---
with tab2:
    st.header("Step 2: Probability Verification")
    if "current_p" not in st.session_state:
        st.warning("Please complete the Audit in Phase 1 first.")
    else:
        st.write(f"Testing for: **{st.session_state.sector}** in **{st.session_state.market}**")
        
        # Grid of results to visually verify the p-value
        cols = st.columns(10)
        for i in range(100):
            with cols[i % 10]:
                if np.random.random() < st.session_state.current_p:
                    st.markdown("🟩")
                else:
                    st.markdown("🟥")
        
        st.divider()
        guess_p = st.number_input("Based on the data above, verify the success probability (p)", 0.0, 1.0, 0.5, 0.01)
        
        if st.button("Verify $p$"):
            if abs(guess_p - st.session_state.current_p) < 0.001:
                st.session_state.p_verified = True
                st.rerun()
            else:
                st.error("Verification failed. Your p-value does not match the market data.")

# --- TAB 3: STRATEGY ---
with tab3:
    st.header("Step 3: Determine Allocation")
    if not st.session_state.get('p_verified', False):
        st.warning("Locked: Verify probability in Phase 1.")
    else:
        # Configuration
        sector_choice = st.session_state.sector
        market_choice = st.session_state.market
        b_val = nav.B_VALS[sector_choice]
        target_p = st.session_state.current_p
        
        # Header - using standard markdown for readable font sizes
        st.markdown(f"**Environment:** {market_choice} | **Target p:** {target_p:.2f} | **Payback b:** {b_val}x")
        st.write(f"Testing reinvestment strategy for **{sector_choice}**")
        
        f_guess = st.slider("Select reinvestment fraction (f)", 0.0, 1.0, 0.1, 0.01)
        
        if st.button("Run Simulation", key="sim_btn"):
            # Execute 100 simulations via the engine
            res = engine.run_simulation(f_guess, target_p, b_val, n_steps=50)
            
            # Extract history for visualization
            history = res['History']
            random_idx = np.random.randint(0, history.shape[0])
            path = history[random_idx, :]
            steps = np.arange(len(path))

            st.subheader(f"Individual Fund Trajectory (Sample #{random_idx})")
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # Color logic: Red if the fund ended insolvent, Green otherwise
            is_insolvent = path[-1] <= 1.0
            p_color = "#e74c3c" if is_insolvent else "#2ecc71"
            
            ax.plot(steps, path, color=p_color, linewidth=2)
            ax.fill_between(steps, path, color=p_color, alpha=0.1)
            
            # Format the plot on a log scale for better exponential visibility
            ax.set_yscale('log')
            ax.set_ylim(bottom=0.1) 
            ax.set_ylabel("Wealth (Log Scale)")
            ax.set_xlabel("Reinvestment Cycles")
            ax.grid(True, which="both", ls="-", alpha=0.1)
            
            st.pyplot(fig)
            plt.close(fig) # Memory cleanup

            st.divider()

            # Batch Statistics Summary (The 100-run aggregate)
            st.subheader("Strategy Statistics (Batch of 100)")
            c1, c2 = st.columns(2)
            c1.metric("Median Final Wealth", f"${res['Median']:,.0f}")
            c2.metric("Insolvency Rate", f"{res['Insolvency Rate']:.1%}")

            with st.expander("Understanding the Insolvency Rate"):
                st.write(f"""
                The **Insolvency Rate** represents the probability of total ruin. 
                Even if your chart above is green, a high insolvency rate 
                means your strategy is likely 'overbetting' and would eventually 
                fail in many parallel universes.
                """)

# --- EOF PADDING ---
# This ensures no truncation issues on final closing characters.
