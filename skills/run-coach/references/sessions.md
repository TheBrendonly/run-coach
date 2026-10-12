# Session library

How each session is built. The kind (tempo, intervals, hills, long, easy) is what the rules see; the **variant** is how it is run. A variant never changes a session's planned distance or time, so weekly volume and the hard rules are unaffected.

## Building a quality session

- Warm-up 15 min easy, cool-down 10 min easy. A short session shrinks them together, never below 10 and 5 min, keeping at least 8 min of main set. Shorter still: one steady run at the slow end of the range.
- Main set = planned time minus warm-up and cool-down. Fit whole repeats into it; leftover time goes to the cool-down.
- Warm-up, recovery jogs and cool-down carry no target (open), so the watch stays quiet. Work steps carry pace.
- Work steps for distance reps are distance-based; everything else is time-based.

## Variants

| Kind | Variant | Main set | Work pace (fraction of threshold speed) | Recovery |
|---|---|---|---|---|
| Tempo | continuous (default) | one block | 94-98% | none |
| Tempo | cruise intervals | 2-6 x 1-3 km | 98-102% | 60 s per km of rep, max 120 s |
| Tempo | over/unders | 2-4 sets of (over 400-1000 m, under 400-1000 m) x 2-3, as consecutive blocks | over 103-106%, under 94-97% | 2 min jog between sets |
| Intervals | timed (default) | 4 min on | 103-108% | 2 min jog |
| Intervals | 1600 m reps | 3-6 reps | 103-108% | 3 min |
| Intervals | 1 km reps | 4-8 reps | 103-108% | 2 min |
| Intervals | 800 m reps | 5-10 reps | 103-108% | 90-120 s |
| Intervals | 400 m reps | 8-16 reps | 109-116% | 60-90 s |
| Intervals | 200 m reps | 10-20 reps | 109-116% | 60 s |
| Intervals | pyramid | 400-800-1200-800-400 m (scale down to fit) | 103-108% | equal time to the rep |
| Hills | 90 s (default) | 90 s up | effort 8-9/10 (or 94-100% on a road) | jog down, about 2 min |
| Hills | short hills | 60 s up | effort 8-9/10 | jog down |
| Hills | long hills | 3 min up | effort 7-8/10 | jog down, about 3 min |
| Long | steady (default) | continuous | heart rate (or long pace) | none |
| Long | progressive | final quarter to third at 86-92% | heart rate, then pace | none |
| Long | race-pace | 2-3 blocks of 3-8 km at goal race pace (half and marathon goals only) | goal pace (`coach.py predict`) | easy between blocks |
| Easy | with strides | easy run, then 4-8 x 20 s fast and relaxed | open (by feel) | 40-60 s easy |

Long-run variants are not pace-scored (section 7 of `rules.md`).

## Choosing a variant

Use the calendar week number to rotate so the same session rarely repeats two weeks running.

| Phase | Tempo | Intervals | Hills |
|---|---|---|---|
| Base | continuous, cruise | timed, 1 km, 800 m | 90 s, short |
| Build | cruise, over/unders, continuous | 1 km, 400 m, 1600 m, pyramid, 800 m | 90 s, long, short |
| Peak | cruise, continuous, over/unders | 1600 m, 1 km, 800 m | 90 s, short, long (ultras: long) |
| Taper | cruise (short) | 400 m, 200 m | short |
| Down week | default shapes only | | |
| Maintain | continuous, cruise, over/unders | timed, 1 km, 400 m, 800 m | 90 s, short, long |

- Long-run variants: at most every third week in build (progressive, alternating with race-pace for half and marathon goals), peak and taper (race-pace for half and marathon); every fifth week in maintain. Never in base or down weeks, or within 2 weeks of the race.
- Strides: on one easy run a week. 4 in base, taper and maintain; 6 in build and peak; none in down weeks.
- When a variant does not fit the main-set time (common in short weeks), use the default shape.
- A session turned easy (dial-back, niggle) loses its variant. A pace change rescales the variant's own range.

## Naming

Name by content, plainly: "Intervals: 10 x 400 m", "Cruise intervals: 3 x 2 km", "Over/unders: 3 sets", "Progressive long run: 24 km", "Easy run with strides: 8 km". Descriptions say what to do and why, paces in words, and the place in the plan ("Week 5 of 12, Build").

## Race-day notes (from 7 days out)

- Predicted finish and a goal pace window of about ±1.5% from threshold (`coach.py predict`); not for ultras or races over about 4 hours.
- First half at the slow side of the window, then even or slightly faster.
- Notable climbing, or an ultra: pace by effort, and name the climbs from the course notes.
- Over 90 minutes: one general fuelling line: about 60 g of carbohydrate an hour is a common guideline; practise it in long runs first.
- These are notes. They change nothing in the plan.
