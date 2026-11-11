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

- _What I asked for:_ I asked for help tracing a submission from the API route
  through the detector, stylometry signal, scoring rule, label, and audit log.
- _What came back:_ The response broke the pipeline into seven steps and
  pointed out that model predictability and text shape have different blind
  spots.
- _What I changed:_ I wrote the trace in my own words, kept the false-positive
  case focused on plain human writing, and added the blind spots to the
  Signals and Scoring section.

**Moment 2**

- _What I asked for:_ I asked for help implementing and testing the second
  signal, combined score, reader labels, and appeal workflow without hiding
  uncertain results.
- _What came back:_ The response suggested testing the signal on its own,
  using an equal-weight average, checking all three label bands, and verifying
  an appeal with a real content id in the audit log.
- _What I changed:_ I adjusted the sentence-spread normalization after the
  calibration results, chose the final label wording and thresholds, tested
  three real label outputs, and confirmed the appeal became `under_review`.

**Moment 3**

- _What I asked for:_ I asked for help choosing one improvement from the attack
  diagnoses and measuring it without changing the other parts of the service.
- _What came back:_ The response focused on route validation because the first
  run had a short-input crash and accepted a very large body.
- _What I changed:_ I added the 3-word and 10,000-character limits, reran the
  full attack set and all five criteria, and recorded that malformed failures
  dropped from 7 to 3 while the other weaknesses stayed the same.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**

Ten submissions per minute gives a real writer enough room to correct or
resubmit work without waiting, while stopping a script from rapidly mapping
the score thresholds. Two hundred per day supports normal writing activity but
puts a clear ceiling on a long automated probing run.

<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Requests count per `creator_id`. If a request has no usable creator id, the
limiter falls back to the caller's address. This is the per-creator stretch
feature: separate writers on one address do not share a bucket, while one
creator cannot avoid the limit by changing request details.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

The flood used one `creator_id`, and 5 of 15 requests were rate limited. The
429 handler recorded each rejected request with `reason: "rate_limited"` and
the active limit.

**Recent log evidence from three normal submissions and one bad request:**

```json
{
     "combined_score": 0.2677,
     "content_id": "6843cb4f-757d-4b59-aa46-e5f2e2a57a13",
     "creator_id": "milestone1-writer-0",
     "guess": "human",
     "label": "We think this was probably written by a person.",
     "model_score": 0.0021,
     "style_score": 0.5333,
     "status": "decided",
     "timestamp": "2026-11-11T15:13:54+00:00"
}
{
     "creator_id": "flood_tester",
     "event": "rejected",
     "limit": "10 per 1 minute",
     "reason": "rate_limited",
     "status": "rejected",
     "timestamp": "2026-11-11T15:13:36+00:00"
}
{
     "creator_id": "milestone1-bad-input",
     "event": "rejected",
     "reason": "invalid_text",
     "status": "rejected",
     "timestamp": "2026-11-11T15:19:19+00:00"
}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

The full first-pass report is [results/attack_run_2026-11-11_1627.md](results/attack_run_2026-11-11_1627.md).
I marked 28 attacks HELD and 28 BROKE. The broken cases were 9 evasion
attacks, 2 false positives, 7 malformed inputs, and 10 flood requests. All 6
prompt-injection attacks were HELD because the text was treated as content,
not as instructions to the service.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
[
  {
    "timestamp": "2026-11-11T21:27:13+00:00",
    "content_id": "24bb523a-bbf1-4440-8b50-3a4e2e33437b",
    "creator_id": "attacker_EV05",
    "guess": "human",
    "model_score": 0.3212,
    "style_score": 0.2319,
    "combined_score": 0.2765,
    "label": "We think this was probably written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T21:27:18+00:00",
    "content_id": "3dfbe575-9526-4050-9af2-6f9de4f6cd64",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "model_score": 0.8051,
    "style_score": 0.5066,
    "combined_score": 0.6559,
    "label": "We think this was probably written by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T21:27:19+00:00",
    "content_id": "a09b7e1b-cd78-4d19-910e-d06d8340aa05",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "model_score": 0.8005,
    "style_score": 0.5144,
    "combined_score": 0.6574,
    "label": "We think this was probably written by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T21:27:32+00:00",
    "content_id": "c2537941-3d18-4b65-beaa-1d70298f87b2",
    "creator_id": "attacker_MF06",
    "guess": "ai",
    "model_score": 0.9969,
    "style_score": 1.0,
    "combined_score": 0.9985,
    "label": "We think this was probably written by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T21:27:35+00:00",
    "content_id": "494831f2-fb61-4b3a-a056-00e3938733c2",
    "creator_id": "attacker_MF08",
    "guess": "ai",
    "model_score": 0.9876,
    "style_score": 0.6545,
    "combined_score": 0.8211,
    "label": "We think this was probably written by AI.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T21:27:36+00:00",
    "content_id": "1384e6b5-1a9f-47e1-9c60-bd829d1c015d",
    "creator_id": "attacker_flood",
    "guess": "human",
    "model_score": 0.0287,
    "style_score": 0.5519,
    "combined_score": 0.2903,
    "label": "We think this was probably written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T21:27:40+00:00",
    "content_id": "4d347872-f695-4662-bfd2-5fcc72a9ac5e",
    "creator_id": "attacker_flood",
    "guess": "human",
    "model_score": 0.0287,
    "style_score": 0.5519,
    "combined_score": 0.2903,
    "label": "We think this was probably written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T21:27:40+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "10 per 1 minute"
  },
  {
    "timestamp": "2026-11-11T21:27:35+00:00",
    "creator_id": "attacker_RQ01",
    "event": "rejected",
    "status": "rejected",
    "reason": "invalid_text"
  },
  {
    "timestamp": "2026-11-11T21:27:36+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "invalid_json_object"
  }
]
```

