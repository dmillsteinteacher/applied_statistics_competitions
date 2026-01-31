import streamlit as st
import numpy as np

# --- HELPER FUNCTIONS ---
def get_dynamic_description(rank_index):
    """0 is worst, 99 is best internal rank"""
    if rank_index > 95: return "✨ Absolute Perfection. A legendary venue."
    elif rank_index > 85: return "💎 Premium Quality. Highly sought after."
    elif rank_index > 70: return "✅ Very Solid. Better than most."
    elif rank_index > 50: return "⚖️ Decent. It gets the job done."
    elif rank_index > 30: return "⚠️ Mediocre. Some red flags."
    else: return "🏚️ Sub-par. The reviews are... honest."

# --- PAGE CONFIG ---
st.set_page_config(page_title="Venue Lab: Training Ground", page_icon="🏢", layout="wide")

# --- CUSTOM COMMAND CENTER STYLING ---
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .main { padding-top: 2rem; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 5px; border: 1px solid #d1d5db; }
    .phase-header { font-size: 1.5rem; font-weight: bold; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: center; }
    .research { background-color: #ff9800; color: white; }
    .selection { background-color: #2196f3; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏢 Venue Lab: The Training Ground")

# --- NARRATIVE & STAKES ---
with st.sidebar:
    st.header("The Mission")
    st.info("""
    **The Story:** You are the Senior Party Social Chair. You have 100 venues to vet.
    
    **The Rules:** You see them one-by-one. Once you pass a venue, it's gone forever.
    
    **The Stakes:** Practice here to find your 'Magic Number' (Cutoff N). Once ready, submit your N to the Instructor for the Official Horse Race.
    """)
    
    st.divider()
    k_val = st.slider("Your Practice Cutoff (N)", 1, 99, 37, help="Number of venues to vet for research.")
    
    if st.button("🌟 Start New Practice Hunt", use_container_width=True):
        # Shifting Scale Logic
        power = np.random.choice([10, 100, 1000])
        base = np.random.randint(1, 100) * power
        scores = np.random.choice(range(base, base + 2000), 100, replace=False)
        
        # Internal Ranking
        sorted_indices = np.argsort(scores)
        ranks = np.zeros(100, dtype=int)
        ranks[sorted_indices] = np.arange(100)
        
        st.session_state.update({
            'game_active': True,
            'current_index': 0,
            'benchmark': 0,
            'booked': False,
            'scores': scores,
            'ranks': ranks,
            'descs': [get_dynamic_description(r) for r in ranks],
            'k': k_val
        })
        st.rerun()

# --- THE MANUAL HUNT ENGINE ---
if 'game_active' in st.session_state and st.session_state.game_active:
    idx = st.session_state.current_index
    scores = st.session_state.scores
    booked = st.session_state.booked
    k = st.session_state.k

    # 1. COMMAND CENTER METRICS
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Venue", f"{idx + 1} / 100")
    m2.metric("N-Cutoff", f"{k}")
    m3.metric("Benchmark to Beat", f"{st.session_state.benchmark:,}")

    st.divider()

    # 2. PHASE INDICATOR & REVEAL
    if not booked:
        if idx < k:
            st.markdown(f'<div class="phase-header research">🕵️ RESEARCH PHASE: Building the Benchmark</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="phase-header selection">⚡ SELECTION PHASE: Active Search Mode</div>', unsafe_allow_html=True)

        # Venue Display Card
        st.markdown(f"""
            <div style="padding:40px; border:3px solid #1f77b4; border-radius:15px; background-color: white; text-align: center;">
                <h1 style="font-size: 4rem; color: #1f77b4; margin-bottom: 0;">{scores[idx]:,}</h1>
                <p style="font-size: 1.5rem; color: #4b5563;">{st.session_state.descs[idx]}</p>
            </div>
        """, unsafe_allow_html=True)

        # Interaction Logic
        st.write("")
        if st.button("➡️ VIEW NEXT VENUE", use_container_width=True):
            # Update Benchmark during Research
            if idx < k:
                if scores[idx] > st.session_state.benchmark:
                    st.session_state.benchmark = scores[idx]
            
            # Auto-Stop Logic (The Leap)
            if idx >= k and scores[idx] > st.session_state.benchmark:
                st.session_state.booked = True
            elif idx == 99: # Forced Choice at end
                st.session_state.booked = True
            else:
                st.session_state.current_index += 1
            st.rerun()
    
    # 3. THE REVEAL & ANALYSIS
    else:
        final_rank = 100 - st.session_state.ranks[idx]
        best_score = max(scores)
        best_idx = list(scores).index(best_score) + 1
        
        st.success("### ✅ BOOKING COMPLETE")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Your Venue Rank", f"#{final_rank}")
        c2.metric("Target #1 Score", f"{best_score:,}")
        c3.metric("Target #1 Position", f"Venue {best_idx}")

        # DEBRIEF MESSAGES (Specification 4)
        st.divider()
        if final_rank == 1:
            st.balloons()
            st.info("🏆 **PERFECT FIND!** Your strategy was flawless this time.")
        else:
            if best_idx <= k:
                st.error(f"❌ **UNLUCKY:** The best venue was at Position {best_idx}. You were still in Research—it was impossible to catch.")
            elif best_idx < (idx + 1):
                st.warning(f"⚠️ **MISSED:** The best venue was at Position {best_idx}. Your benchmark was too low or your leap was too early.")
            else:
                st.warning(f"📉 **MISSED:** The best venue was at Position {best_idx}. You settled for Rank #{final_rank} before you ever reached the best one.")

else:
    st.info("👈 Use the sidebar to set your N-Cutoff and start a Practice Hunt.")

# --- FOOTER ---
st.markdown("---")
st.caption("Applied Statistics Competitions | Venue Lab v3.0 | Training Mode")

# --- SOURCE CODE PADDING (FOR EDITOR COMFORT) ---
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
