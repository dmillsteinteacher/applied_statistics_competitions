import streamlit as st
import numpy as np
import random
import time

# --- CONFIGURATION & UI SETUP ---
st.set_page_config(page_title="Senior Party Venue Lab", layout="wide")

# Custom CSS for a clean, academic-yet-engaging vibe
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { border-radius: 8px; height: 3em; font-weight: bold; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    </style>
    """, unsafe_allow_html=True)

# --- DYNAMIC DESCRIPTION GENERATOR ---
def get_dynamic_description(rank):
    """Generates a fresh description based on rank (0-99). 99 is best."""
    tiers = {
        "low": { # Ranks 0-30
            "adj": ["A damp", "A suspicious", "A cramped", "An abandoned", "A smelly", "A drafty", "A cluttered"],
            "noun": ["basement", "parking lot", "garage", "storage unit", "backyard", "alleyway", "cafeteria annex"]
        },
        "mid": { # Ranks 31-80
            "adj": ["A standard", "A functional", "A typical", "A clean", "A basic", "A respectable", "An unremarkable"],
            "noun": ["community center", "hotel side-room", "pizza parlor", "office lounge", "clubhouse", "bowling alley"]
        },
        "high": { # Ranks 81-98
            "adj": ["A stylish", "A premium", "An elegant", "A trendy", "A spacious", "A sleek", "A sophisticated"],
            "noun": ["loft", "rooftop terrace", "ballroom", "historic mansion", "modern lounge", "garden estate"]
        },
        "top": { # Rank 99
            "adj": ["The ultimate", "A legendary", "A world-class", "A breathtaking", "The premier", "An elite"],
            "noun": ["VIP penthouse", "waterfront estate", "private island club", "grand royal hall", "luxury skyscraper suite"]
        }
    }

    if rank < 31: tier = "low"
    elif rank < 81: tier = "mid"
    elif rank < 99: tier = "high"
    else: tier = "top"

    return f"{random.choice(tiers[tier]['adj'])} {random.choice(tiers[tier]['noun'])}"

# --- APP LOGIC ---
st.title("🏰 The Senior Party Venue Lab")
st.markdown("""
### The Narrative
You are the lead organizer for the **Senior Graduation Party**. There are **100 venues** available to view. 
You see them one at a time. Once you pass a venue, it is booked by another school and **gone forever**.

**Your Objective:** Find the **#1 "Ultimate" Venue** (the 100th percentile).
""")

tab1, tab2 = st.tabs(["🎯 Mode 1: The Manual Hunt", "🔬 Mode 2: The Data Factory"])

# --- TAB 1: MANUAL HUNT (Intuition Builder) ---
with tab1:
    st.header("Mode 1: The Manual Hunt")
    st.info("**Instructions:** Use the 'Research Phase' to set a benchmark. In the 'Selection Phase', the app will automatically stop at the first venue that beats your benchmark.")

    # State management for game persistence
    if 'manual_scores' not in st.session_state:
        st.session_state.manual_scores = None
        st.session_state.manual_ranks = None
        st.session_state.manual_descs = None

    col1, col2 = st.columns([1, 2])

    with col1:
        k_percent = st.slider("Research Cutoff % (The 'Look' Phase)", 1, 99, 37)
        if st.button("Generate New Game (Shift Hype Scales)"):
            # Shifting Scale Logic: Randomly set the order of magnitude
            power = np.random.choice([10, 100, 1000, 10000])
            base_min = np.random.randint(1, 100) * power
            base_max = base_min + (np.random.randint(200, 800) * power)
            
            # Generate 100 unique scores
            raw_scores = np.random.choice(range(base_min, base_max + 200), 100, replace=False)
            
            # Map ranks 0-99 (99 is best)
            sorted_indices = np.argsort(raw_scores)
            ranks = np.zeros(100, dtype=int)
            ranks[sorted_indices] = np.arange(100)
            
            # Generate fresh descriptions for THIS run only
            st.session_state.manual_descs = [get_dynamic_description(r) for r in ranks]
            st.session_state.manual_scores = raw_scores
            st.session_state.manual_ranks = ranks

    with col2:
        if st.session_state.manual_scores is not None:
            scores = st.session_state.manual_scores
            ranks = st.session_state.manual_ranks
            descs = st.session_state.manual_descs
            
            st.write(f"### Hunt Active (Hype Range: {min(scores):,} — {max(scores):,})")
            
            # Benchmark from Look Phase
            look_phase_scores = scores[:k_percent]
            benchmark = max(look_phase_scores)
            st.warning(f"**Research Phase (1-{k_percent}) Complete.** Benchmark to beat: **{benchmark:,}**")
            
            found = False
            selected_idx = -1
            
            with st.status("Reviewing Selection Phase Venues...", expanded=True) as status:
                for i in range(k_percent, 100):
                    current_score = scores[i]
                    current_desc = descs[i]
                    
                    st.write(f"Venue #{i+1}: **{current_score:,}** — *{current_desc}*")
                    time.sleep(0.08) # Tension delay
                    
                    if current_score > benchmark:
                        selected_idx = i
                        found = True
                        status.update(label="✅ CRITERIA MET: VENUE BOOKED!", state="complete")
                        break
                
                if not found:
                    selected_idx = 99 
                    status.update(label="❌ NO SUPERIOR VENUE FOUND. Settled for the final option.", state="error")

            # THE REVEAL
            st.divider()
            final_rank_display = 100 - ranks[selected_idx] # Convert 0-99 rank to 1-100 (1 is best)
            
            c1, c2 = st.columns(2)
            c1.metric("Selected Venue Score", f"{scores[selected_idx]:,}")
            c2.metric("True Rank", f"Rank #{final_rank_display}")
            
            st.write(f"**Final Booking:** {descs[selected_idx]}")

            if final_rank_display == 1:
                st.balloons()
                st.success("🎉 MISSION ACCOMPLISHED! You found the absolute best venue!")
            elif final_rank_display <= 5:
                st.info(f"Excellent! You found the #{final_rank_display} venue. A top-tier choice!")
            else:
                st.error(f"Regret. The #1 Venue was worth {max(scores):,}. You missed it!")

# --- TAB 2: DATA FACTORY (Simulation Mode) ---
with tab2:
    st.header("Mode 2: The Data Factory")
    st.markdown("""
    **The Statistical Lab:** Run 10,000 automated trials to test your 'Stopping Rule' reliability.
    The computer will record a **Win** only if it finds the True #1 Venue (Rank 100).
    """)

    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        sim_k = st.number_input("Set Cutoff Percentage", 1, 99, 37)
        if st.button("Run 10,000 Trials"):
            with st.spinner("Processing 1,000,000 candidates..."):
                # VECTORIZED NUMPY ENGINE
                trials = 10000
                n = 100
                
                # Generate unique random ranks (0.0 to 1.0) for 10,000 experiments
                data = np.random.rand(trials, n)
                
                # Identify the benchmark (max of the 'Look' phase)
                look_phase = data[:, :sim_k]
                benchmarks = np.max(look_phase, axis=1)
                
                # Identify potential picks in the 'Leap' phase
                leap_phase = data[:, sim_k:]
                mask = leap_phase > benchmarks[:, np.newaxis]
                
                # Logic: Find the first True in the mask
                win_exists = np.any(mask, axis=1)
                first_win_idx = np.argmax(mask, axis=1)
                
                # The index we actually picked
                picks = np.where(win_exists, sim_k + first_win_idx, n - 1)
                
                # The actual max index in each trial
                actual_max_indices = np.argmax(data, axis=1)
                
                # Did our pick match the global max?
                wins = (picks == actual_max_indices)
                success_rate = np.mean(wins) * 100

                st.session_state.sim_result = f"Strategy **{sim_k}%** Success Rate: **{success_rate:.2f}%**"

    with col_b:
        if 'sim_result' in st.session_state:
            st.subheader("Latest Result")
            st.write(st.session_state.sim_result)
            st.markdown("---")
            st.warning("**LAB NOTE:** This result is not saved. You must manually record the Cutoff and Success Rate in your Excel spreadsheet for submission.")

st.sidebar.markdown("### Lab Protocol")
st.sidebar.write("1. Use Mode 1 to build your 'gut' feeling.")
st.sidebar.write("2. Use Mode 2 to gather statistical evidence.")
st.sidebar.write("3. Map the peak success rate in Excel.")

# --- PADDING TO PREVENT TRUNCATION ---
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
# 
# 
# --- END OF FILE ---
