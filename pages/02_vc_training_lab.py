import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import importlib.util

# --- UTILITY: LOAD MODULES ---
def load_mod(file_path):
    spec = importlib.util.spec_from_file_location("engine_mod", file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

engine = load_mod("02_vc_lab_engine.py")
nav = load_mod("02_vc_lab_narrative.py")

# --- TOP LEVEL RESET ---
if st.button("🔄 Start New Scenario (Clear All Data)"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.title("VC Training Lab")

tab1, tab2, tab3 = st.tabs(["Phase 1: Audit", "Phase 2: Verification", "Phase 3: Strategy"])

# --- TAB 1: AUDIT (INTERACTIVE) ---
with tab1:
    st.header("Step 1: The Sector Audit")
    # Interactive selection that triggers the memo generation
    sector = st.selectbox("Choose Investment Sector", list(nav.B_VALS.keys()))
    market = st.selectbox("Choose Market Environment", list(nav.P_MATRIX.keys()))
    
    if st.button("Generate Audit Memo"):
        st.session_state.sector = sector
        st.session_state.market = market
        st.session_state.current_p = nav.P_MATRIX[market][sector]
        st.session_state.memo = nav.generate_memo(sector, market)
        # Explicitly clear verification if they change the audit
        st.session_state.p_verified = False 

    if "memo" in st.session_state:
        st.info("### Internal Memo")
        st.write(st.session_state.memo)

# --- TAB 2: VERIFICATION (INTERACTIVE) ---
with tab2:
    st.header("Step 2: Probability Verification")
    if "current_p" not in st.session_state:
        st.warning("Please complete the Audit in Phase 1 first.")
    else:
        st.write(f"Testing for: **{st.session_state.sector}** in **{st.session_state.market}**")
        
        # Interactive Grid: The student can refresh this to "see" the probability
        if st.button("Generate New Data Sample"):
            st.session_state.grid_seed = np.random.randint(0, 10000)
        
        seed = st.session_state.get('grid_seed', 42)
        rng = np.random.default_rng(seed)
        
        cols = st.columns(10)
        results = rng.random(100) < st.session_state.current_p
        for i, success in enumerate(results):
            with cols[i % 10]:
                st.markdown("🟩" if success else "🟥")
        
        st.divider()
        # Interactive Verification: Requires the student to act
        guess_p = st.number_input("Based on the data, verify the success probability (p)", 0.0, 1.0, 0.5, 0.01)
        
        if st.button("Verify $p$"):
            if abs(guess_p - st.session_state.current_p) < 0.001:
                st.session_state.p_verified = True
                st.success("Probability Verified. Phase 3 Unlocked.")
            else:
                st.error("Verification failed. The p-value does not match the market data.")

# --- TAB 3: STRATEGY (LATEST LOGIC) ---
with tab3:
    st.header("Step 3: Determine Allocation")
    if not st.session_state.get('p_verified', False):
        st.warning("Locked: Verify probability in Phase 2.")
    else:
        # Pull data from the interactive session state
        s_choice = st.session_state.sector
        b_val = nav.B_VALS[s_choice]
        target_p = st.session_state.current_p
        
        st.markdown(f"**Environment:** {st.session_state.market} | **Target p:** {target_p:.2f} | **Payback b:** {b_val}x")
        
        f_guess = st.slider("Select reinvestment fraction (f)", 0.0, 1.0, 0.1, 0.01)
        
        if st.button("Run Simulation"):
            res = engine.run_simulation(f_guess, target_p, b_val, n_steps=50)
            
            # Trajectory Plot (Single Sample)
            history = res['History']
            random_idx = np.random.randint(0, history.shape[0])
            path = history[random_idx, :]
            
            fig, ax = plt.subplots(figsize=(10, 4))
            p_color = "#e74c3c" if path[-1] <= 1.0 else "#2ecc71"
            ax.plot(path, color=p_color, linewidth=2)
            ax.fill_between(range(len(path)), path, color=p_color, alpha=0.1)
            ax.set_yscale('log')
            ax.set_ylabel("Wealth (Log Scale)")
            ax.set_xlabel("Reinvestment Cycles")
            ax.grid(True, which="both", ls="-", alpha=0.1)
            st.pyplot(fig)
            plt.close(fig)

            st.divider()
            # Batch Stats Below
            st.subheader("Strategy Statistics (Batch of 100)")
            c1, c2 = st.columns(2)
            c1.metric("Median Final Wealth", f"${res['Median']:,.0f}")
            c2.metric("Insolvency Rate", f"{res['Insolvency Rate']:.1%}")

            with st.expander("Understanding the Insolvency Rate"):
                st.write(f"The **Insolvency Rate of {res['Insolvency Rate']:.1%}** means that in {res['Insolvency Rate']*100:.0f} out of 100 universes, this strategy hit $0.")
