import numpy as np

def run_simulation(f, p, b, initial_wealth=1000, n_sims=100, n_steps=50):
    """
    Simulates VC fund growth using Kelly-style reinvestment logic.
    f: The fraction of the current fund reinvested in each round.
    p: The probability of a successful exit.
    b: The payback ratio (net profit multiple).
    """
    
    # Initialize a 2D array to store the wealth at every step for every simulation
    # Rows = Individual Simulations (n_sims)
    # Columns = Time Steps (n_steps + 1 to include the starting wealth)
    history = np.zeros((n_sims, n_steps + 1))
    history[:, 0] = initial_wealth

    for s in range(n_sims):
        wealth = initial_wealth
        for t in range(1, n_steps + 1):
            if wealth < 1.0:
                wealth = 0.0
            else:
                # Amount committed to this specific investment round
                bet_size = f * wealth
                
                # Check for success based on probability p
                if np.random.random() < p:
                    # Success: Gain the payout multiple (b * bet_size)
                    wealth += (bet_size * b)
                else:
                    # Failure: Lose the entire committed fraction
                    wealth -= bet_size
            
            # Record the result of this step in the history matrix
            history[s, t] = wealth

    # Calculate summary statistics based on the final column (the end of the sim)
    final_results = history[:, -1]
    
    return {
        "Median": float(np.median(final_results)),
        "Insolvency Rate": float(np.mean(final_results <= 1.0)),
        "Mean": float(np.mean(final_results)),
        "History": history # This allows the UI to plot the paths
    }
