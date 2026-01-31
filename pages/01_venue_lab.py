import streamlit as st
import numpy as np
import pandas as pd

# --- HELPER FUNCTIONS ---
def get_dynamic_description(rank_index):
    """Returns a 'vibe' description based on the internal rank (0=worst, 99=best)"""
    if rank_index > 95:
        return "✨ Absolute Perfection. A legendary venue."
    elif rank_index > 85:
        return "💎 Premium Quality. Highly sought after."
    elif rank_index > 70:
        return "✅ Very Solid. Better than most."
    elif rank_index > 50:
        return "⚖️ Decent. It gets the job done."
    elif rank_index > 30:
        return "⚠️ Mediocre. Some red flags."
    else:
        return "🏚️ Sub-par. The reviews are... honest."

# --- PAGE CONFIG ---
st.set_page_config(page_title="Venue Lab", page_icon="🏢", layout="wide")

st.title("🏢 The Senior Party Venue Lab")
st.markdown("""
Acting as the social chair, you must pick the best venue. 
**The Catch:** You see them one by one. Once you reject a venue, you can never go back.
""")

tab1, tab2 = st.tabs(["🎮 Mode 1: Manual Hunt", "📈 Mode 2: Large Scale Simulation"])

# --- TAB 1: MANUAL HUNT (Step-by-Step) ---
with tab1:
    st.header("The Manual Hunt")
    
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
        st.session_state.current_index = 0
        st.session_state.benchmark = 0
        st.session_state.booked = False
        st.session_state.scores = []
        st.session_state.ranks = []
        st.session_state.descs = []

    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.write("### Strategy")
        k_val = st.slider("Research Cutoff (N)", 1, 99, 37, 
                          help="How many venues to observe before you are eligible to book?")
        
        if st.button("🌟 Start New Game / Reset"):
            power = np.random.choice([10, 100, 1000])
            base = np.random.randint(1, 100) * power
            scores = np.random.choice(range(base, base + 2000), 100, replace=False)
            
            sorted_indices = np.argsort(scores)
            ranks = np.zeros(100, dtype=int)
            ranks[sorted_indices] = np.arange(100)
            
            st.session_state.scores = scores
            st.session_state.ranks = ranks
            st.session_state.descs = [get_dynamic_description(r) for r in ranks]
            st.session_state.game_active = True
            st.session_state.current_index = 0
            st.session_state.benchmark = 0
            st.session_state.booked = False
            st.rerun()

    with c2:
        if st.session_state.game_active:
            idx = st.session_state.current_index
            scores = st.session_state.scores
            descs = st.session_state.descs
            
            if idx < k_val:
                st.subheader(f"🕵️ Research Phase ({idx + 1} / {k_val})")
                st.warning("Currently building your benchmark. You cannot book yet.")
            else:
                st.subheader(f"⚡ Selection Phase ({idx + 1} / 100)")
                st.info(f"**Benchmark to Beat: {st.session_state.benchmark:,}**")

            st.markdown(f"""
            <div style="padding:20px; border:2px solid #f0f2f6; border-radius:10px; background-color: #f9f9f9;">
                <h1 style="color: #1f77b4;">Value: {scores[idx]:,}</h1>
                <p style="font-size: 1.3rem; color: #333;">{descs[idx]}</p>
            </div>
            """, unsafe_allow_html=True)

            if not st.session_state.booked:
                btn_label = "Next Venue" if idx < 99 else "See Final Forced Choice"
                if st.button(f"➡️ {btn_label}"):
                    if idx < k_val:
                        if scores[idx] > st.session_state.benchmark:
                            st.session_state.benchmark = scores[idx]
                    
                    if idx >= k_val and scores[idx] > st.session_state.benchmark:
                        st.session_state.booked = True
                    elif idx == 99:
                        st.session_state.booked = True
                    else:
                        st.session_state.current_index += 1
                    st.rerun()
            
            if st.session_state.booked:
                final_rank = 100 - st.session_state.ranks[idx]
                st.success(f"### ✅ BOOKED AT VENUE #{idx + 1}!")
                
                col_a, col_b = st.columns(2)
                col_a.metric("Your Venue Rank", f"#{final_rank}")
                col_b.metric("Best Possible Value", f"{max(scores):,}")
                
                if final_rank == 1:
                    st.balloons()
                    st.snow()
                    st.write("🏆 **PERFECT!** You found the #1 venue!")
                elif final_rank <= 10:
                    st.write("👏 **Excellent!** You landed in the top 10%.")
                else:
                    st.write("😅 **Ouch.** Tough luck this time!")

# --- TAB 2: LARGE SCALE SIMULATION ---
with tab2:
    st.header("Mode 2: The Math of 10,000 Hunts")
    st.write("Determine the optimal 'Stopping Rule' by simulating thousands of trials instantly.")
    
    sim_k = st.slider("Testing Cutoff (N)", 1, 99, 37, key="sim_k")
    num_trials = 10000

    if st.button("🚀 Run 10,000 Simulations"):
        with st.spinner("Simulating..."):
            success_count = 0
            results = []
            for _ in range(num_trials):
                sim_scores = np.random.permutation(np.arange(100))
                benchmark = -1
                if sim_k > 0:
                    benchmark = np.max(sim_scores[:sim_k])
                
                selection = sim_scores[-1]
                for i in range(sim_k, 100):
                    if sim_scores[i] > benchmark:
                        selection = sim_scores[i]
                        break
                if selection == 99:
                    success_count += 1
                results.append(selection)

            win_rate = (success_count / num_trials) * 100
            st.metric("Win Rate (Found #1 Venue)", f"{win_rate:.2f}%")
            
            st.write("### Distribution of Ranks Found")
            display_results = [100 - r for r in results]
            chart_data = pd.Series(display_results).value_counts().sort_index()
            st.bar_chart(chart_data)

st.markdown("---")
st.caption("Applied Statistics Competitions | Venue Lab v2.0")

# --- PADDING ---
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
