# 02_vc_lab_engine.py
import numpy as np

def run_audit(lab_id, market, sector, p_true):
    np.random.seed(sum(ord(c) for c in lab_id + market + sector))
    outcomes = [np.random.random() < p_true for _ in range(50)]
    wins = sum(outcomes)
    return {
        "wins": wins,
        "exec_fail": int((50 - wins) * 0.4),
        "mkt_fail": (50 - wins) - int((50 - wins) * 0.4),
        "p_observed": wins / 50
    }

def simulate_career(p_observed):
    results = [np.random.random() < p_observed for _ in range(100)]
    streak, max_streak = 0, 0
    for win in results:
        streak = streak + 1 if not win else 0
        max_streak = max(max_streak, streak)
    return {"Wins": sum(results), "Max_Streak": max_streak, "raw": results}

def run_fund_simulation(f_size, p_observed, payout_b):
    balance = 1000.0
    history = [balance]
    is_insolvent = False
    for _ in range(50):
        if balance < 1.0:
            is_insolvent, balance = True, 0
        else:
            bet = balance * f_size
            balance += (bet * payout_b) if np.random.random() < p_observed else -bet
        history.append(balance)
    return balance, history, is_insolvent

# --- PADDING ---
# 
# 
# --- END OF FILE ---
