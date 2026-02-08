import numpy as np

def run_audit(mkt, sec, p_true):
    """
    Generates a simulated audit report. 
    Now matches the call: eng.run_audit(mkt, sec, p_true)
    """
    # Simulate components of failure that add up to the 'true' p
    # This is flavor text for the memo
    ef = round(np.random.uniform(0.05, 0.15), 2)
    mf = round((1 - p_true) - ef, 2)
    
    return {
        "exec_fail": f"{ef:.1%}",
        "mkt_fail": f"{mf:.1%}",
        "p_observed": round(p_true, 2)
    }

def simulate_career(p_val, n_deals=100):
    """Simulates a sequence of wins/losses for Stage 2."""
    raw = np.random.random(n_deals) < p_val
    wins = int(np.sum(raw))
    
    # Calculate max streak of 0s (failures)
    max_streak = 0
    current_streak = 0
    for outcome in raw:
        if not outcome:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
            
    return {
        "Wins": wins,
        "Max_Streak": max_streak,
        "raw": raw.tolist()
    }

def run_simulation(f, p, b, n_steps=50, n_sims=100):
    """The core math for Stage 3 sizing."""
    history = np.zeros((n_sims, n_steps + 1))
    history[:, 0] = 100.0  # Starting wealth
    
    for i in range(n_sims):
        for t in range(n_steps):
            if history[i, t] <= 1.0: # Insolvency check
                history[i, t+1] = 0.0
                continue
                
            win = np.random.random() < p
            payoff = b if win else 0.0
            
            # Reinvestment logic
            bet = history[i, t] * f
            history[i, t+1] = (history[i, t] - bet) + (bet * payoff)
            
    final_vals = history[:, -1]
    insolvent_count = np.sum(final_vals <= 1.0)
    
    return {
        "Median": np.median(final_vals),
        "Insolvency Rate": insolvent_count / n_sims,
        "History": history
    }
