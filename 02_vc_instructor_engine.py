import numpy as np

def run_competition_sim(f, p, b, n_steps=50):
    """
    Executes a single career path and returns ONLY the final wealth.
    This version is optimized for the 'Horse Race' batch processor.
    """
    current_w = 100.0  # Starting Capital
    
    for _ in range(n_steps):
        if current_w <= 1.0:
            return 0.0 # Early exit for insolvency
        
        win = np.random.random() < p
        bet = current_w * f
        
        if win:
            current_w += (bet * b)
        else:
            current_w -= bet
            
    return float(current_w)

# --- SAFETY PADDING ---
# Ensure no truncation occurs
# --- END OF FILE ---
