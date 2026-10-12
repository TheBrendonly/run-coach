# Coaching rules

The method, with its numbers. Read the section a task needs. `scripts/coach.py` does the sums; these rules decide what to do with them.

Contents: 1 Terms · 2 Targets and thresholds · 3 Building a plan · 4 Hard rules · 5 Rearranging a plan · 6 Missed sessions and missed time · 7 Check-ins and execution · 8 Adaptation · 9 Dial-back · 10 Requests and caps · 11 Proposals · 12 Wording

## 1. Terms

- **Week**: Monday to Sunday in the athlete's time zone. Dates are calendar days, never instants.
- **Session kinds**: easy, long, tempo, intervals, hills, recovery, strength, rest, race. Runs are everything except strength and rest.
- **Quality session**: tempo, intervals, hills. **Key run**: a quality session or the long run. **Hard session**: a key run or a race.
- **Session** is what is planned, **workout** is what goes to the watch, **activity** is what actually happened.
- **Missed**: a planned run with no matching activity by the end of its day. A **skip** is the athlete's choice before the day, not a miss.
- **Locked**: a session on a past day, or completed, or missed. Nothing ever moves or changes it.
- **Horizon**: today to the end of next week. Rearranging only touches sessions inside it.
- **Niggle**: an ache with body part, side, and severity 1 (aware of it), 2 (affects running), 3 (sharp, or changes how you run). Never "injury": the coach does not diagnose.
- **Excused run**: tagged heat, sick or poor sleep. Left out of pace trends.

## 2. Targets and thresholds

**Threshold pace** is roughly one-hour race pace. Source order: the watch's value (COROS fitness assessment) if plausible (2:34 to 8:20 per km); else a value the athlete accepted before; else a race or time trial of 10 minutes to 4 hours (`coach.py race`); else ask for one. A new or changed threshold that moves paces is a **proposal** (it retargets every remaining pace session); ignore changes under 1%.

**LTHR, max HR, resting HR**: ask the athlete (their watch app shows them) or use the watch's zones. Resting HR falls back to 55 bpm, flagged.

**Targets by kind** (`coach.py paces`):

| Kind | Target |
|---|---|
| Easy, long | heart rate 75-89% of LTHR (or the easy/long pace range if the athlete prefers pace) |
| Recovery | heart rate 70-84% of LTHR |
| Tempo | 94-98% of threshold speed |
| Intervals | 103-108% |
| Hills | 94-100%, or by effort on real hills |
| Race | no target |

Pace from a speed fraction f: `threshold seconds per km / f`, whole seconds. Variants in `sessions.md` have their own ranges.

**Durations from distance**: easy runs at 0.78 of threshold speed, long runs at 0.75, quality sessions at 0.88 averaged over the whole session. Without a threshold, easy runs at 6:25/km.

## 3. Building a plan

**Baseline** (`coach.py baseline`): the median weekly running distance and median longest run of the last 6 complete weeks, rounded to 100 m. Under 10 km a week is a layoff: start from 30 km a week and a 10 km long run.

**Goals**

- **Maintain** (the default when there is no goal): 4-week blocks. Loading weeks at 100%, 104% and 97% of baseline, then a down week at 70%. The long run holds near baseline.
- **Build** (toward a weekly distance and/or long run): each loading week up 8%, never more than 10% on the previous loading week, a down week at 70% every fourth week. A target below baseline holds at baseline.
- **Race**: count weeks back from race week. Taper first, then 2 peak weeks, then base and build share the rest. Loading weeks ramp from baseline toward the race peak, never below baseline, with a down week at 70% every fourth week before the taper. Race date must be after today and within 104 weeks.

| Race up to | Peak week | Longest run | Taper (multipliers of the last loading week) |
|---|---|---|---|
| 10 km | 35 km | 16 km | 0.55 (one week) |
| 21.1 km | 42 km | 21 km | 0.70, 0.50 |
| 42.2 km | 65 km | 32 km | 0.75, 0.60, 0.45 |
| Ultra | 70 km | 40 km | 0.75, 0.60, 0.45 |

