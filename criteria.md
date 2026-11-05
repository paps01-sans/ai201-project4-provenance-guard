# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. _"The
detector is accurate"_ is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. _"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"_ is a criterion.

Under each, write a sentence or two on **why that target**. _"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"_ is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area            | A question it could answer                                    |
| --------------- | ------------------------------------------------------------- |
| False positives | How often may a human's writing get called AI?                |
| Score spread    | How far apart should clearly-AI and clearly-human text score? |
| Label coverage  | Is every one of your three labels actually reachable?         |
| The appeal path | Does an appeal always change status and always get recorded?  |
| Bad input       | What happens when `text` is missing, empty, or enormous?      |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## 1.

<!-- Your criterion. It must name a number. -->

Across each of three evaluation runs, no more than 1 of 10 pieces of my own
writing may receive the `high-confidence AI` label.

**Why this target:**

False accusations are more harmful than letting some AI writing pass. Allowing
one false positive gives the detector a small margin for uncertainty while
keeping the target meaningful for a real writing site.

---

## 2.

<!-- Your criterion. -->

In each of three runs, the average combined score for 5 clearly AI-written
texts must be at least `0.65`, and the average combined score for 5 clearly
human-written texts must be at most `0.35`.

**Why this target:**

The two averages need a gap of at least `0.30` so the scores provide useful
separation before labels are applied. Using averages allows individual texts
to be unusual without making the whole signal fail.

---

## 3.

<!-- Your criterion. -->

The three labels `human`, `unsure`, and `ai` must each be produced by at least
one submitted text in the label-coverage scenario during every evaluation
run.

**Why this target:**

Every label is part of the public contract. Requiring all three in all three
runs proves that the thresholds are reachable and that the unsure option is
not just documentation that the service never returns.

---

## 4.

<!-- Your criterion. -->

For 5 valid submissions followed by 5 valid appeals, every appeal must return
an observable success response, include the original `content_id`, and create
an audit entry with `status: "under_review"` and the submitted reasoning.

**Why this target:**

An appeal is the main protection against a wrong accusation. Requiring all 5
appeals to be recorded makes sure the path works repeatedly and does not only
appear to work for one example.

---

## 5.

<!-- Your criterion. -->

For four malformed submissions, covering missing `text`, `null` text, empty
text, and an oversized text body, the service must return a JSON error with a
4xx status every time, never return a 5xx response, and never write a normal
`decided` audit entry.

**Why this target:**

Malformed input is normal for a public endpoint, and a bad request should not
crash the service or look like a real detection decision. Four cases cover the
main input failures without hiding which behavior needs fixing.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
