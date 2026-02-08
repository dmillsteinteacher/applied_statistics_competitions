import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Applied Statistics Competitions",
    page_icon="📊",
    layout="wide"
)

# --- HEADER SECTION ---
st.title("📊 Applied Statistics Competitions")

st.markdown("---")

# --- MISSION STATEMENT ---
st.markdown("""
### Welcome to the Lab Portal
This platform hosts interactive simulations designed to bridge the gap between 
**raw data** and **decision making.** In each module, you will act as a researcher: 
collecting your own experimental results, identifying patterns in the "noise," 
and submitting a strategy to compete against your peers.

#### 🛠️ Available Modules

**1. Senior Party Venue Lab**
* **The Scenario:** You are tasked with selecting the best possible venue for a senior party. Venues are presented one by one, and once you pass on a venue, you cannot go back.
* **Objective:** Develop a strategy to maximize your chances of picking the absolute best venue in the list.
* **Status:** Active. Select **'01 Venue Lab'** in the sidebar to begin.

**2. Venture Capital Lab**
* **The Scenario:** You are a fund manager overseeing investments across different market environments and industry types. You must determine how much of your capital to risk on various opportunities.
* **Objective:** Research the success rates of different industries and calibrate your investment sizes to grow your fund over time.
* **Status:** In Development.
""")

st.markdown("---")

# --- SYSTEM STATUS / FOOTER ---
st.caption("Applied Statistics | Interactive Competition Suite | Built with Streamlit & NumPy")

# --- PADDING TO PREVENT TRUNCATION ---
# 
# 
# 
# 
# 
# 
# 
# 
# --- END OF FILE ---
