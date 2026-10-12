#!/usr/bin/env python3
"""run-coach helper: the arithmetic a chat model tends to get wrong.

No dependencies (Python 3.8+). Every command reads JSON from a file or stdin and prints JSON.

  python3 coach.py paces    --threshold 4:40 [--lthr 165]
  python3 coach.py race     --distance-km 10 --time 45:00            (threshold pace from a result)
  python3 coach.py predict  --threshold 4:40 --distance-km 21.1      (finish time and pace window)
  python3 coach.py baseline activities.json [--today 2026-10-12]
  python3 coach.py load     activities.json --lthr 165 --max-hr 185 [--rest-hr 50] [--threshold 4:40] [--today ...]
  python3 coach.py check    weeks.json                               (hard rules and week sums)
  python3 coach.py score    rearrange.json                           (hard rules and S1-S7 cost per candidate)
  python3 coach.py coros    workout.json                             (COROS course JSON)

The numbers come from reference/rules.md and reference/sessions.md. Change them there and here together.
"""
import argparse
import datetime as dt
import json
import math
import statistics
import sys

# ---------------------------------------------------------------- shared helpers


def die(message):
    print(json.dumps({"ok": False, "error": message}))
    sys.exit(1)


def read_json(path):
    try:
        return json.load(sys.stdin if path in (None, "-") else open(path))
    except (OSError, ValueError) as error:
        die(f"could not read JSON: {error}")


def parse_pace(text):
    """'4:40' or '4:40/km' -> seconds per km."""
    text = str(text).replace("/km", "").strip()
    try:
        minutes, seconds = text.split(":")
        return int(minutes) * 60 + float(seconds)
    except ValueError:
        die(f"pace '{text}' should look like 4:40")


def parse_time(text):
    """'45:00' or '1:35:20' -> seconds."""
    parts = [float(p) for p in str(text).split(":")]
    total = 0.0
    for part in parts:
        total = total * 60 + part
    return total


def fmt_pace(sec_per_km):
    sec = int(round(sec_per_km))
    return f"{sec // 60}:{sec % 60:02d}"


