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

# Initialize Tabs
tab1, tab2, tab3 = st.tabs(["Phase 1: Audit", "Phase 2: Verification", "Phase 3: Strategy"])

# --- TAB 1: AUDIT ---
with tab1:
    st.header("Step 1: The Sector Audit")
    
    # We use index=0 or session_state to keep selections stable
    sector = st.selectbox("Choose Investment Sector", list(nav.B_VALS.keys()))
    market = st.selectbox("Choose Market Environment", list(nav.P_MATRIX.keys()))
    
    if st.button("Generate Audit Memo"):
        st.session_state.sector = sector
        st.session_state.market = market
        st.session_state.current_p = nav.P_MATRIX[market][sector]
        st.session_state.memo = nav.generate_memo(sector, market)
        st.session_state.p_verified = False # Reset verification on new audit

    # PERSISTENCE: If the memo exists in state, show it
    if "memo" in st.session_state:
        st.info("### Internal Memo")
        st.write(st.session_state.memo)

# --- TAB 2: VERIFICATION ---
with tab2:
    st.header("Step 2: Probability Verification")
    if "sector" not in st.session_state:
        st.warning("Please complete the Audit in Phase 1 first.")
    else:
        st.write(f"Testing for: **{st.session_state.sector}** in **{st.session_state.market}**")
        
        # Grid of results (using a fixed seed based on session to keep grid stable)
        cols = st.columns(10)
        for i in range(100):
            with cols[i % 10]:
                # We use a stable random check so the grid doesn't flicker on every click
                if np.random.default_rng(i + 42).random() < st.session_state.current_p:
                    st.markdown("🟩")
                else:
                    st.markdown("🟥")
        
        st.divider()
        guess_p = st.number_input("Verify success probability (p)", 0.0, 1.0, 0.5, 0.01)
        
        if st.button("Verify $p$"):
            if abs(guess_p - st.session_state.current_p) < 0.001:
                st.session_state.p_verified = True
                st.rerun()
            else:
                st.error("Verification failed.")

# --- TAB 3: STRATEGY ---
with tab3:
    st.header("Step 3: Determine Allocation")
    if "sector" not in st.session_state or not st.session_state.get('p_verified', False):
        st.warning("Locked: Verify probability in Phase 1 and 2.")
    else:
        b_val = nav.B_VALS[st.session_state.sector]
        target_p = st.session_state.current_p
        
        st.markdown(f"**Environment:** {st.session_state.market} | **Target p:** {target_p:.2f} | **Payback b:** {b_val}x")
        
        f_guess = st.slider("Select reinvestment fraction (f)", 0.0, 1.0, 0.1, 0.01)
        
        if st.button("Run Simulation"):
            res = engine.run_simulation(f_guess, target_p, b_val, n_steps=50)
            
            # Trajectory Plot
            history = res['History']
            random_idx = np.random.randint(0, history.shape[0])
            path = history[random_idx, :]
            
            fig, ax = plt.subplots(figsize=(10, 4))
            p_color = "#e74c3c" if path[-1] <= 1.0 else "#2ecc71"
            ax.plot(path, color=p_color, linewidth=2)
            ax.fill_between(range(len(path)), path, color=p_color, alpha=0.1)
            ax.set_yscale('log')
            ax.set_ylabel("Wealth (Log)")
            st.pyplot(fig)
            plt.close(fig)

            st.divider()
            st.subheader("Strategy Statistics")
            c1, c2 = st.columns(2)
            c1.metric("Median Final Wealth", f"${res['Median']:,.0f}")
            c2.metric("Insolvency Rate", f"{res['Insolvency Rate']:.1%}")
