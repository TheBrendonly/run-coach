# Pushing to COROS

Confirmed against the live COROS connector (October 2026). The connector's own tool descriptions carry the full field rules; this file carries what shapes the coaching.

## Runs go in one training plan

- Name it `Run Coach: <goal>`. Its days can be replaced or cleared later. A one-off scheduled workout can only be moved or removed by the athlete in the COROS app, so use one-offs only for strength.
- **Limits**: 4 to 16 weeks, starting between today and 14 days ahead, natural Monday-Sunday weeks (a mid-week start makes a partial first week), and the final week must hold a workout. Days with no course are rest days.
- **Day numbers** count from the plan's start date (day 0) across the whole plan.
- **Phases**: base 2, build 3, peak 4, taper and race week 5, post-race 6 (preparation 1). Maintain and down weeks take base. The first phase starts on the start date, later ones on a Monday, every phase ends on a Sunday, and the weeks add up to the plan length.
- **Longer plans**: push up to 16 weeks; when one call would be too large, create the first 8 weeks and extend in the same session. For builds over 16 weeks, keep the outline in the log and start the next plan as the first ends.
- **Before writing**: query the plan library. Only plans this connector created are editable; a plan pushed by another app (for example another coaching app) cannot be changed and will sit beside this one, so tell the athlete to stop that app's sync to avoid doubled days.

## A workout

One session is one course: warm-up, main set and cool-down as sections of one workout. Build it with `coach.py coros`:

```json
{"name": "Cruise intervals: 3 x 1 km",
 "description": "Week 1 of 12, Base. 2 km easy, then 3 x 1 km at 4:54-5:06/km with 60 s easy jog, then 1 km easy. Smooth and controlled.",
 "steps": [
  {"type": "warmup", "km": 2},
  {"repeat": 3, "steps": [{"type": "work", "km": 1, "pace": "4:54-5:06"}, {"type": "recovery", "s": 60}]},
  {"type": "cooldown", "km": 1}]}
```

Output (what the connector takes):

```json
{"courseName": "Cruise intervals: 3 x 1 km", "courseDescription": "...", "sportType": 1,
 "sections": [
  {"sectionType": 1, "targetType": 1, "targetValue": 2000},
  {"intervalGroup": true, "repeats": 3, "sets": [
    {"sectionType": 2, "targetType": 1, "targetValue": 1000, "intensityType": 2, "intensityValueStart": 294, "intensityValueEnd": 306},
    {"sectionType": 3, "targetType": 2, "targetValue": 60}]},
  {"sectionType": 4, "targetType": 1, "targetValue": 1000}]}
```

- Sections: 1 warm-up, 2 work or steady, 3 recovery, 4 cool-down. Targets: 1 distance in metres, 2 time in seconds. Intensity: 1 heart rate in bpm, 2 pace in seconds per km, as an ascending range. No intensity fields means an open step.
- Repeats: 1-20 per group (the script splits more), no nesting, only work and recovery inside. Sections may mix heart rate and pace.
- Trail running (sport 5) takes distance or climb targets, not time.
- Names and descriptions show on the watch exactly as written: plain coaching words, never field names or code numbers.
- **Open steps need consent**: the connector leaves a step without a target only when the athlete asked. At setup, ask once: "Warm-ups, recoveries and cool-downs go to the watch with no target, so it doesn't alert you while you jog. OK?" Record the answer in the log.

## Changing the plan

- **Read the day first** (plan details), then send the whole day. An update replaces a whole day.
- **Move**: one update holding a rest entry for the old day (`{dayNo, courseName: "Rest", courseDescription: "Recovery day", sportType: 4, sections: []}`) and the session on the new day.
- Completed days are locked; the update skips them and says so.
- Change the plan length through `totalWeeks` (with the full phase table). Ending or deleting a plan is done by the athlete in the COROS app.

## Read back, every time

After every write, read the plan details for the changed dates and compare. Only then say a run is on the watch, and remind the athlete to sync the watch. If a read-back differs or a write failed, say so plainly and keep the log's watch status as "not on watch".

## Strength

The connector cannot create or edit strength workouts. It can schedule a workout already in the athlete's COROS workout library onto a date (today to 90 days ahead), and that copy cannot be moved afterwards. So: the athlete builds the sessions once from the build sheet (`strength.md`), and the coach schedules only the next 7 days, once per session. If a scheduled session later moves, tell the athlete to delete the old one in the COROS app.

## Other watches

No push. Give each day's session in words (title and steps) when asked "what's on today".
