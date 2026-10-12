# Training log template

One document titled **Run Coach Training Log**. It is the coach's memory between conversations: everything Strava and the watch do not hold. Fill every field; write "unknown" where the athlete does not know.

Where it lives (chosen at setup): a page in a connected notes app (Notion, Google Docs) found by its exact title; or a `training-log.md` file in a persistent folder (Claude Code, a connected folder); or, with neither, printed at the end of each conversation for the athlete to save and paste back next time.

Upkeep: keep 8 weeks of check-in rows and fold older ones into one line a month. Keep Decisions for 120 days (the stacking rules read them). Edit only the sections that changed, so the athlete's own notes survive. Check-ins hold health information: keep them in the athlete's own document only.

```markdown
# Run Coach Training Log

## Athlete
- Units: km | Time zone: | Log home:
- Watch: COROS | other (no push) | Open steps on the watch confirmed: yes | no
- Runs a week: | Long-run day: | Preferred hard days:
- Usual week (per day: open or not, time limit): Mon | Tue | Wed | Thu | Fri | Sat | Sun
- Days off coming up:
- Easy runs by: heart rate | pace
- Usual terrain:
- Injury history:
- Body weight (for strength):

## Fitness
- Threshold pace: /km (source, date)
- LTHR: bpm | Max HR: bpm | Resting HR: bpm (source, date)
- Baseline: km a week, long run km (median of the last 6 full weeks, date)
- Latest fitness / fatigue / form: (date, from coach.py load)
- Recent race or time trial:

## Targets (from threshold, date)
| Zone | Pace /km | Heart rate |

## Pace changes
| Date | Change | Reason |

## Goal
- Type: maintain | build | race
- Race: name, date, distance, climb, surface, target
- Course notes: (with sources)

## Plan
- COROS plan: name, start, end | Last read back: (date)
| Week | Starts | Phase | Target km | Long run km | Key sessions | Actual km |

## Open proposal
(the full proposal text while one is waiting for Accept or Keep as planned, else "None")

## Check-ins
| Run date | Activity id | Session | Score | Effort | Tags | Why | Niggle |

## Niggles
| First reported | Part and side | Severity | Reports | Status |

## Strength
- Mode: 5-movement | builder | Sessions a week:
- Kit:
- COROS strength workouts: (exact names)
- This cycle: started (Monday), squat / hinge / push / pull / core exercises, wave week
| Date | Exercise | Load | Sets x reps | RIR | Next time |

## Decisions
| Date | Type | Detail | Outcome | Mute until |
```

Decision types to record (the stacking rules depend on them): pace change, quality swap, fatigue cut, block progression, niggle action (part, side, severity), dial-back (level, days, return speed, window end, return end), missed-time return (tier), make-up offered, request (with what was capped), threshold change, kept (with the reason muted).
