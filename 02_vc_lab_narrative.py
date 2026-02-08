# 02_vc_lab_narrative.py

MARKET_STORIES = {
    "Market A: The Boom": "Capital is plentiful and exit multiples are high.",
    "Market B: The Squeeze": "Liquidity is tightening; efficiency is key.",
    "Market C: Rule Change": "New regulations have shifted the landscape."
}

TYPE_STORY = {
    "Type 1: The Basics": "Proven business models with steady growth.",
    "Type 2: Tech Apps": "High-growth software ventures.",
    "Type 3: Big Science": "High-cap-ex, high-reward ventures."
}

P_MATRIX = {
    "Market A: The Boom": {"Type 1: The Basics": 0.65, "Type 2: Tech Apps": 0.45, "Type 3: Big Science": 0.25},
    "Market B: The Squeeze": {"Type 1: The Basics": 0.40, "Type 2: Tech Apps": 0.25, "Type 3: Big Science": 0.10},
    "Market C: Rule Change": {"Type 1: The Basics": 0.50, "Type 2: Tech Apps": 0.35, "Type 3: Big Science": 0.15}
}

# RESTORED REALISTIC B-VALUES
B_VALS = {
    "Type 1: The Basics": 0.5,
    "Type 2: Tech Apps": 2.0,
    "Type 3: Big Science": 8.0
}

MEMO_TEMPLATE = """
### 🛡️ INTERNAL AUDIT REPORT
**Target Sector:** {sector} | **Market:** {market}

* **Execution Failure Rate:** {ef}
* **Market Friction Rate:** {mf}

Verify the observed success rate (p) to proceed.
"""
