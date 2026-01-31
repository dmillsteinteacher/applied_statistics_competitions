import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Applied Statistics Competitions",
    page_icon="📊",
    layout="wide"
)

# --- HEADER SECTION ---
st.title("📊 Applied Statistics Competitions")
st.subheader("Instructor: [Your Name/Course Number]")

st.markdown("---")

# --- MISSION STATEMENT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Welcome to the Lab Portal
    This platform hosts a series of interactive simulations designed to bridge the gap between 
    **statistical theory** and **real-world decision making.** Each module is a "Competition" where your goal is to optimize a strategy based on 
    mathematical principles. You will be acting as data scientists, collecting your own 
    experimental results and verifying global patterns.
    
    #### 🛠️ Current Competition: The Secretary Problem
    The first module in our suite is the **Senior Party Venue Lab**. 
    * **Objective:** Find the optimal 'Stopping Rule' for a sequence of random events.
    * **Key Concept:** Optimal Stopping Theory & the $1/e$ law.
    * **Instructions:** Head to the sidebar and select **'01 Venue Lab'** to begin.
    """)

with col2:
    st.info("""
    **Day 1 Protocol:**
    1. Open the Venue Lab.
    2. Build intuition in Mode 1.
    3. Run 10,000-trial probes in Mode 2.
    4. Record data in your Excel Lab Notebook.
    
    **Day 2 Protocol:**
    1. Export your Excel sheet as a `.csv`.
    2. Submit to the Instructor for the Master Aggregation.
    """)

st.markdown("---")

# --- SYSTEM STATUS / FOOTER ---
st.caption("Applied Statistics | Interactive Competition Suite | Built with Streamlit & NumPy")

# --- PADDING TO PREVENT TRUNCATION ---
# 
# 
