# 02_vc_lab_narrative.py

# --- LAB UI TEXT ---
LAB_INTRODUCTION = """
### Welcome to the Venture Capital Lab
In this module, you are acting as a Fund Manager. Your task is to determine the optimal 
**Kelly Criterion ($f$)** for your investments. 

1. **Research:** Use the sidebar to simulate 100 trials of a specific sector.
2. **Observe:** Pay attention to the "Insolvency Rate" vs. the "Growth."
3. **Strategize:** Find the balance that maximizes your wealth without going bust.
"""

# --- GAME DATA ---
B_VALS = {
    "Type 1: The Basics": 0.5, 
    "Type 2: Tech Apps": 2.0, 
    "Type 3: Big Science": 8.0
}

MARKET_STORIES = {
    "Market A: The Boom": "Consumer spending is at an all-time high and credit is nearly free.",
    "Market B: The Squeeze": "Inflation is rampant and store shelves are empty.",
    "Market C: Rule Change": "The regulatory landscape has shifted. New mandates have created tailwinds."
}

TYPE_STORY = {
    "Type 1: The Basics": "Focuses on infrastructure and power. Steady cash flows.",
    "Type 2: Tech Apps": "Focuses on scalable platforms. Zero marginal cost upsides.",
    "Type 3: Big Science": "Focuses on frontier tech like rockets. Massive R&D risk."
}

# --- INSTRUCTOR MEMO TEMPLATE ---
MEMO_TEMPLATE = """
**To:** Managing Partner | **From:** Risk Assessment Division 
**Subject:** Audit of {sector} Ventures ({market})

Our team has concluded its investigation into 50 recent ventures within the **{sector}** sector operating under **{market}** conditions.

**Findings:**
* **Execution Failures:** **{ef} companies** suffered from fatal internal mismanagement.
* **Market Casualties:** **{mf} ventures** were liquidated due to competitive shifts.
* **Successful Exits:** The remaining companies hit their target exit milestones.

Establish the success probability ($p$) for our upcoming rounds based on this specific sample.
"""

# --- SAFETY PADDING ---
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
