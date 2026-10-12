# run-coach

A Claude skill that coaches your running and strength like an adaptive training app, using the Strava and COROS connectors.

- **Strava** supplies your history: every run, lap by lap, with heart rate and effort.
- **COROS** gets the plan: structured workouts (warm-up, repeats, recoveries, cool-down, pace or heart-rate targets) land on your watch calendar.
- **A training log** (one document you own) holds your goal, targets, check-ins, niggles, strength and every decision.

Tell it a goal. It reads your history, researches the race, builds a periodised plan with varied sessions (400 m reps, cruise intervals, pyramids, over/unders, hills, strides, progressive and race-pace long runs) and pushes it to your watch. Say "check in" whenever you like: it scores your runs against the plan, asks how they felt and proposes changes. **Nothing changes until you accept.**

## What's inside

```
skills/run-coach/
  SKILL.md                  the coach's workflow
  references/rules.md       plan building, 8 hard rules, rearranging, missed runs, adaptation, dial-back, caps, proposals, wording
  references/sessions.md    the session library and race-day notes
  references/strength.md    the 5-movement method, loads, light-kit tricks, placement
  references/coros.md       pushing to the watch, with the verified workout format
  references/log-template.md the training log
  scripts/coach.py          the arithmetic: paces, baseline, fitness and fatigue, hard-rule checks, rearrangement scoring, COROS workout JSON (Python 3, no dependencies)
```

## You need

- Claude with skills (Claude apps or Claude Code).
- The Strava connector (a Strava subscription is needed for it).
- The COROS connector for watch push. Without it the skill still plans and adapts, and gives each day's session in words.
- Somewhere for the log: a notes app Claude can reach (Notion, Google Docs), or a folder. With neither, the skill prints the log for you to keep.

## Install

- **Claude apps:** add the `run-coach.plugin` file, or this folder, as a plugin.
- **Claude Code:** copy `skills/run-coach` to `~/.claude/skills/run-coach/`.

## Use

| Say | What happens |
|---|---|
| "Set up run coach" | Reads your history, asks a few questions, creates the log |
| "I'm running a half marathon on 21 March, build me a plan" | Researches the race, proposes a plan, pushes it on your accept |
| "Check in" | Scores recent runs, asks how they felt, proposes changes if needed |
| "Move Sunday's long run to Saturday" / "I'm away next week" / "Not feeling 100%" | Rearranges around it, as a proposal |
| "My left calf is tight" | Conservative niggle rules |
| "Give me a 20 minute hotel strength session" | A custom session, logged |
| "What's on today?" | Today's session |

## Limits

- COROS plans run 4 to 16 weeks and must start within 14 days; longer builds are chained.
- The COROS connector cannot create strength workouts or delete anything. You build strength sessions once in the COROS app from a sheet the skill gives you, and delete old items yourself.
- A plan another app pushed to COROS can't be edited by the skill; stop that app's sync to avoid doubled days.

Connector behaviour verified October 2026.

## Not medical advice

Training guidance from an AI model. It does not diagnose or treat anything. For pain, illness or injury, see a physio or doctor.

Not affiliated with Strava or COROS. Licence: MIT.
