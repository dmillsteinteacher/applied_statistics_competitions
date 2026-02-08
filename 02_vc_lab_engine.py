import numpy as np

def run_simulation(f, p, b, initial_wealth=1000, n_sims=100, n_steps=50):
    # Matrix to store wealth at every step: rows = sims, cols = time steps
    history = np.zeros((n_sims, n_steps + 1))
    history[:, 0] = initial_wealth

    for s in range(n_sims):
        wealth = initial_wealth
        for t in range(1, n_steps + 1):
            if wealth < 1.0:
                wealth = 0
            else:
                bet_size = f * wealth
                if np.random.random() < p:
                    wealth += (bet_size * b)
                else:
                    wealth -= bet_size
            history[s, t] = wealth

    return {
        "Median": float(np.median(history[:, -1])),
        "Insolvency Rate": float(np.mean(history[:, -1] <= 1.0)),
        "History": history  # Crucial: returns the full 2D array
    }
