# 02_vc_lab_engine.py
import numpy as np

def run_audit(mkt, sec, p_true):
    total_failure = 1.0 - p_true
    ef_val = total_failure * np.random.uniform(0.3, 0.5)
    mf_val = total_failure - ef_val
    return {
        "exec_fail": f"{ef_val:.1%}",
        "mkt_fail": f"{mf_val:.1%}",
        "p_observed": round(p_true, 2)
    }

def simulate_career(p_val, n_deals=100):
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
    return {
        "Median": np.median(history[:, -1]),
        "Insolvency Rate": np.sum(history[:, -1] <= 1.0) / n_sims,
        "History": history
    }