**The single worst outcome**

FP03 is the outcome I would least want to explain to a writer. The attack set
describes it as careful writing by a non-native English speaker, but the
service returned `ai` with a combined score of `0.6559`, just over the `0.65`
threshold. The model score was `0.8051`, so the main failure is signal one
mistaking predictable careful language for evidence of AI authorship. The
equal-weight rule then preserved that accusation instead of moving it into the
unsure band.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion                       | Target                               | Run 1                  | Run 2                  | Run 3                  | Verdict |
| ------------------------------- | ------------------------------------ | ---------------------- | ---------------------- | ---------------------- | ------- |
| 1. My own writing flagged as AI | <= 1 of 10                           | 1/10                   | 1/10                   | 1/10                   | MET     |
| 2. Score spread                 | AI avg 0.65+, human avg 0.35 or less | AI 0.491 / human 0.394 | AI 0.491 / human 0.394 | AI 0.491 / human 0.394 | MISSED  |
| 3. All three labels reachable   | 3 of 3                               | 3/3                    | 3/3                    | 3/3                    | MET     |
| 4. Appeal changes status        | 5 of 5                               | 5/5                    | 5/5                    | 5/5                    | MET     |
| 5. Bad input returns 4xx        | 4 of 4                               | 3/4                    | 3/4                    | 3/4                    | MISSED  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Source: `results/run_2026-11-11_1644_before.md`, produced by
`run_eval.py::main`. These are the Trial 1 results.

### Criterion 1: my own writing

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6522,
    "model_score": 0.7258,
    "style_score": 0.5786,
    "label": "We think this was probably written by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4705,
    "model_score": 0.5057,
    "style_score": 0.4352,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3644,
    "model_score": 0.2915,
    "style_score": 0.4373,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4401,
    "model_score": 0.5112,
    "style_score": 0.369,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4637,
    "model_score": 0.6303,
    "style_score": 0.297,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5025,
    "model_score": 0.4963,
    "style_score": 0.5086,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5526,
    "model_score": 0.516,
    "style_score": 0.5892,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3663,
    "model_score": 0.3787,
    "style_score": 0.354,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.2564,
    "model_score": 0.3275,
    "style_score": 0.1852,
    "label": "We think this was probably written by a person."
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.339,
    "model_score": 0.3441,
    "style_score": 0.3339,
    "label": "We think this was probably written by a person."
  }
]
```

### Criterion 2: score spread

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6122,
    "model_score": 0.6858,
    "style_score": 0.5387,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6112,
    "model_score": 0.801,
    "style_score": 0.4213,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5066,
    "model_score": 0.5328,
    "style_score": 0.4804,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4068,
    "model_score": 0.5903,
    "style_score": 0.2233,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3185,
    "model_score": 0.4928,
    "style_score": 0.1443,
    "label": "We think this was probably written by a person."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5294,
    "model_score": 0.6791,
    "style_score": 0.3798,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.1466,
    "model_score": 0.1144,
    "style_score": 0.1787,
    "label": "We think this was probably written by a person."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5133,
    "model_score": 0.4854,
    "style_score": 0.5412,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.37,
    "model_score": 0.5975,
    "style_score": 0.1424,
    "label": "We are not sure whether this was written by a person or by AI."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4122,
    "model_score": 0.4412,
    "style_score": 0.3831,
    "label": "We are not sure whether this was written by a person or by AI."
  }
]
```

