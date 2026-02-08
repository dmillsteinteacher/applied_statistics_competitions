import numpy as np

def run_simulation(f, p, b, initial_wealth=1000, n_sims=100, n_steps=20):
    """
    Simulates VC fund growth using the Kelly-style reinvestment logic.
    f: The fraction of the current fund reinvested in each round.
    p: The probability of a successful exit.
    b: The payback ratio (net profit multiple, e.g., 8.0 means you keep your 1.0 AND get 8.0 more).
    """
    # Track the final wealth of every simulated universe
    final_wealths = []

    for _ in range(n_sims):
        wealth = initial_wealth
        for _ in range(n_steps):
            if wealth < 1.0: # Fund is effectively insolvent
                wealth = 0
                break
            
            # Amount committed to the round
            bet_size = f * wealth
            
            # Outcome logic
            if np.random.random() < p:
                # Success: Gain the payout (b * bet_size)
                wealth += (bet_size * b)
            else:
                # Failure: Lose the commitment
                wealth -= bet_size
        
        final_wealths.append(wealth)

    final_wealths = np.array(final_wealths)
    
    # Return metrics for the UI to display
    return {
        "Median": float(np.median(final_wealths)),
        "Insolvency Rate": float(np.mean(final_wealths <= 1.0)),
        "Mean": float(np.mean(final_wealths))
    }
