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

def run_simulation(f, p, b, n_steps=50):
    """Runs a SINGLE wealth simulation path."""
    path = [100.0]
    for t in range(n_steps):
        current_w = path[-1]
        if current_w <= 1.0:
            path.append(0.0)
            continue
        
        win = np.random.random() < p
        bet = current_w * f
        
        if win:
            path.append(current_w + (bet * b))
        else:
            path.append(current_w - bet)
            
    return np.array(path)

# --- END OF ENGINE FILE ---
