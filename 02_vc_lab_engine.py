import numpy as np

def run_simulation(f, p, b, initial_wealth=1000, n_sims=100, n_steps=50):
    # Matrix to store wealth at every step for every simulation
    # (n_sims rows, n_steps columns)
    history = np.zeros((n_sims, n_steps + 1))
    history[:, 0] = initial_wealth

    for s in range(n_sims):
        wealth = initial_wealth
        for t in range(1, n_steps + 1):
            if wealth < 1.0:
                wealth = 0.0
            else:
                bet_size = f * wealth
                if np.random.random() < p:
                    wealth += (bet_size * b)
                else:
                    wealth -= bet_size
            history[s, t] = wealth

    final_results = history[:, -1]
    
    return {
        "Median": float(np.median(final_results)),
        "Insolvency Rate": float(np.mean(final_results <= 1.0)),
        "History": history  # <--- THIS IS THE NEW ADDITION
    }
