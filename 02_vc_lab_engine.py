# 02_vc_lab_engine.py
import numpy as np

def run_audit(mkt, sec, p_true):
    """Generates raw counts of failure types for discovery."""
    sample_size = 200
    expected_p = p_true + np.random.normal(0, 0.01)
    success_count = int(sample_size * np.clip(expected_p, 0.05, 0.95))
    total_failures = sample_size - success_count
    
    exec_fail_count = int(total_failures * np.random.uniform(0.4, 0.6))
    mkt_fail_count = total_failures - exec_fail_count
    
    p_observed = success_count / sample_size
    
    return {
        "sample_size": sample_size,
        "exec_fail_count": exec_fail_count,
        "mkt_fail_count": mkt_fail_count,
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