Peaks never sit below baseline. If the 10% cap cannot reach the peak in the weeks available, plan the reachable peak and say so.

**Ultras and hilly races**: long runs carry climb in proportion: long-run climb = long-run distance x race climb / race distance. In build and peak weeks, offer a back-to-back: an easy run the day before the long run at 60% of its distance.

**Race week**: up to two easy runs before the race. No strength in the final 7 days.

**Placing a week**

1. Runs a week: what the athlete gave (default 5). Runs under 3 km are not planned.
2. Long run on the preferred day, else the roomiest weekend day (Sunday on a tie). At most half the week's distance.
3. Quality sessions: 1 in maintain, base, down and taper weeks; 2 in build and peak; never more than runs minus two. At least two calendar days apart, never next to another hard day, as far from hard days as possible. Kinds rotate intervals, tempo, hills; pick each one's variant from `sessions.md`.
4. Easy runs fill the longest gaps, avoiding the day after the long run on a tie.
5. At least 80% of the week's distance is easy (long runs, warm-ups, cool-downs and jogs count as easy).
6. No easy run longer than the week's long run or the larger of 16 km and 25% of the week's target. Volume that does not fit is left out rather than piled into one day; say when a target is above what the runs a week can reach.
7. A plan starting mid-week scales the first week to the open days left; its long run waits for the preferred day, or is skipped that week.
8. Strength by `strength.md` placement.
9. Week target = the planned distance, so a new plan meets H7 exactly.

**Check every plan and every change** with `coach.py check` before showing it.

## 4. Hard rules

A plan or proposal that breaks one is never shown.

| ID | Rule |
|---|---|
| H1 | No two hard sessions on consecutive days |
| H2 | No long run the day after intervals (an easy run the day before a long run is fine) |
| H3 | Nothing on a day the athlete cannot train, and each day's sessions together fit that day's time limit. The race is exempt |
| H4 | Taper weeks never gain load, and nothing moves into the taper from before it |
| H5 | No strength the day before a key run |
| H6 | At most one run and one strength session a day |
| H7 | A week never goes over its target by more than 10% (completed runs count at their actual distance) |
| H8 | Past days, completed and missed sessions never move or change, and nothing new lands in the past |

Read 48-hour rules as at least 2 calendar days apart. Rules hold across week boundaries.

## 5. Rearranging a plan

Triggers: a move, a skip, a swap, a day off, a missed session, a check-in finding, a request, a dial-back, a threshold change.

1. **Pin** what the athlete asked for (the session on its new day; the day off). A pinned session may go anywhere in the horizon.
2. Every other movable session (planned, today or later, not race or rest) may stay, move up to 3 days (earlier first on a tie), or be dropped. A long run on a day too short for it may be shortened to no less than half.
3. Keep every hard rule. Among valid arrangements pick the lowest cost:

| Cost | Points |
|---|---|
| S1 each extra day in a gap of 2+ days with no run (a 2-day gap is 1 unit) | 50 per unit |
| S2 each percentage point a week falls below 90% of its target | 5 |
| S3 each session moved (not the pinned one) | 10 |
| S4 each day a session moved | 4 |
| S5 long run off its preferred day | 30 |
| S6 leg strength sessions under 2 days apart, or leg strength the day after a long run | 40 each |
| S7 a dropped session: strength 100, easy 200, quality 400, long 800 | as listed |

Removing a 2-day gap always beats moving one session one day (50 against 14). On a tie, the earlier day for the earlier session.

