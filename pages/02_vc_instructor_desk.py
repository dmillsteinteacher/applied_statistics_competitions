import streamlit as st
import pandas as pd
import numpy as np
import importlib.util
import os

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="VC Instructor Desk", layout="wide")

# --- 2. MODULE LOADING ---
def load_mod(name):
    current_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(current_dir)
    path = os.path.join(root_dir, name)
    
    if not os.path.exists(path):
        path = os.path.join(current_dir, name)

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None: return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

nav = load_mod("02_vc_lab_narrative.py")
inst_eng = load_mod("02_vc_instructor_engine.py")

if nav is None or inst_eng is None:
    st.error("Missing critical helper files (Narrative or Instructor Engine) in Root.")
    st.stop()

# --- 3. SESSION STATE INITIALIZATION ---
if "contestants" not in st.session_state:
    st.session_state.contestants = []
    st.session_state.results_data = {}  # Stores raw final wealth values: {Name: [results]}
    st.session_state.sim_total_trials = 0
    st.session_state.colors = {}       # Mapping of student names to colors

# --- 4. UI SETUP ---
st.title("🏆 VC Competition: The Horse Race")

pwd = st.sidebar.text_input("Instructor Password", type="password")

if pwd == "VC_LEADER":
    show_truth = st.sidebar.checkbox("🔓 REVEAL MEDIAN TRUTH", value=False)
    # SCENARIO CONFIG
    with st.expander("🛠️ Secret Scenario Configuration", expanded=True):
        col1, col2 = st.columns(2)
        m_sel = col1.selectbox("Set Secret Market", list(nav.MARKET_STORIES.keys()))
        
        # GROUND TRUTH SYNC: Pulling directly from your hand-tuned Narrative file
        p_matrix = nav.P_MATRIX 
        
        st.write("### Current Ground Truth Probabilities:")
        st.json(p_matrix[m_sel])

    st.header("📢 Current Market Briefing")
    st.info(f"**Field Report:** {nav.MARKET_STORIES[m_sel]}")

    # STUDENT ENTRY FORM
    st.subheader("Contestant Registration")
    with st.form("entry_form", clear_on_submit=True):
        f_col1, f_col2, f_col3 = st.columns([2, 2, 1])
        s_name = f_col1.text_input("Student Name")
        s_sec = f_col2.selectbox("Chosen Sector", list(nav.TYPE_STORY.keys()))
        s_f = f_col3.number_input("Strategy (f)", 0.0, 1.0, 0.1, step=0.01)
        
        if st.form_submit_button("Add Strategy"):
            if s_name:
                # Add to contestant list
                st.session_state.contestants.append({"Name": s_name, "Sector": s_sec, "f": s_f})
                # Initialize their color and data slot
                palette = ["#FF4B4B", "#1C83E1", "#00C0F2", "#FFD166", "#06D6A0", "#118AB2", "#EE82EE", "#FFA500"]
                if s_name not in st.session_state.colors:
                    st.session_state.colors[s_name] = palette[len(st.session_state.contestants) % len(palette)]
                    st.session_state.results_data[s_name] = []
                st.rerun()

    # --- 5. THE PENDING ROSTER ---
    if st.session_state.contestants:
        st.write("### Registered Contestants")
        roster_df = pd.DataFrame(st.session_state.contestants)
        st.table(roster_df)
        
        if st.button("Clear All Contestants"):
            st.session_state.contestants = []
            st.session_state.results_data = {}
            st.session_state.sim_total_trials = 0
            st.rerun()

        # --- 6. THE TRUTH ENGINE (HORSE RACE) ---
        st.divider()
        st.header("🏁 The Truth Engine: Live Performance")
        
        sim_col1, sim_col2, sim_col3 = st.columns([1, 1, 2])
        batch_to_add = sim_col1.number_input("Trials per Batch:", 10, 1000, 100, step=10)
        
        if sim_col2.button("🏁 Run Next Batch", type="primary", use_container_width=True):
            # 1. Capture the batch size as a clean integer
            num_to_run = int(batch_to_add) 
            
            # 2. Outer Loop: Number of trials
            for _ in range(num_to_run):
                # 3. Inner Loop: Each contestant
                for c in st.session_state.contestants:
                    p_true = p_matrix[m_sel][c['Sector']]
                    b_val = nav.B_VALS[c['Sector']]
                    
                    final_wealth = inst_eng.run_competition_sim(c['f'], p_true, b_val)
                    
                    if c['Name'] not in st.session_state.results_data:
                        st.session_state.results_data[c['Name']] = []
                    st.session_state.results_data[c['Name']].append(final_wealth)
            
            # 4. FIXED: Update total and rerun ONLY ONCE after all loops finish
            st.session_state.sim_total_trials += num_to_run
            st.rerun()

        # --- 7. THE TRAPPED LEADERBOARD (LOG-SCALE & SHOCK REVEAL) ---
        st.divider()
        st.subheader("📊 Market Leaderboard")
        st.write(f"**Total Universes Simulated:** {st.session_state.sim_total_trials}")
        
        if st.session_state.sim_total_trials > 0:
            leaderboard_data = []
            for name, results in st.session_state.results_data.items():
                arr = np.array(results)
                total_w = np.sum(arr)
                # Log10 scale to keep "Unicorns" from squashing the rest of the class
                log_val = np.log10(total_w + 1)
                
                leaderboard_data.append({
                    "Name": name, 
                    "TotalWealth": total_w,
                    "LogVal": log_val,
                    "Median": np.median(arr), 
                    "Insolvency": np.sum(arr <= 1.0) / len(arr),
                    "Color": st.session_state.colors.get(name, "#1C83E1")
                })
            
            # --- DYNAMIC SORTING ---
            # Sort by AUM if hidden, but snap to Median if Revealed
            if not show_truth:
                leaderboard_data = sorted(leaderboard_data, key=lambda x: x['TotalWealth'], reverse=True)
            else:
                leaderboard_data = sorted(leaderboard_data, key=lambda x: x['Median'], reverse=True)

            # Max log value for relative bar widths
            max_log = max([entry['LogVal'] for entry in leaderboard_data]) if leaderboard_data else 1

            # Header Labels
            h_col1, h_col2, h_col3 = st.columns([0.15, 0.55, 0.30])
            h_col1.caption("**Manager**")
            h_col2.caption("**Total Assets (Log Scale Race)**")
            h_col3.caption("**The Reality**" if show_truth else "**Fund Status**")

            # --- THE RACE TRACK ---
            for entry in leaderboard_data:
                # Calculate bar width based on log scale
                rel_width = (entry['LogVal'] / max_log * 100)
                
                # Logic for the "Reveal"
                if not show_truth:
                    status_text = "🟢 Active" if entry['TotalWealth'] > 0 else "🔴 Liquidated"
                    text_color = "#444"
                else:
                    # The "Shock" reveal: Red for bankruptcy (<$100), Green for profit
                    status_text = f"**Med: ${entry['Median']:,.2f}** ({entry['Insolvency']:.0%} Default)"
                    text_color = "#D32F2F" if entry['Median'] < 100 else "#2E7D32"

                race_html = f"""
                <div style="display: flex; align-items: center; margin-bottom: 6px; font-family: sans-serif;">
                    <div style="width: 15%; text-align: right; padding-right: 12px; font-weight: bold; font-size: 0.85rem; overflow: hidden; white-space: nowrap;">
                        {entry['Name']}
                    </div>
                    <div style="width: 55%; background-color: #f0f2f6; border-radius: 4px; height: 16px;">
                        <div style="width: {rel_width}%; background-color: {entry['Color']}; height: 100%; border-radius: 4px; transition: width 0.6s ease-in-out;">
                        </div>
                    </div>
                    <div style="width: 30%; padding-left: 12px; font-size: 0.85rem; color: {text_color}; white-space: nowrap;">
                        {status_text}
                    </div>
                </div>
                """
                st.markdown(race_html, unsafe_allow_html=True)
            
            st.write("---")
            if show_truth:
                st.success("🏁 **Leaderboard now sorted by Median Wealth Growth.**")
            else:
                st.info("🚀 **Leaderboard sorted by Total Aggregate Wealth (AUM).**")

else:
    st.warning("Please enter the Instructor Password in the sidebar.")

# --- PADDING ---
# ............................................................