### Criterion 3: label coverage

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8899,
    "model_score": 0.9948,
    "style_score": 0.785,
    "label": "We think this was probably written by AI."
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.0874,
    "model_score": 0.1424,
    "style_score": 0.0324,
    "label": "We think this was probably written by a person."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5558,
    "model_score": 0.5435,
    "style_score": 0.5682,
    "label": "We are not sure whether this was written by a person or by AI."
  }
]
```

### Criterion 4: appeal path

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5766,
    "appeal_http_status": 200,
    "appeal_status": "under_review",
    "appeal_message": "Your appeal was received and is now under review."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3726,
    "appeal_http_status": 200,
    "appeal_status": "under_review",
    "appeal_message": "Your appeal was received and is now under review."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3614,
    "appeal_http_status": 200,
    "appeal_status": "under_review",
    "appeal_message": "Your appeal was received and is now under review."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4708,
    "appeal_http_status": 200,
    "appeal_status": "under_review",
    "appeal_message": "Your appeal was received and is now under review."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5461,
    "appeal_http_status": 200,
    "appeal_status": "under_review",
    "appeal_message": "Your appeal was received and is now under review."
  }
]
```

### Criterion 5: bad input

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_null\", \"text\": null}"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.9988,
    "model_score": 0.9975,
    "style_score": 1.0,
    "label": "We think this was probably written by AI.",
    "sent": "word word word word word word word word word word word word word word "
  }
]
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

### Criterion 2: score spread, MISSED

The stage is mainly signal one, with help from the combining rule. The clearly
AI texts averaged only `0.491`, below my `0.65` target, while the clearly human
texts averaged `0.394`, above my `0.35` target. The model signal gave several
human examples fairly high predictability scores, and the style signal also
gave some AI examples low AI-likeness scores. Since the combining rule gives
both signals equal weight, those overlapping scores stayed in the unsure band
instead of separating the two groups. The target was measurable, so I am not
revising it just because the system missed it.

### Criterion 5: bad input, MISSED

The stage is the route. Three of the four bad-input cases returned 400, but the
oversized `word ` body returned 200 and received an AI label. The route checks
that `text` is a non-empty string but has no maximum length check. The detector
then truncates the huge input to its token window and scores it like normal
content. The mechanism is missing input-size validation, not a threshold
problem. The target was clear, so I am keeping the original criterion.

### Broken attack patterns

The evasion failures were mostly signal two: EV02, EV03, EV06, EV07, and EV09
changed sentence shape, quotations, or punctuation so the style score moved
the AI text into the unsure band. The stage is signal two, and the mechanism is
that surface edits change sentence spread or punctuation without changing
authorship. EV04 and EV08 reached signal one: unusual words raised perplexity
and text below the token window changed what the model saw, so the model score
dropped. The stage is signal one, and the mechanism is that predictability is
not the same as authorship. EV05 fooled both signals with heavy editing and
was labeled human, so its stages are signal one and signal two together.
EV01 never returned a JSON response and timed out, so its stage is the route
around the detector call. The mechanism was a request that did not complete,
which is a service failure before labeling.

FP03 and FP05 were the two false positives. They reached the label mapping
with scores just above `0.65`, but the main stage was signal one: careful
formal or technical human writing was predictable to the local model. The
equal-weight combining rule kept the score above the AI threshold instead of
letting the style signal move it into unsure. This is the most important human
impact because the system accused real writers.

