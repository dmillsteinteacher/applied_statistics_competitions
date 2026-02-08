# 02_vc_lab_narrative.py

# 1. Success probabilities (p) mapped to Market and Sector
P_MATRIX = {
    "Market A: The Boom": {
        "Type 1: The Basics": 0.65,
        "Type 2: Deep Tech": 0.45,
        "Type 3: Moonshots": 0.25
    },
    "Market B: The Squeeze": {
        "Type 1: The Basics": 0.40,
        "Type 2: Deep Tech": 0.25,
        "Type 3: Moonshots": 0.10
    },
    "Market C: Stagnation": {
        "Type 1: The Basics": 0.50,
        "Type 2: Deep Tech": 0.35,
        "Type 3: Moonshots": 0.15
    }
}

# 2. Payback multiples (b) per sector
B_VALS = {
    "Type 1: The Basics": 3.0,
    "Type 2: Deep Tech": 8.0,
    "Type 3: Moonshots": 25.0
}

# 3. The function that generates the flavor text for Tab 1
def generate_memo(sector, market):
    """
    Creates the internal audit text based on the chosen sector and market.
    """
    # Safety lookup
    p_est = P_MATRIX.get(market, {}).get(sector, 0.5)
    b_val = B_VALS.get(sector, 1.0)
    
    memo_text = f"""
    ### STRATEGIC AUDIT: {sector.upper()}
    **Market Condition:** {market}
    **Subject:** Internal Probability Assessment
    
    Our proprietary analysis of {market} suggests a baseline success rate 
    of approximately **{p_est:.0%}** for {sector} investments. 
    
    Historical data for this sector indicates a successful exit typically 
    yields a **{b_val}x** return on invested capital. 
    
    *Confidentiality Notice: This data is for internal simulation use only.*
    """
    return memo_text

# --- EOF PADDING ---
