"""Generate synthetic Northfield FC datasets for the workshop.

Run:
    python data/_generate.py

This overwrites the CSVs in data/. You do not normally need to run this -
the CSVs are committed. It exists so you can regenerate cleanly if someone
corrupts a file during a lesson.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

DATA = Path(__file__).parent

# ------------------------------------------------------------------
# Squad roster
# ------------------------------------------------------------------
POSITIONS = ["GK", "CB", "FB", "CM", "WM", "FW"]
SQUADS = {
    "U23": 22,
    "U18": 20,
    "U16": 18,
}

roster: list[dict] = []
player_num = 1
for squad, n in SQUADS.items():
    for _ in range(n):
        pid = f"NF{player_num:03d}"
        pos = random.choices(POSITIONS, weights=[1, 3, 3, 4, 3, 3])[0]
        birth_year = {"U23": 2002, "U18": 2007, "U16": 2009}[squad] + random.randint(-1, 1)
        roster.append({
            "player_id": pid,
            "squad": squad,
            "position": pos,
            "birth_year": birth_year,
        })
        player_num += 1

with (DATA / "squad_roster.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["player_id", "squad", "position", "birth_year"])
    w.writeheader()
    w.writerows(roster)

# ------------------------------------------------------------------
# GPS training data - this week, messy
# ------------------------------------------------------------------
# Three pitch sessions this week: Mon, Wed, Fri.
# Shape per-row: one row per player per session.
# Messy quirks we deliberately seed:
#   - Mixed date formats (ISO vs dd/mm/yyyy vs text)
#   - Trailing whitespace on player_id
#   - Inconsistent casing of session_type
#   - Missing max_speed_ms for one whole session (unit firmware glitch)
#   - A duplicate row (same player, same session)
#   - Two rows where total_distance_m is clearly an outlier (unit strap came off)
#   - Empty rows at the bottom

monday = date(2026, 4, 20)
wednesday = monday + timedelta(days=2)
friday = monday + timedelta(days=4)

sessions = [
    (monday, "Match + 1 recovery", "recovery"),
    (wednesday, "MD-3 high intensity", "high_intensity"),
    (friday, "MD-1 activation", "activation"),
]

def rough_position_load(pos: str, session_kind: str) -> tuple[float, float, float, float]:
    """Return (total_distance_m, hsr_m, sprint_m, max_speed_ms) roughly realistic."""
    base = {
        "GK": 3200,
        "CB": 6500,
        "FB": 8200,
        "CM": 9000,
        "WM": 8800,
        "FW": 7800,
    }[pos]
    mult = {"recovery": 0.55, "high_intensity": 1.15, "activation": 0.75}[session_kind]
    total = base * mult * random.uniform(0.9, 1.1)
    hsr = total * {"GK": 0.02, "CB": 0.07, "FB": 0.11, "CM": 0.10, "WM": 0.13, "FW": 0.12}[pos] * random.uniform(0.8, 1.2)
    sprint = hsr * random.uniform(0.25, 0.45)
    max_speed = {"GK": 6.8, "CB": 8.1, "FB": 9.2, "CM": 8.6, "WM": 9.4, "FW": 9.6}[pos] * random.uniform(0.92, 1.05)
    return round(total, 1), round(hsr, 1), round(sprint, 1), round(max_speed, 2)


rows = []
for sess_date, sess_label, sess_kind in sessions:
    # only U23 squad trains on all three; U18/U16 only train on Wed + Fri
    squads_today = ["U23", "U18", "U16"] if sess_kind != "recovery" else ["U23"]
    for p in roster:
        if p["squad"] not in squads_today:
            continue
        # one dropped unit: skip a random U16 player on Friday
        if sess_kind == "activation" and p["squad"] == "U16" and random.random() < 0.08:
            continue

        total, hsr, sprint, max_speed = rough_position_load(p["position"], sess_kind)

        # seed outliers
        if random.random() < 0.02:
            total *= 3.2  # strap came loose
        if random.random() < 0.03:
            max_speed = 14.8  # impossible spike - student should catch it

        # date format variance
        rnd = random.random()
        if rnd < 0.55:
            date_str = sess_date.isoformat()
        elif rnd < 0.85:
            date_str = sess_date.strftime("%d/%m/%Y")
        else:
            date_str = sess_date.strftime("%d %b %Y")

        # case variance on session type
        session_type = random.choice([sess_label, sess_label.lower(), sess_label.upper(), sess_label.title()])

        # trailing whitespace on some player_ids
        pid = p["player_id"] + (" " if random.random() < 0.2 else "")

        rows.append({
            "date": date_str,
            "session": session_type,
            "player_id": pid,
            "squad": p["squad"],
            "position": p["position"],
            "total_distance_m": total,
            "high_speed_running_m": hsr,
            "sprint_distance_m": sprint,
            "max_speed_ms": max_speed,
            "rpe": random.randint(3, 9),
        })

# knock out max_speed for the whole Wed session (firmware glitch)
for r in rows:
    if "MD-3" in r["session"].upper() or "HIGH INTENSITY" in r["session"].upper():
        if random.random() < 0.88:
            r["max_speed_ms"] = ""

# insert duplicate row
rows.append(dict(rows[5]))

# blank rows at bottom
rows.append({k: "" for k in rows[0].keys()})
rows.append({k: "" for k in rows[0].keys()})

# shuffle so duplicates and blanks are not all clustered
random.shuffle(rows)

with (DATA / "gps_training_messy.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# ------------------------------------------------------------------
# GPS training - previous week, tidy (used to compute load change)
# ------------------------------------------------------------------
prev_rows = []
prev_monday = monday - timedelta(days=7)
prev_sessions = [
    (prev_monday, "Recovery", "recovery"),
    (prev_monday + timedelta(days=2), "High intensity", "high_intensity"),
    (prev_monday + timedelta(days=4), "Activation", "activation"),
]

for sess_date, sess_label, sess_kind in prev_sessions:
    squads_today = ["U23", "U18", "U16"] if sess_kind != "recovery" else ["U23"]
    for p in roster:
        if p["squad"] not in squads_today:
            continue
        total, hsr, sprint, max_speed = rough_position_load(p["position"], sess_kind)
        prev_rows.append({
            "date": sess_date.isoformat(),
            "session": sess_label,
            "player_id": p["player_id"],
            "squad": p["squad"],
            "position": p["position"],
            "total_distance_m": total,
            "high_speed_running_m": hsr,
            "sprint_distance_m": sprint,
            "max_speed_ms": max_speed,
            "rpe": random.randint(3, 9),
        })

with (DATA / "gps_training_week_prior.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(prev_rows[0].keys()))
    w.writeheader()
    w.writerows(prev_rows)

# ------------------------------------------------------------------
# Athlete wellness - daily, last 7 days
# ------------------------------------------------------------------
wellness_rows = []
for days_back in range(7, 0, -1):
    d = date(2026, 4, 26) - timedelta(days=days_back)
    for p in roster:
        if random.random() < 0.15:
            continue  # missed a check-in
        wellness_rows.append({
            "date": d.isoformat(),
            "player_id": p["player_id"],
            "sleep_hours": round(random.uniform(6.0, 9.0), 1),
            "sleep_quality_1_5": random.randint(2, 5),
            "muscle_soreness_1_5": random.randint(1, 5),
            "stress_1_5": random.randint(1, 5),
            "mood_1_5": random.randint(2, 5),
        })

with (DATA / "athlete_wellness.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(wellness_rows[0].keys()))
    w.writeheader()
    w.writerows(wellness_rows)

# ------------------------------------------------------------------
# Strength testing - one round, current block
# ------------------------------------------------------------------
strength_rows = []
test_date = date(2026, 4, 15)
for p in roster:
    body_mass_mean = {"GK": 82, "CB": 80, "FB": 74, "CM": 72, "WM": 71, "FW": 75}[p["position"]]
    body_mass = round(body_mass_mean + random.uniform(-6, 6), 1)
    cmj = round(random.uniform(28, 48) + (5 if p["position"] in ["FW", "WM"] else 0), 1)
    squat_1rm = round(body_mass * random.uniform(1.4, 2.3), 1)
    sprint_10m = round(random.uniform(1.65, 1.95), 2)
    sprint_40m = round(sprint_10m + random.uniform(3.4, 4.1), 2)
    strength_rows.append({
        "test_date": test_date.isoformat(),
        "player_id": p["player_id"],
        "body_mass_kg": body_mass,
        "countermovement_jump_cm": cmj,
        "back_squat_1rm_kg": squat_1rm,
        "sprint_10m_s": sprint_10m,
        "sprint_40m_s": sprint_40m,
    })

with (DATA / "strength_testing.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(strength_rows[0].keys()))
    w.writeheader()
    w.writerows(strength_rows)

# ------------------------------------------------------------------
# Talent ID combine data - external prospects, not yet signed
# ------------------------------------------------------------------
combine_rows = []
for i in range(1, 41):
    pid = f"PR{i:03d}"
    pos = random.choices(POSITIONS, weights=[1, 3, 3, 4, 3, 3])[0]
    age = random.randint(15, 18)
    combine_rows.append({
        "prospect_id": pid,
        "age": age,
        "primary_position": pos,
        "height_cm": round(random.gauss(178, 7), 1),
        "body_mass_kg": round(random.gauss(70, 8), 1),
        "sprint_10m_s": round(random.uniform(1.62, 2.05), 2),
        "sprint_40m_s": round(random.uniform(5.0, 6.1), 2),
        "cmj_cm": round(random.uniform(26, 52), 1),
        "yoyo_ir1_m": random.choice([800, 880, 960, 1040, 1120, 1200, 1280, 1360, 1440, 1520, 1600, 1680, 1760]),
        "dribble_slalom_s": round(random.uniform(8.1, 11.2), 2),
        "coach_rating_1_10": random.randint(4, 10),
    })

with (DATA / "talent_id_combine.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(combine_rows[0].keys()))
    w.writeheader()
    w.writerows(combine_rows)

print(f"Wrote {len(list(DATA.glob('*.csv')))} CSVs to {DATA}")
