# 02_vc_lab_narrative.py

# 1. Used for the Sidebar Dropdown and Intelligence Briefing
MARKET_STORIES = {
    "Market A: The Boom": "Capital is plentiful and exit multiples are at record highs. A 'rising tide' environment.",
    "Market B: The Squeeze": "Liquidity is tightening. Only the most capital-efficient firms are reaching exit.",
    "Market C: Rule Change": "New regulations have shifted the landscape, creating uncertainty but also niche opportunities."
}

# 2. Used for the Sidebar Dropdown and Intelligence Briefing
TYPE_STORY = {
    "Type 1: The Basics": "Proven business models with steady, predictable growth and lower risk.",
    "Type 2: Tech Apps": "High-growth software ventures. Scalable, but sensitive to market sentiment.",
    "Type 3: Big Science": "High-cap-ex, high-reward ventures. Long timelines with binary outcomes."
}

# 3. Success probabilities (p) mapped to Market and Sector
# Note: These are the 'true' underlying probabilities
P_MATRIX = {
    "Market A: The Boom": {
        "Type 1: The Basics": 0.65,
        "Type 2: Tech Apps": 0.45,
        "Type 3: Big Science": 0.25
    },
    "Market B: The Squeeze": {
        "Type 1: The Basics": 0.40,
        "Type 2: Tech Apps": 0.25,
        "Type 3: Big Science": 0.10
    },
    "Market C: Rule Change": {
        "Type 1: The Basics": 0.50,
        "Type 2: Tech Apps": 0.35,
        "Type 3: Big Science": 0.15
    }
}

# 4. Payback multiples (b) per sector
B_VALS = {
    "Type 1: The Basics": 3.0,
    "Type 2: Tech Apps": 8.0,
    "Type 3: Big Science": 25.0
}

# 5. Template for the Stage 1 Audit Report
# The Lab script uses .format(ef=..., mf=..., sector=..., market=...)
MEMO_TEMPLATE = """
### 🛡️ INTERNAL AUDIT REPORT
**Target Sector:** {sector}
**Market Condition:** {market}

Our analysts have performed a look-back on similar vintages. 
* **Execution Failure Rate:** {ef}
* **Market Friction Rate:** {mf}

Based on these combined friction points, please calculate the observed success rate (p) 
to proceed with capital sizing.
"""

# --- EOF ---