4. **When not everything fits, drop in this order**: strength; easy runs, first spreading a dropped easy run's distance over the week's other easy runs and the long run (each grows by at most 20% or 3 km, in 100 m steps, never past H7, the taper or a day's limit); then weekly volume; then the quality session; the long run is shortened before it is ever dropped. Missed volume is never repaid beyond H7.
5. Edits (a dial-back, a volume change, a revert) are applied as asked; the rearranging then only repairs hard rules with the fewest moves. It never fills a gap a dial-back made on purpose.
6. If the pin itself breaks a rule nothing can fix, say which rule and offer the nearest valid day.
7. Report soft rules left unmet (S1, S2, S5, S6, S7) as trade-offs. Moves are the price of a fix, not a trade-off. The pinned session never counts for S3, S4 or S5 (moving the long run off its day because the athlete asked is not a trade-off).
8. Score candidate arrangements with `coach.py score`: it checks the hard rules (H8 and the taper included) and adds up S1 to S7 for each, so the choice is arithmetic, not judgment. Try the pin alone first, then the smallest fixes for each problem it reports.

Worked example: this week Mon rest, Tue easy 8 (done), Wed intervals 10 (done), Thu easy 8, Fri easy 8, Sat rest, Sun long 20; next week Mon rest, Tue easy 8, Wed tempo 10, Thu easy 8, Fri easy 8, Sat rest, Sun long 20. "Move Sunday's long run to Saturday" (today Thursday). The move alone leaves Sunday and next Monday without a run. The proposal also moves next Tuesday's easy run to next Monday. Two sessions moved, none dropped, 54 km to 54 km both weeks, reason "Avoids 2 days in a row without a run.", no trade-offs. Cost 14 against 18 for the next best and 50 for leaving the gap.

## 6. Missed sessions and missed time

**Matching** a run to a planned session: same date and sport, the closest duration within 50% (distance when there is no duration), one activity per session. A run on the day beside a missed session, on a day with no run planned, is offered as the match: ask the athlete to confirm or decline. A run that matches nothing is an extra run: ask which session it was, if any.

**Outcomes are facts**: completed and missed are written to the log straight away, without a proposal.

**One missed session**: rearrange the horizon. A missed **key** run is offered once as a make-up later in its own week (never next week). A missed easy run is let go.

**Missed time**, counted from the first missed run after the last run actually done:

| Days | Response | Volume |
|---|---|---|
| 3-6 | Resume | 90% for the rest of this week |
| 7-13 | Re-entry | 70% this week, 80% next week |
| 14-27 | Ramp | 60%, 73%, 87%, then full, week by week |
| 28+ | Rebuild | current fitness over fitness before the break (`coach.py load`), between 50% and 100%, for two weeks |

A stricter tier for the same break replaces the milder one; the same or a milder tier is not proposed again.

## 7. Check-ins and execution

One check-in per run, ever, for runs in the last 7 days. Ask in one message for all open runs:

1. Effort 1-10 (prefill from the watch's perceived exertion if it has one, and confirm).
2. Tags: legs heavy, poor sleep, sick, niggle, heat, stress, fuelling, felt great.
3. If it went badly: why (keep the athlete's words, at most 500 characters).
4. If a niggle: body part, side (left, right, both, none), severity 1-3. If the athlete describes it without a number, map their words (aware of it 1, affects running 2, sharp or changes how they run 3) and say in the proposal which you used.

Question template: "Quick check-in on [day] ([km] km) and [day] ([km] km). For each: effort out of 10, and anything from: legs heavy, poor sleep, sick, niggle, heat, stress, fuelling, felt great? If one went badly, why? Any niggle: where, which side, and is it 1 aware of it, 2 affecting your running, or 3 sharp?" Ask why for each missed session too.

**Execution score** for tempo, intervals and hills: line the laps up with the planned steps. When the lap count matches the steps (one extra trailing lap allowed), the laps in work positions are the work reps; otherwise use laps within 15% of a work step's distance or time. Take the **median** speed of the work reps. Slower than the slow end of the range: **below**. Faster than the fast end: **above**. Otherwise **on**. No usable laps: **unscored**. Easy and long runs are not pace-scored.

## 8. Adaptation

Run these at every check-in and on the first check-in of each week. **Safety rules always run.** When sick, or a niggle is severity 2+, skip the training rules. While any niggle is current or fatigue is flagged, hold every increase.

| Signal | Trigger | Response |
|---|---|---|
| One bad run | any | No change. Log it |
| Pace too slow | 3 scored, unexcused key runs in a row below target, counted since the last pace change | Ease paces 2% of threshold speed. At most once in 14 days |
| Pace too fast | 3 scored, unexcused key runs in a row above target at effort 8 or less | Quicken paces 2%. Same limit |
| Easy runs too hard | the last 3 easy runs within 14 days (since the last swap) at effort 7+, whatever the tags | Next quality session becomes an easy run |
| Sick | the latest answer within 3 days says sick | Dial-back: short easy only, 3 days, balanced return |
| Niggle 1 | latest report of that part and side within 7 days | Next hard session becomes easy |
| Niggle 2 | same | Dial-back: easy and long only, 7 days, slow return. Cross-training is fine if it does not hurt |
| Niggle 3 | same | No running for 7 days, and see a physio now. Never muted |
| Physio | same niggle at 2 check-ins, or 5 days after its first report | Notice only: suggest a physio, naming the part and side. Never muted |
| Fatigue | form below -30 for 3 days, or fitness up more than 7 in a week (`coach.py load`); not when history is under 42 days | Cut the week's volume 20%. Then rest this rule for 7 days |
| Great block | at least 3 scored key runs in the last 4 weeks, none below, all effort 8 or less, form never below -20 | Next block +5%, once a block |

Streaks count scored key runs only: missed, excused and unscored runs neither count nor break a streak. A scored run on or above target breaks a "too slow" streak.

**Stacking** (record every accepted action in the log's Decisions so these hold):

1. Two dial-backs at once merge into one: the strictest level, the longest days, the slowest return.
2. A dial-back is not proposed while an accepted one at least as strict still covers today.
3. A stricter dial-back during a milder one applies to the plan as it was before the milder one, so cuts never compound; keep the longer tail.
4. An accepted change is never proposed again from the same evidence.
5. Runs inside an accepted dial-back's window and return never grow.

## 9. Dial-back ("not feeling 100%")

| Level | Volume | Quality | Long run | Run cap | Strength | Pace |
|---|---|---|---|---|---|---|
| Toned down | 90% | kept | kept | none | kept | quality 5% easier |
| Easy and long runs only | 80% | becomes easy | kept | none | kept | unchanged |
| Short easy runs only | 60% | becomes easy | becomes easy | 6 km | dropped | unchanged |
| No running | 0 | none | none | 0 | dropped | none |

1 to 21 days from today. Then a return the athlete picks: **slowly** 14 days at 70%, **balanced** 7 days at 80%, **quickly** 3 days at 90%. The return never asks less than the window did (use the larger fraction). A run cut below 3 km is dropped. More than 21 days: refuse and ask for 21 or fewer.

Example: short easy only for 4 days, balanced: an 8 km easy run becomes 4.8 km, the long run becomes a 6 km easy run, strength is dropped; the return week runs at 80% (8 to 6.4, tempo 10 to 8, long 20 to 16).

## 10. Requests and caps

Anything the athlete asks for in their own words becomes one of these, one change per message:

| Request | Cap |
|---|---|
| Weekly volume up or down (this week and next) | between -50% and +10% of plan |
| Next long run longer or shorter | at most 20% of it or 5 km, whichever is smaller, in 100 m steps |
| Paces faster or slower | within 5% of threshold speed |
| Dial-back | 1-21 days, as above |
| Move, skip or swap a session; a day off | rearranging rules |
| Review now | run section 8 |

Increases skip taper weeks, are trimmed to the week's H7 room, and are held while a niggle is current, a dial-back covers today or fatigue is flagged. A capped request says so: "You asked to add 30% to weekly volume. The most it can grow is 10%."

A new goal or a new usual week is the athlete's own save: confirm it, then offer a new plan as a proposal.

## 11. Proposals

Every change, whoever raised it, is a proposal. Nothing changes until the athlete says **Accept**. **Keep as planned** closes it and mutes its main reason for 3 days (except a severity 3 niggle and a physio notice, which are never muted; a niggle mute covers only that part and side at no worse severity). At most one proposal is open; a new one replaces it and says so. The athlete's own requests replace an app finding; an app finding never replaces the athlete's open request and waits instead ("one finding is waiting until you decide").

Ranking when several findings arrive: a day off holding a session; health and missed time; a missed-run make-up; training changes; a threshold change; a missed strength session.

Layout:

```
Proposal: <headline>
Changes
- <one line per change, dated>
Why
- <reasons, main one first>
Trade-offs
- <or None.>
Impact: week of <date> <before> km to <after> km; week of <date> ...; N moved, N dropped, N added, N changed.
<health line, for any health proposal>
Accept or keep as planned?
```

One impact entry per affected week. "Changed" counts sessions whose distance, time or targets changed; a move alone counts as moved.

On Accept: write the new plan to the watch and the log, record the decision. On Keep: record it and the mute.

## 12. Wording

Short, plain, metric, Australian spelling, no em dashes, no emojis. Days like "Sun 11 Oct". Use these sentences:

| Situation | Sentence |
|---|---|
| Moved by the athlete | You moved the [kind] from [day] to [day]. |
| Moved by the coach | [Kind] moves from [day] to [day]. |
| Skipped | You're skipping the [kind] on [day]. |
| Day off | [Day] is off limits. / [Day] to [day] are off limits. |
| Missed | The [kind] on [day] didn't happen. |
| Gap | Avoids [N] days in a row without a run. |
| Redistributed | [N km] spread over the rest of the week of [day], so it holds its volume. |
| Long run day | Keeps the long run on your usual day. |
| Leg sessions | Keeps leg sessions two days apart. |
| Dropped | Drops the [kind] on [day]. It doesn't fit anywhere else. |
| Hard rule kept | H1 Keeps hard days apart. H2 Keeps the long run off the day after intervals. H3 Keeps sessions off days you can't train, and inside each day's time limit. H4 Protects the taper. H5 Keeps strength off the day before a key run. H6 Keeps it to one run and one strength session a day. H7 Keeps the week within 10% of plan. H8 Leaves the past alone. |
| Missed time | [N days] without a run. Then: Back at about 90% for the rest of the week. / A lighter week to get going again. / A two-week ramp back to full volume. / Rebuilding from where your fitness is now. |
| Pace ease | Your last 3 key sessions came in slower than target. Paces ease by 2%. |
| Pace progress | Your last 3 key sessions came in faster than target and felt fine. Paces pick up by 2%. |
| Easy too hard | Your last 3 easy runs felt hard. The next quality session becomes an easy run. |
| Sick | You're not well. Short, easy running for a few days. |
| Niggle 1 | Your [part] is niggling. The next hard session becomes an easy run. |
| Niggle 2 | Your [part] is affecting your running. Easy and long runs only for a week. Cross-training is fine if it doesn't hurt. |
| Niggle 3 | Your [part] hurts. No running for now. See a physio about your [part] before you run again. |
| Physio later | Your [part] has hung around. Worth seeing a physio. |
| Form low | Fatigue is well ahead of fitness (form [n]). Easing off for a bit. |
| Ramp high | Fitness is climbing fast ([n] a week). Easing off so it sticks. |
| Block | Strong block. A little more (5%) next block. |
| Dial-back | [Toned down / Easy and long runs only / Short easy runs only / No running] for N days, [then a gentle return over two weeks / then a week to build back / then straight back to it]. |
| Capped | You asked to [add N% to weekly volume]. The most it can [grow] is [N]. |
| Threshold | Threshold pace set at [pace] from your race or time trial. / Your threshold pace on your watch is [pace]. |
| Health line | This isn't medical advice. If pain is sharp, getting worse or changes how you run, see a physio or GP. |

The part reads "left calf", "right calf", or "calf on both sides".
