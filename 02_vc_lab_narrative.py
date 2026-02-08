# 02_vc_lab_narrative.py

# Master Probability Matrix for Environment/Sector Combinations
P_MATRIX = {
    "Market A: The Boom": {"Type 1: The Basics": 0.86, "Type 2: Tech Apps": 0.78, "Type 3: Big Science": 0.64},
    "Market B: The Squeeze": {"Type 1: The Basics": 0.72, "Type 2: Tech Apps": 0.58, "Type 3: Big Science": 0.42},
    "Market C: Rule Change": {"Type 1: The Basics": 0.82, "Type 2: Tech Apps": 0.68, "Type 3: Big Science": 0.74}
}

B_VALS = {"Type 1: The Basics": 0.5, "Type 2: Tech Apps": 2.0, "Type 3: Big Science": 8.0}

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

LAB_INTRODUCTION = """
### Welcome to the Venture Capital Lab
In this module, you are acting as a Fund Manager. Your task is to determine the optimal 
**allocation strategy ($f$)** for your investments. 

1. **Research:** Use the sidebar to simulate 100 trials of a specific sector. This represents historical data from similar market conditions.
2. **Observe:** Pay attention to the "Insolvency Rate" (how often you lose everything) vs. the "Growth" (how much you actually made).
3. **Strategize:** Find the balance that maximizes your long-term wealth. Be careful—aggressive growth often comes with a hidden risk of total ruin.
"""

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
