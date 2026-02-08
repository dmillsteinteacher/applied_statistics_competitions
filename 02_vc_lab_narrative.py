MARKET_STORIES = {
    "Market A: The Boom": "Capital is plentiful and exit multiples are at record highs.",
    "Market B: The Squeeze": "Liquidity is tightening. Only the most efficient reach exit.",
    "Market C: Rule Change": "New regulations have created niche uncertainty."
}

TYPE_STORY = {
    "Type 1: The Basics": "Proven business models with steady growth.",
    "Type 2: Tech Apps": "High-growth software ventures. Scalable but sensitive.",
    "Type 3: Big Science": "High-cap-ex, long timelines with binary outcomes."
}

P_MATRIX = {
    "Market A: The Boom": {"Type 1: The Basics": 0.65, "Type 2: Tech Apps": 0.45, "Type 3: Big Science": 0.25},
    "Market B: The Squeeze": {"Type 1: The Basics": 0.40, "Type 2: Tech Apps": 0.25, "Type 3: Big Science": 0.10},
    "Market C: Rule Change": {"Type 1: The Basics": 0.50, "Type 2: Tech Apps": 0.35, "Type 3: Big Science": 0.15}
}

B_VALS = {
    "Type 1: The Basics": 0.5,
    "Type 2: Tech Apps": 2.0,
    "Type 3: Big Science": 8.0
}

MEMO_TEMPLATE = """
### 🛡️ INTERNAL AUDIT: RAW DATA RETRIEVAL
**Project:** {sector} Historical Performance  
**Environment:** {market}

Our research team reviewed **{n}** past deal attempts in similar conditions. Here are the findings:

* **Executive/Operational Failures:** {ef} cases
* **Market/Macro Failures:** {mf} cases

---
**TASK:** Based on these findings, calculate the **Probability of Success (p)** for the remaining cases in this set. 
*(Hint: Successes = Total cases minus all failures)*
"""