MF02 was a route failure because a one-character string reached
`detector.perplexity`, which raised `ValueError` instead of returning a JSON
400 response. MF03 and MF04 were also route validation failures because
control characters and punctuation-only text passed the non-empty-string check
and were scored as submissions. MF05, MF06, MF07, and MF08 show the same
missing-boundary problem for a long word, emoji, right-to-left text, and a
60,000-character body. The route accepted them, then the signals interpreted
them as text and produced confident scores. The attack mechanism is missing
content and size validation before signal one and signal two run.

FL01_01 through FL01_10 broke because the limiter allows the configured burst
of 10 requests per minute. FL01_11 and FL01_12 were held with 429. The stage
is the rate-limit layer, and the mechanism is that the chosen limit stops the
attack only after ten submissions, so the first half of the 20-request attack
still gets through. All prompt-injection attacks were held because the route
treats their instructions as ordinary text and never executes them.

---

## The Improvement

**What I changed:** I added one route-level input validation check in
`app.py::submit`. Text with fewer than 3 words or more than 10,000 characters
now returns a JSON 400 and is logged as a rejection before either signal runs.

**Which diagnosis pointed at it:** The malformed-input diagnosis showed that a
one-character request crashed inside signal one and a 60,000-character request
was accepted as a normal decision. I changed the route because the failure was
input validation, not scoring.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

The full after report is [results/attack_run_2026-11-11_1748_after.md](results/attack_run_2026-11-11_1748_after.md).
The after criteria report is [results/run_2026-11-11_1749_after.md](results/run_2026-11-11_1749_after.md).

| Measurement                   |          Before |           After |
| ----------------------------- | --------------: | --------------: |
| Auto-marked attack crashes    |               2 |               0 |
| Broken attacks                |              28 |              24 |
| Held attacks                  |              28 |              32 |
| Broken malformed attacks      |               7 |               3 |
| Criterion 5 bad-input verdict |     MISSED, 3/4 |        MET, 4/4 |
| Other criteria                | 3 MET, 2 MISSED | 3 MET, 2 MISSED |

**Did it help, and how do I know:** Yes. The change stopped the short-input
crash, rejected oversized input, reduced broken attacks by 4, and moved
criterion 5 from 3/4 to 4/4 in all three trials. It did not improve the
evasion, false-positive, score-spread, or flood results, which is expected
because I did not change those stages.

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

EV01 through EV09 are still broken evasion cases. EV01, EV02, EV03, EV06,
EV07, and EV09 mainly get through signal two because typos, sentence breaks,
quotes, punctuation, and added human text change the surface statistics. I
would replace the simple style measures with features that are less easy to
change, or add a semantic signal. EV04 and EV08 still get through signal one
because unusual words and the token window change the model's predictability;
I would calibrate the detector on longer examples and test more than one model.
I stopped because both fixes would be a second improvement and would need a new
calibration run.

FP03 and FP05 are still false positives. Signal one gives careful non-native
English writing and technical writing high predictability scores, and the
combining rule leaves the scores just above the AI threshold. I would lower the
model weight or widen the unsure band, but I stopped because that could let
more AI writing pass and I did not want to mix a scoring change with the input
validation experiment.

MF03, MF04, and MF07 still pass the route because they contain enough
characters or whitespace for the new boundary, even though they are control
characters, punctuation-only text, or right-to-left text with no normal words.
I would reject text with no tokens from `stylometry.words()` and add an
explicit policy for unsupported characters. I stopped after fixing the crash
and oversized-body cases because the milestone asks for one measured change.

FL01_01 through FL01_10 still get 200 before the limiter returns 429 on
FL01_11 and FL01_12. I would lower the per-minute limit or add a shorter burst
limit, but that would make normal correction and resubmission harder for real
writers, so I left the chosen 10-per-minute trade unchanged.

Criterion 2 is still MISSED. The AI average stayed at `0.491` instead of
`0.65`, and the human average stayed at `0.394` instead of at most `0.35` in
all three trials. I would collect a better calibration set and retune the
signal weights, but I stopped because the one input-validation change already
had a measurable result and changing scoring now would make the comparison less
clear.

**The trade I'd make if this ran for real:**

I would widen the unsure band to reduce false accusations, even though edited
AI text would get through more often. Real writers would pay less of the cost
of detector mistakes, while the site would pay by accepting more uncertain AI
submissions.

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
