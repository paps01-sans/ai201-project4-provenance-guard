# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. A writing site sends the writer's `text` and `creator_id` to `POST /submit`.
2. The submit handler validates the request and creates a unique `content_id`.
3. `detector.py` runs the local language model and adds `model_score`, based on
   how predictable the text is to that model.
4. `stylometry.py` measures the text's shape and adds `style_score`, using
   sentence-length variation, vocabulary repetition, and punctuation density.
5. `scoring.py::combine_signals` combines both 0 to 1 signals into one score,
   where a higher score means more likely AI writing.
6. `scoring.py::score_to_label` turns the combined score into a machine-readable
   guess and a plain-English label for the reader.
7. `audit.py` records the decision, both signal scores, the combined score, and
   the content id. The API returns that same result to the writing site.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a local language model.
The model signal uses perplexity and converts it to a 0 to 1 score, where a
higher score means the text looks more AI-like.

**Why that might differ between human and AI writing:** A language model tends
to find generated text easy to predict because it was produced by choosing
likely next words. Human writing often has more unusual word choices and
unexpected turns, which can make it less predictable.

**What it can't see:** It cannot see who actually wrote the text. Plain,
ordinary human writing, second-language writing, or writing by someone using a
limited vocabulary can also be predictable and get a high AI score. It can
also mistake rare or formal vocabulary for human authorship.

### Signal two — the style signal

**What it measures:** The visible shape of the text rather than its meaning.
It measures sentence-length spread, type-token ratio, and punctuation density,
then combines those measures into a 0 to 1 score where higher means more
AI-like.

**Why that might differ between human and AI writing:** Generated writing often
has steady sentence lengths, repeated common vocabulary, and predictable
punctuation. Human writing is more likely to vary in sentence length,
vocabulary, and punctuation.

**What it can't see:** It cannot understand the topic, meaning, or authorship.
Small edits, inserted typos, a quotation, or manually split sentences can
change the measurements without changing who wrote the text. A careful human
writer can also naturally have the same surface pattern as generated prose.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** The style signal converts each measure to an AI-likeness value
between 0 and 1. Low sentence-length variation, low vocabulary variation, and
low punctuation density increase the AI-likeness value. The combined score is
an equal-weight average of the model signal and style signal. When the two
signals disagree, the average pulls the result toward the unsure band instead
of allowing either signal to make a confident decision by itself.

**The numbers:** `combined_score = (0.50 * model_score) + (0.50 * style_score)`.
The model weight is `0.50` and the style weight is `0.50`, configured in
`config.py`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

For example, if the model signal is `0.78` and the style signal is `0.30`, the
combined score is `0.54`. The signals split, but the average keeps the result
in the unsure band instead of making a high-confidence AI claim.

My four calibration inputs produced these results:

| Input             | Model score | Style score | Combined score |
| ----------------- | ----------: | ----------: | -------------: |
| clearly AI        |      0.6858 |      0.5387 |         0.6122 |
| clearly human     |      0.6791 |      0.3798 |         0.5294 |
| formal human      |      0.5878 |      0.4032 |         0.4955 |
| lightly edited AI |      0.6812 |      0.3817 |         0.5314 |

The clearly human input is a split case: the model score is high at `0.6791`,
but the style score is lower at `0.3798`. The combined score of `0.5294`
keeps it below the high-confidence AI threshold. The small gap between the
clearly human and clearly AI combined scores is also a finding: these short
examples are difficult for the model signal to separate.

### False-positive trace

A real writer submits plain, conventional prose. The model finds it very
predictable and returns `model_score = 0.78`. The style signal is less certain
and returns `style_score = 0.50`. With the initial equal-weight plan, the
combined score is `0.64`, which is in the current unsure band between `0.35`
and `0.65`. The reader sees: "We are not sure whether this was written by a
person or by AI." The response includes the `content_id`, so the writer can
call `POST /appeal` with that id and a reason. The appeal is recorded in the
append-only audit log and changes the item's status to `under_review`.

The system cannot prove the writer's authorship from these signals, so the
thresholds should leave room for an unsure result rather than treating one
predictable signal as proof.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label                 | Score range              | The exact text a reader sees                                   |
| --------------------- | ------------------------ | -------------------------------------------------------------- |
| high-confidence human | 0.00 to 0.35             | We think this was probably written by a person.                |
| unsure                | above 0.35 to below 0.65 | We are not sure whether this was written by a person or by AI. |
| high-confidence AI    | 0.65 to 1.00             | We think this was probably written by AI.                      |