def fmt_time(seconds):
    s = int(round(seconds))
    h, rest = divmod(s, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def day(text):
    return dt.date.fromisoformat(str(text)[:10])


def monday(date):
    return date - dt.timedelta(days=date.weekday())


# ---------------------------------------------------------------- paces

# Fractions of threshold SPEED (rules.md "Targets", sessions.md "Pace ranges").
PACE_ZONES = [
    ("recovery", 0.62, 0.72, "recovery jogs between reps"),
    ("easy", 0.72, 0.82, "easy runs, warm-ups, cool-downs (pace users)"),
    ("long", 0.70, 0.80, "long runs (pace users)"),
    ("steady", 0.86, 0.92, "progressive finish, marathon-pace work"),
    ("tempo", 0.94, 0.98, "tempo, the 'under' of over/unders"),
    ("hills", 0.94, 1.00, "hill reps on a road"),
    ("cruise", 0.98, 1.02, "cruise intervals"),
    ("intervals", 1.03, 1.08, "4 min reps, 800 m to 1600 m reps, pyramids, the 'over'"),
    ("fast-reps", 1.09, 1.16, "200 m and 400 m reps"),
]
HR_ZONES = [("easy and long", 0.75, 0.89), ("recovery", 0.70, 0.84)]


def pace_range(threshold_sec, low, high):
    """Fraction range of threshold speed -> (fastest, slowest) seconds per km, whole seconds."""
    return round(threshold_sec / high), round(threshold_sec / low)


def cmd_paces(args):
    threshold = parse_pace(args.threshold)
    if not 150 <= threshold <= 500:
        die("threshold pace outside 2:30 to 8:20 per km")
    zones = []
    for name, low, high, use in PACE_ZONES:
        fast, slow = pace_range(threshold, low, high)
        zones.append({"zone": name, "pace": f"{fmt_pace(fast)}-{fmt_pace(slow)}", "fastestSecPerKm": fast, "slowestSecPerKm": slow, "use": use})
    out = {"ok": True, "thresholdPace": fmt_pace(threshold), "paces": zones}
    if args.lthr:
        out["heartRate"] = [{"zone": n, "bpm": f"{round(args.lthr * lo)}-{round(args.lthr * hi)}", "minBpm": round(args.lthr * lo), "maxBpm": round(args.lthr * hi)} for n, lo, hi in HR_ZONES]
    print(json.dumps(out, indent=1))


# ---------------------------------------------------------------- race result and prediction (Riegel, exponent 1.06)

RIEGEL = 1.06


def cmd_race(args):
    distance = args.distance_km * 1000
    seconds = parse_time(args.time)
    if not 600 <= seconds <= 14400:
        die("use a race or time trial between 10 minutes and 4 hours")
    hour_distance = distance * (3600 / seconds) ** (1 / RIEGEL)
    speed = hour_distance / 3600
    if not 2.0 <= speed <= 6.5:
        die("that result gives an implausible threshold")
    print(json.dumps({"ok": True, "thresholdPace": fmt_pace(1000 / speed), "thresholdSpeedMps": round(speed, 4), "method": "Riegel, carried to a one-hour effort"}))


def cmd_predict(args):
    threshold = parse_pace(args.threshold)
    distance = args.distance_km * 1000
    seconds = 3600 * (distance / (3600 * 1000 / threshold)) ** RIEGEL
    pace = seconds / args.distance_km
    window = 0.015
    print(json.dumps({
        "ok": True,
        "predictedFinish": fmt_time(seconds),
        "goalPace": fmt_pace(pace),
        "paceWindow": f"{fmt_pace(pace * (1 - window))}-{fmt_pace(pace * (1 + window))}",
        "note": "Prediction from threshold pace on a flat course. Not valid beyond about 4 hours; pace ultras and hilly races by effort.",
    }))


# ---------------------------------------------------------------- activities

RUN_TYPES = {"Run", "TrailRun", "VirtualRun", "run", "trail", "trailrun"}


def normalise(item):
    """Strava list item (raw) or compact {date, km, min, hr?, sport?} -> one record. Names are dropped."""
    if not isinstance(item, dict) or not ("summary" in item or "date" in item):
        die("each activity needs either Strava's start_local and summary, or date, km and min")
    if "summary" in item:  # raw Strava list-activities item
        s = item["summary"]
        return {
            "date": day(item["start_local"]),
            "run": item.get("sport_type") in RUN_TYPES,
            "sport": item.get("sport_type", "Other"),
            "km": s.get("distance", 0) / 1000,
            "min": s.get("moving_time", 0) / 60,
            "speed": s.get("avg_speed"),
            "hr": item.get("average_heartrate"),
            "race": bool(item.get("isRace")),
        }
    sport = item.get("sport", "Run")
    return {
        "date": day(item["date"]),
        "run": sport in RUN_TYPES,
        "sport": sport,
        "km": float(item.get("km", 0)),
        "min": float(item.get("min", 0)),
        "speed": (float(item["km"]) * 1000 / (float(item["min"]) * 60)) if item.get("km") and item.get("min") else None,
        "hr": item.get("hr"),
        "race": bool(item.get("race")),
    }


def load_activities(path):
    data = read_json(path)
    items = data.get("activities", data) if isinstance(data, dict) else data
    return sorted((normalise(i) for i in items), key=lambda a: a["date"])


def cmd_baseline(args):
    acts = load_activities(args.file)
    today = day(args.today) if args.today else dt.date.today()
    this_week = monday(today)
    weeks = {}
    for a in acts:
        if not a["run"]:
            continue
        w = monday(a["date"])
        km, longest = weeks.get(w, (0.0, 0.0))
        weeks[w] = (km + a["km"], max(longest, a["km"]))
    full = [this_week - dt.timedelta(weeks=n) for n in range(6, 0, -1)]
    rows = [{"weekStart": w.isoformat(), "km": round(weeks.get(w, (0, 0))[0], 1), "longestKm": round(weeks.get(w, (0, 0))[1], 1)} for w in full]
    weekly = statistics.median(r["km"] for r in rows)
    longest = statistics.median(r["longestKm"] for r in rows)
    layoff = weekly < 10
    days = {}
    for a in acts:
        if a["run"] and a["date"] >= this_week - dt.timedelta(weeks=12):
            days[a["date"].strftime("%a")] = days.get(a["date"].strftime("%a"), 0) + 1
    print(json.dumps({
        "ok": True,
        "lastSixFullWeeks": rows,
        "baselineWeeklyKm": 30.0 if layoff else round(weekly, 1),
        "baselineLongRunKm": 10.0 if layoff or longest < 3 else round(longest, 1),
        "layoff": layoff,
        "runDaysLast12Weeks": days,
        "rule": "median of the last 6 complete Monday-Sunday weeks; under 10 km a week is a layoff (start from 30 km and a 10 km long run)",
    }, indent=1))


# ---------------------------------------------------------------- load, fitness, fatigue, form

ASSUMED_IF = {"walk": 0.45, "hike": 0.55, "ride": 0.60, "strength": 0.50, "other": 0.50}


def trimp_per_min(r):
    return r * 0.64 * math.exp(1.92 * r)


def activity_load(a, lthr, max_hr, rest_hr, threshold_speed):
    hours = a["min"] / 60
    if hours <= 0:
        return 0.0, "none"
    if a["hr"] and lthr and max_hr and rest_hr < a["hr"] and rest_hr < lthr <= max_hr:
        r = min(1.0, max(0.0, (a["hr"] - rest_hr) / (max_hr - rest_hr)))
        r_lthr = (lthr - rest_hr) / (max_hr - rest_hr)
        return 100 * trimp_per_min(r) * a["min"] / (60 * trimp_per_min(r_lthr)), "avg-hr-trimp"
    if a["run"] and threshold_speed and a["speed"]:
        return 100 * hours * (a["speed"] / threshold_speed) ** 2, "pace-rtss"
    if a["run"]:
        effort = 0.95 if a["race"] else 0.65 if a["min"] >= 90 else 0.70
    else:
        effort = ASSUMED_IF.get(str(a["sport"]).lower(), 0.50)
    return 100 * hours * effort ** 2, "assumed-intensity"


def cmd_load(args):
    acts = load_activities(args.file)
    if not acts:
        die("no activities")
    today = day(args.today) if args.today else dt.date.today()
    threshold_speed = 1000 / parse_pace(args.threshold) if args.threshold else None
    rest = args.rest_hr or 55
    per_day, methods = {}, {}
    for a in acts:
        value, method = activity_load(a, args.lthr, args.max_hr, rest, threshold_speed)
        per_day[a["date"]] = per_day.get(a["date"], 0) + value
        methods[method] = methods.get(method, 0) + 1
    warnings = [f"{methods['none']} activities had no moving time (min), so they count as zero load"] if methods.get("none") else []
    start = acts[0]["date"]
    kc, ka = math.exp(-1 / 42), math.exp(-1 / 7)
    ctl = atl = 0.0
    series, d = [], start
    while d <= today:
        form = ctl - atl  # yesterday's CTL minus yesterday's ATL
        load = per_day.get(d, 0.0)
        ctl = ctl * kc + load * (1 - kc)
        atl = atl * ka + load * (1 - ka)
        series.append({"date": d.isoformat(), "load": round(load, 1), "fitness": round(ctl, 1), "fatigue": round(atl, 1), "form": round(form, 1)})
        d += dt.timedelta(days=1)
    days_of_series = len(series)
    settled = days_of_series >= 42
    low_form = settled and len(series) >= 3 and all(s["form"] < -30 for s in series[-3:])
    ramp = series[-1]["fitness"] - series[-8]["fitness"] if len(series) >= 8 else 0
    flags = []
    if settled and low_form:
        flags.append("form-too-low: form below -30 for 3 days")
    if settled and ramp > 7:
        flags.append(f"fitness-ramp-too-high: fitness up {ramp:.1f} in a week")
    print(json.dumps({
        "ok": True,
        "latest": series[-1],
        "fitnessUpLast7Days": round(ramp, 1),
        "seriesDays": days_of_series,
        "settled": settled,
        "note": None if settled else "Under 42 days of history: fitness numbers are still settling, fatigue rules are held.",
        "flags": flags,
        "loadMethods": methods,
        "warnings": warnings,
        "restHrAssumed": args.rest_hr is None,
        "last14Days": series[-14:],
    }, indent=1))


# ---------------------------------------------------------------- week check (hard rules H1-H7, gaps, easy share, caps)

HARD = {"tempo", "intervals", "hills", "long", "race"}
KEY = {"tempo", "intervals", "hills", "long"}
EASY_KINDS = {"easy", "recovery", "long"}
RUN_KINDS = {"easy", "recovery", "long", "tempo", "intervals", "hills", "race"}


def cmd_check(args):
    result = check_sessions(read_json(args.file))
    print(json.dumps(result, indent=1))


def check_sessions(data):
    sessions = sorted(data.get("sessions", []), key=lambda s: s["date"])
    targets = {k: float(v) for k, v in data.get("weekTargetsKm", {}).items()}
    taper = set(data.get("taperWeeks", []))
    unavailable = set(data.get("unavailable", []))
    caps = {k: float(v) for k, v in data.get("maxMinutes", {}).items()}
    problems, notes = [], []
    by_day = {}
    for s in sessions:
        by_day.setdefault(s["date"], []).append(s)

    def kinds_on(date):
        return {s["kind"] for s in by_day.get(date.isoformat(), [])}

    for date_text, items in by_day.items():
        d = day(date_text)
        runs = [s for s in items if s["kind"] in RUN_KINDS]
        strength = [s for s in items if s["kind"] == "strength"]
        nxt, prev = d + dt.timedelta(days=1), d - dt.timedelta(days=1)
        if HARD & kinds_on(d) and HARD & kinds_on(nxt):
            problems.append(f"H1 {date_text}: hard sessions on consecutive days")
        if "intervals" in kinds_on(prev) and "long" in kinds_on(d):
            problems.append(f"H2 {date_text}: long run the day after intervals")
        if date_text in unavailable and not all(s["kind"] == "race" for s in items):
            problems.append(f"H3 {date_text}: session on an unavailable day")
        minutes = sum(float(s.get("min", 0)) for s in items if s["kind"] != "race")
        if date_text in caps and minutes > caps[date_text]:
            problems.append(f"H3 {date_text}: {minutes:.0f} min over the {caps[date_text]:.0f} min limit")
        if strength and KEY & kinds_on(nxt):
            problems.append(f"H5 {date_text}: strength the day before a key run")
        if len(runs) > 1 or len(strength) > 1:
            problems.append(f"H6 {date_text}: more than one run or strength session")

    weeks = {}
    for s in sessions:
        if s["kind"] in RUN_KINDS and s["kind"] != "race":
            weeks.setdefault(monday(day(s["date"])).isoformat(), []).append(s)
    summary = []
    for week, items in sorted(weeks.items()):
        total = sum(float(s.get("km", 0)) for s in items)
        easy = sum(float(s.get("km", 0)) * (1 if s["kind"] in EASY_KINDS else 0) + float(s.get("bookendKm", 0)) for s in items)
        long_km = max([float(s.get("km", 0)) for s in items if s["kind"] == "long"] or [0])
        target = targets.get(week)
        row = {"weekStart": week, "km": round(total, 1), "targetKm": target, "easyShare": round(easy / total, 2) if total else None, "longKm": long_km}
        summary.append(row)
        if target is not None and total > target * 1.10 + 1e-9:
            problems.append(f"H7 week {week}: {total:.1f} km is over 110% of the {target:.1f} km target")
        if week in taper and target is not None and total > target + 1e-9:
            problems.append(f"H4 week {week}: taper week above its target")
        if target is not None and abs(total - target) > 0.02 * target:
            notes.append(f"week {week}: sessions add to {total:.1f} km, target {target:.1f} km (more than 2% apart)")
        if total and easy / total < 0.80:
            notes.append(f"week {week}: easy share {easy / total:.0%} is under 80%")
        if long_km and long_km > 0.5 * total:
            notes.append(f"week {week}: long run is over half the week")
        cap = max(16.0, 0.25 * (target or total))
        for s in items:
            if s["kind"] == "easy" and (float(s.get("km", 0)) > cap or (long_km and float(s.get("km", 0)) > long_km)):
                notes.append(f"{s['date']}: easy run longer than the cap ({cap:.1f} km) or the long run")

    if sessions:
        first, last = day(sessions[0]["date"]), day(sessions[-1]["date"])
        gap, d = 0, first
        while d <= last:
            gap = 0 if RUN_KINDS & kinds_on(d) else gap + 1
            if gap == 2:
                notes.append(f"S1 {d.isoformat()}: second day in a row without a run")
            d += dt.timedelta(days=1)
    return {"ok": not problems, "hardRuleProblems": problems, "notes": notes, "weeks": summary}


# ---------------------------------------------------------------- scoring rearrangements (rules.md section 5)

DROP_MULT = {"strength": 1, "cross-training": 1, "easy": 2, "recovery": 2, "tempo": 4, "intervals": 4, "hills": 4, "long": 8}


def score_candidate(data, candidate):
    today = day(data["today"])
    original = {s["id"]: s for s in data["original"]}
    pinned = set(data.get("pinned", []) if isinstance(data.get("pinned"), list) else [data.get("pinned")])
    taper = set(data.get("taperWeeks", []))
    result = check_sessions({**data, "sessions": [s for s in candidate if s.get("status") != "dropped"]})
    problems, cost = list(result["hardRuleProblems"]), {}
    cand = {s["id"]: s for s in candidate}
    for sid, o in original.items():
        locked = day(o["date"]) < today or o.get("status") in ("completed", "missed")
        c = cand.get(sid)
        if locked and (c is None or c["date"] != o["date"] or float(c.get("km", 0)) != float(o.get("km", 0))):
            problems.append(f"H8 {sid}: a past, completed or missed session changed")
    for sid, c in cand.items():
        if sid not in original and day(c["date"]) < today:
            problems.append(f"H8 {sid}: a new session in the past")
        o = original.get(sid)
        if o and c["date"] != o["date"]:
            shift = abs((day(c["date"]) - day(o["date"])).days)
            if monday(day(c["date"])).isoformat() in taper and monday(day(o["date"])).isoformat() not in taper:
                problems.append(f"H4 {sid}: moved into the taper")
            if sid not in pinned:
                if shift > 3:
                    problems.append(f"{sid}: moved more than 3 days")
                cost["S3 moves"] = cost.get("S3 moves", 0) + 10
                cost["S4 days moved"] = cost.get("S4 days moved", 0) + 4 * shift
    live = [s for s in candidate if s.get("status") != "dropped"]
    runs = sorted({day(s["date"]) for s in live if s["kind"] in RUN_KINDS})
    future = [s for s in live if day(s["date"]) >= today]
    if future:
        end = max(day(s["date"]) for s in future)
        before = [d for d in runs if d < today]
        d = (before[-1] + dt.timedelta(days=1)) if before else today
        gap, units = 0, 0
        while d <= end:
            if d in runs:
                units += max(0, gap - 1)
                gap = 0
            else:
                gap += 1
            d += dt.timedelta(days=1)
        units += max(0, gap - 1)
        if units:
            cost["S1 gaps"] = 50 * units
    for week in result["weeks"]:
        if week["targetKm"]:
            short = 90 - 100 * week["km"] / week["targetKm"]
            if short > 0:
                cost["S2 volume short"] = cost.get("S2 volume short", 0) + round(5 * short, 1)
    pref = data.get("preferredLongRunDay")
    if pref is not None:
        for s in live:
            if s["kind"] == "long" and s["id"] not in pinned and day(s["date"]).weekday() != int(pref):
                cost["S5 long run off its day"] = cost.get("S5 long run off its day", 0) + 30
    legs = sorted(day(s["date"]) for s in live if s["kind"] == "strength" and s.get("legs", True))
    longs = {day(s["date"]) for s in live if s["kind"] == "long"}
    for a, b in zip(legs, legs[1:]):
        if (b - a).days < 2:
            cost["S6 leg strength"] = cost.get("S6 leg strength", 0) + 40
    for a in legs:
        if a - dt.timedelta(days=1) in longs:
            cost["S6 leg strength"] = cost.get("S6 leg strength", 0) + 40
    for sid, o in original.items():
        if o.get("status", "planned") != "planned" or day(o["date"]) < today:
            continue
        c = cand.get(sid)
        if c is None or c.get("status") == "dropped":
            if not o.get("userSkip"):
                cost["S7 dropped"] = cost.get("S7 dropped", 0) + 100 * DROP_MULT.get(o["kind"], 2)
        elif o["kind"] == "long" and float(c.get("km", 0)) < float(o.get("km", 0)):
            lost = 1 - float(c["km"]) / float(o["km"])
            if lost > 0.5:
                problems.append(f"{sid}: long run cut by more than half")
            cost["S7 long run shortened"] = cost.get("S7 long run shortened", 0) + round(100 * (4 + 4 * lost), 1)
    return {"valid": not problems, "problems": problems, "cost": round(sum(cost.values()), 1), "breakdown": cost, "weeks": result["weeks"], "notes": result["notes"]}


def cmd_score(args):
    data = read_json(args.file)
    if "original" not in data or "candidates" not in data or "today" not in data:
        die("score needs today, original and candidates")
    scored = {name: score_candidate(data, c) for name, c in data["candidates"].items()}
    valid = sorted((v["cost"], name) for name, v in scored.items() if v["valid"])
    print(json.dumps({"ok": True, "best": valid[0][1] if valid else None, "candidates": scored}, indent=1))


# ---------------------------------------------------------------- COROS course JSON

SECTION = {"warmup": 1, "work": 2, "steady": 2, "recovery": 3, "cooldown": 4}


def plain(step):
    kind = step.get("type", "work")
    if kind not in SECTION:
        die(f"step type '{kind}' should be one of {sorted(SECTION)}")
    section = {"sectionType": SECTION[kind]}
    if "km" in step or "m" in step:
        section.update(targetType=1, targetValue=int(round(float(step.get("m", float(step.get("km", 0)) * 1000)))))
    elif "min" in step or "s" in step:
        section.update(targetType=2, targetValue=int(round(float(step.get("s", float(step.get("min", 0)) * 60)))))
    else:
        die("every step needs km, m, min or s")
    if section["targetValue"] <= 0:
        die("step length must be positive")
    if step.get("pace"):
        a, b = (parse_pace(p) for p in str(step["pace"]).split("-"))
        section.update(intensityType=2, intensityValueStart=int(round(min(a, b))), intensityValueEnd=int(round(max(a, b))))
    elif step.get("hr"):
        a, b = (int(x) for x in str(step["hr"]).split("-"))
        section.update(intensityType=1, intensityValueStart=min(a, b), intensityValueEnd=max(a, b))
    return section


def cmd_coros(args):
    spec = read_json(args.file)
    name = str(spec.get("name", "")).strip()
    if not name or len(name) > 100:
        die("name is required, 100 characters at most")
    sections = []
    for step in spec.get("steps", []):
        if "repeat" in step:
            inner = [plain(s) for s in step["steps"]]
            if any("repeat" in s for s in step["steps"]):
                die("repeats cannot nest; write sets as consecutive repeat blocks")
            for s in inner:
                if s["sectionType"] not in (2, 3):
                    die("inside a repeat only work, steady or recovery steps are allowed")
            left = int(step["repeat"])
            while left > 0:  # COROS allows 1-20 repeats per group
                n = min(20, left)
                sections.append({"intervalGroup": True, "repeats": n, "sets": inner})
                left -= n
        else:
            sections.append(plain(step))
    if not sections:
        die("no steps")
    course = {"courseName": name, "courseDescription": str(spec.get("description", name)), "sportType": 5 if spec.get("trail") else 1, "sections": sections}
    if spec.get("trail") and any(s.get("targetType") == 2 for s in sections if not s.get("intervalGroup")):
        die("trail running workouts take distance (or climb) targets, not time")
    if "dayNo" in spec:
        course["dayNo"] = int(spec["dayNo"])
    print(json.dumps({"ok": True, "course": course}, indent=1))


# ---------------------------------------------------------------- main


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("paces"); s.add_argument("--threshold", required=True); s.add_argument("--lthr", type=int)
    s = sub.add_parser("race"); s.add_argument("--distance-km", type=float, required=True); s.add_argument("--time", required=True)
    s = sub.add_parser("predict"); s.add_argument("--threshold", required=True); s.add_argument("--distance-km", type=float, required=True)
    s = sub.add_parser("baseline"); s.add_argument("file", nargs="?"); s.add_argument("--today")
    s = sub.add_parser("load"); s.add_argument("file", nargs="?"); s.add_argument("--lthr", type=int); s.add_argument("--max-hr", type=int)
    s.add_argument("--rest-hr", type=int); s.add_argument("--threshold"); s.add_argument("--today")
    s = sub.add_parser("check"); s.add_argument("file", nargs="?")
    s = sub.add_parser("score"); s.add_argument("file", nargs="?")
    s = sub.add_parser("coros"); s.add_argument("file", nargs="?")
    args = p.parse_args()
    {"paces": cmd_paces, "race": cmd_race, "predict": cmd_predict, "baseline": cmd_baseline, "load": cmd_load, "check": cmd_check, "score": cmd_score, "coros": cmd_coros}[args.cmd](args)


if __name__ == "__main__":
    main()
