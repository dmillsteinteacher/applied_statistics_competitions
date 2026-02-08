import numpy as np

def run_audit(mkt, sec, p_true):
    """Generates counts using keys 'n', 'ef', and 'mf' for the memo."""
    n = 200
    # Add minor noise so every audit feels unique
    expected_p = p_true + np.random.normal(0, 0.01)
    success_count = int(n * np.clip(expected_p, 0.05, 0.95))
    total_failures = n - success_count
    
    # Randomly split failures into Operational (ef) and Market (mf)
    ef = int(total_failures * np.random.uniform(0.4, 0.6))
    mf = total_failures - ef
    
    # This is the actual value the student must calculate
    p_observed = success_count / n
    
    return {
        "n": n,
        "ef": ef,
        "mf": mf,
        "p_observed": round(p_observed, 3)
    }

def simulate_career(p_val, n_deals=100):
    """Simulates a deal sequence for Stage 2 visualization."""
    raw = np.random.random(n_deals) < p_val
    max_streak, current_streak = 0, 0
    for outcome in raw:
        if not outcome:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return {"Wins": int(np.sum(raw)), "Max_Streak": max_streak, "raw": raw.tolist()}

def run_simulation(f, p, b, n_steps=50, n_sims=100):
    """Core wealth simulation for Stage 3 sizing."""
    history = np.zeros((n_sims, n_steps + 1))
    history[:, 0] = 100.0
    for i in range(n_sims):
        for t in range(n_steps):
            if history[i, t] <= 1.0:
                history[i, t+1] = 0.0
                continue
            win = np.random.random() < p
            payoff = b if win else 0.0
            bet = history[i, t] * f
            history[i, t+1] = (history[i, t] - bet) + (bet * payoff)
    
    final_vals = history[:, -1]
    return {
        "Median": np.median(final_vals),
        "Insolvency Rate": np.sum(final_vals <= 1.0) / n_sims,
        "History": history
    }

# --- END OF ENGINE FILE ---