**Why I worded the "unsure" one this way:**

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It says what the system does not know without accusing the writer. It also
gives the writer a clear reason to use the appeal path.

I reached all three labels with these submissions:

| Guess    | Combined score | Reader-facing label                                            |
| -------- | -------------: | -------------------------------------------------------------- |
| `ai`     |         0.8899 | We think this was probably written by AI.                      |
| `unsure` |         0.5558 | We are not sure whether this was written by a person or by AI. |
| `human`  |         0.0874 | We think this was probably written by a person.                |

## Endpoint Contracts

### `POST /submit`

**Request JSON:**

| Field        | Type   | Required | Meaning                             |
| ------------ | ------ | -------- | ----------------------------------- |
| `text`       | string | yes      | The writing to evaluate             |
| `creator_id` | string | yes      | The writer or account submitting it |

**Response JSON:**

| Field            | Type   | Meaning                                             |
| ---------------- | ------ | --------------------------------------------------- |
| `content_id`     | string | Unique id for this submission and future appeals    |
| `guess`          | string | Machine-readable result: `human`, `unsure`, or `ai` |
| `confidence`     | number | Confidence value from 0.0 to 1.0                    |
| `label`          | string | Plain-English text shown to the reader              |
| `model_score`    | number | Detector signal from 0.0 to 1.0                     |
| `style_score`    | number | Stylometry signal from 0.0 to 1.0                   |
| `combined_score` | number | Score used to choose the label                      |

### `POST /appeal`

**Request JSON:**

| Field        | Type   | Required | Meaning                             |
| ------------ | ------ | -------- | ----------------------------------- |
| `content_id` | string | yes      | Submission being challenged         |
| `reasoning`  | string | yes      | The writer's explanation or context |

**Response JSON:**

| Field        | Type   | Meaning                                     |
| ------------ | ------ | ------------------------------------------- |
| `content_id` | string | The appealed submission id                  |
| `status`     | string | `under_review` after the appeal is recorded |
| `message`    | string | Confirmation that the appeal was received   |

The endpoint shapes give another developer the field names, types, required
inputs, and returned result without needing to ask how the service works.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
           -d '{"text": "I walked home after class and noticed the same blue mug on the library steps. I do not know who left it there, but it made the whole afternoon feel strangely personal.", "creator_id": "milestone5-unsure"}'
```

```json
{
  "combined_score": 0.5558,
  "confidence": 0.5558,
  "content_id": "6fb45c95-4274-42a0-a6f2-7a74a7b4250b",
  "guess": "unsure",
  "label": "We are not sure whether this was written by a person or by AI.",
  "model_score": 0.5435,
  "style_score": 0.5682
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
     -d '{"content_id": "6fb45c95-4274-42a0-a6f2-7a74a7b4250b", "reasoning": "I wrote this piece myself and would like a human review of the uncertain result."}'
```

```json
{
  "content_id": "6fb45c95-4274-42a0-a6f2-7a74a7b4250b",
  "message": "Your appeal was received and is now under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.5558,
      "content_id": "6fb45c95-4274-42a0-a6f2-7a74a7b4250b",
      "creator_id": "milestone5-unsure",
      "guess": "unsure",
      "label": "We are not sure whether this was written by a person or by AI.",
      "model_score": 0.5435,
      "status": "decided",
      "style_score": 0.5682,
      "timestamp": "2026-11-05T15:36:18+00:00"
    },
    {
      "combined_score": 0.0874,
      "content_id": "2979c638-d85a-46b3-bf32-a88ce0afe79a",
      "creator_id": "milestone5-human",
      "guess": "human",
      "label": "We think this was probably written by a person.",
      "model_score": 0.1424,
      "status": "decided",
      "style_score": 0.0324,
      "timestamp": "2026-11-05T15:36:18+00:00"
    },
    {
      "content_id": "6fb45c95-4274-42a0-a6f2-7a74a7b4250b",
      "creator_id": "milestone5-unsure",
      "event": "appeal",
      "reasoning": "I wrote this piece myself and would like a human review of the uncertain result.",
      "status": "under_review",
      "timestamp": "2026-11-05T15:36:28+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- _What I asked for:_
- _What came back:_
- _What I changed:_

**Moment 2**

- _What I asked for:_
- _What came back:_
- _What I changed:_

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** **_ per minute, _** per day

**Why those numbers and not others:**

<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ------- |
| 1.        |        |       |       |       |         |
| 2.        |        |       |       |       |         |
| 3.        |        |       |       |       |         |
| 4.        |        |       |       |       |         |
| 5.        |        |       |       |       |         |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
