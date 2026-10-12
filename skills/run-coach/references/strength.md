# Strength

## Kit

Record the athlete's kit in the log: dumbbells by weight and count, barbell, machines, a pull-up bar, a bench, a step or box (unlocks deficits), or bodyweight only. **Single-weight kit** means exactly one dumbbell weight and nothing heavier. Body weight is needed for bodyweight lifts; ask for it.

## The 5-movement method (default)

- Every session trains **squat, hinge, push, pull, core**: one exercise each, 3 sets (2 in a down week). Both weekly sessions are full body.
- **Rep wave**: 12, 10, 8, 6 reps, one step per calendar week, counted from the Monday of the week of the first logged session. Both sessions of a week share the reps. After week 4 the cycle restarts at 12.
- **Rotation**: each new 4-week cycle moves every slot to the next exercise that suits the kit, main lifts first. A permanent swap the athlete asked for wins.
- Bodyweight lifts ignore the wave: use the rep target the athlete can do with 2 in reserve.
- Nothing rotates until the athlete has logged once.

Allowed exercises (stay inside this list unless the athlete asks):

| Slot | Exercises |
|---|---|
| Squat | goblet squat, bodyweight squat, back squat, leg press, dumbbell split squat, Bulgarian split squat, reverse lunge, step-up, walking lunge |
| Hinge | dumbbell Romanian deadlift, single-leg Romanian deadlift, Romanian deadlift, deadlift, single-leg glute bridge, dumbbell glute bridge, hip thrust |
| Push | push-up, dumbbell floor press, dumbbell bench press, bench press, dumbbell shoulder press, overhead press |
| Pull | one-arm dumbbell row, bent-over dumbbell row, seated cable row, inverted row, pull-up (band-assisted when needed), lat pulldown |
| Core | dead bug, Pallof press, side plank, farmer's carry (30-40 m) |
| Extras (builder mode) | calf raises (standing, single-leg, bent-knee), side-lying hip raise |

Write your own one-line cue for each; never copy instruction text or images from elsewhere.

**Builder mode** (if the athlete prefers): at most 5 exercises, patterns by focus (lower: squat, hinge, lunge, calf, core; upper: horizontal push, horizontal pull, vertical push, vertical pull, core; full: squat, hinge, horizontal push, horizontal pull, lunge, core), keep the same exercise per pattern until the athlete says "change it up", double progression (below).

## Loads

Aim to finish each working set with **2 reps in reserve (RIR 2)**.

**Estimate (e1RM)** from a logged set of 12 reps or fewer at RIR 3 or less: reps to failure n = reps + RIR (+0.5 when RIR is above 0), then e1RM = load / f(n):

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| f(n) % | 100 | 95.5 | 92.2 | 89.2 | 86.3 | 83.7 | 81.1 | 78.6 | 76.2 | 73.9 | 70.7 | 68.0 |

Beyond 12: f(n) = f(12) x (1 + 12/30) / (1 + n/30). Blend each new estimate into the old one at 30% (new = old + 0.3 x (set estimate - old)). Warm-ups and sets above 12 reps never change e1RM.

**Load for a target**: e1RM x f(reps + 2), snapped down to what the kit can make. First time on an exercise with no history: aim one rep easier (RIR 3) and calibrate from the log.

**Double progression** (builder mode): when every working set reaches the top of the rep range without a grind, go up one kit step and back to the bottom of the range (only if the step is within +5% or the estimate supports it); otherwise add a rep. If the estimate says the bottom of the range is out of reach, come down at most 10%.

**Stalls**: a session's best estimate more than 5% below the average of the previous 4 is a stall. Two in a row: a lighter session at 90% of the last load; the session after resets the count.

## Single-weight kit

With one fixed weight, make the lift fit 6 to 20 reps at RIR 2 (preferably 6-12 lower body, 6-15 upper) by choosing, fewest changes first:

1. one or two dumbbells, or the single-leg/single-arm version;
2. then levers in this order, each lowering what you can lift: 3 s lowering (x0.95), 5 s lowering (x0.90), 2 s pause (x0.92), one-and-a-half reps (x0.85), a deficit on a step (x0.93, only with a step).

Levers multiply. Keep a rep under 8 seconds: base 3 s, +2 s for a 3 s lowering or +4 s for a 5 s lowering, +2 s for a pause, then x1.5 for one-and-a-half reps (so 5 s lowering with a pause, or with 1.5 reps, is out).

Warnings, in these words:
- Leg lift still over 15 reps: "[Exercise] is still over 15 reps. A heavier weight would help your running more."
- Any other lift over 20 reps: "[Exercise] is still over 20 reps, so it is too easy to build much. A heavier weight would make it count."

**What to buy**: after 2 logged sessions, the heaviest common pair (5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30 kg; check local availability) that still gives every lift in the rotation at least 6 reps at RIR 2 if the athlete is 10% weaker than estimated, plus a heavier "also fine" pair for about 12 weeks of progress. Before 2 sessions, a range from 75% to 100% of the estimates.

## Placement in the running week

- 2 sessions in a normal week, 1 in down and taper weeks, none in the final 7 days before a race.
- Leg (or full-body) work on a hard-run day after the run, or an easy day; at least 2 days between leg sessions; avoid leg work the day after a long run.
- Never the day before a key run (H5). One strength session a day at most (H6). Session plus that day's run must fit the day's time limit (plan 40 min).
- A missed session is offered again later in its own week if a day fits; never a make-up of a make-up; let it go when the week has ended. Keep as planned declines it for good.

## On the watch

The COROS connector cannot create strength workouts. Give the athlete a **build sheet** to key into the COROS app once (workout name, each exercise with sets and reps), record the exact names in the log, then schedule them for the next 7 days only (`coros.md`). The watch keeps the reps it was built with, so say the week's wave reps at each check-in.

## Custom sessions in chat

On request (travel, a short window, different kit) write a session card: exercise, sets x reps, load, tempo, rest (120 s main lifts, 75 s accessories). It lives in chat and the log, not the watch.

## Logging

Per set: exercise, set number, type (warm-up, normal, failure), load, reps, RIR. Read recorded sets from the watch or Strava when present, otherwise ask. A finished session completes the planned one (a fact, no proposal). After each session say the next-time change in one line: "Top of the range on every set. Up to [n] kg next time." / "Same weight, aim for [n] reps next time." / "Down from [a] kg to [b] kg next time, to stay at the target effort." / "Two sessions in a row below par. A lighter session to reset." / "Next time: [n] reps (at [n] kg)."

Personal records worth naming: heaviest load, most reps at a load done before, best estimate.
