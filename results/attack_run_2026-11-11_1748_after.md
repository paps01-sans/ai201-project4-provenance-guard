# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 17:48
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator*id `attacker*<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID      | Family             | Targeting                                              | Status | Content ID                             | Guess  | Score | Verdict |
| ------- | ------------------ | ------------------------------------------------------ | ------ | -------------------------------------- | ------ | ----- | ------- |
| EV01    | evasion            | signal two: typos raise word variety                   | 200    | `20c14df2-547e-473d-9402-333e44feb262` | human  | 0.325 | BROKE   |
| EV02    | evasion            | signal two: broken-up sentences raise length spread    | 200    | `eb7a137a-1357-4dfd-92d5-d24c46731f62` | unsure | 0.361 | BROKE   |
| EV03    | evasion            | signal two: a pasted quotation changes the shape       | 200    | `54a184d4-19d6-4597-ba90-8effd42d1ac0` | unsure | 0.496 | BROKE   |
| EV04    | evasion            | signal one: unusual words raise perplexity             | 200    | `9011e0a5-91a1-4b72-9e0a-43a898e3efc8` | unsure | 0.538 | BROKE   |
| EV05    | evasion            | both signals: heavy human editing pass                 | 200    | `810a6d9f-8ff1-4a33-81f8-71f69998e82f` | human  | 0.277 | BROKE   |
| EV06    | evasion            | signal two: one very long sentence and one very short  | 200    | `5962860c-7212-40a0-b403-0e0911d8ea7a` | unsure | 0.366 | BROKE   |
| EV07    | evasion            | signal two: padding with punctuation                   | 200    | `8825a490-a30f-4870-9d21-965a38ae926f` | unsure | 0.577 | BROKE   |
| EV08    | evasion            | signal one: text below the token window                | 200    | `82dea6a1-18b0-4c8f-bd94-922c8c46afeb` | human  | 0.302 | BROKE   |
| EV09    | evasion            | both: AI text with a human opening paragraph bolted on | 200    | `f9fa87c9-6301-40f1-b0b3-961c2acc50a2` | unsure | 0.508 | BROKE   |
| EV10    | evasion            | signal two: repeated stanza structure                  | 200    | `0147a812-8adf-4312-96b0-51c1a8b09c96` | ai     | 0.817 | HELD    |
| FP01    | false_positive     | plain, clear human writing with no flourishes          | 200    | `e109cedc-00ad-4ae8-ad94-60c661901bd6` | unsure | 0.523 | HELD    |
| FP02    | false_positive     | human writing in a formal register                     | 200    | `9b38110c-f395-43ef-b3c3-b202fc99b813` | unsure | 0.632 | HELD    |
| FP03    | false_positive     | a non-native English speaker writing carefully         | 200    | `84ef3ebe-e90b-468e-85af-fb77975ca20a` | ai     | 0.656 | BROKE   |
| FP04    | false_positive     | a student essay written to a rubric                    | 200    | `8c999806-9dbe-4e07-b226-8d23d36aea64` | unsure | 0.615 | HELD    |
| FP05    | false_positive     | technical documentation written by a person            | 200    | `c5d2ba72-cc99-40cd-bafb-ef1c7af8961e` | ai     | 0.657 | BROKE   |
| FP06    | false_positive     | a person imitating a formal template                   | 200    | `1f736f81-c361-4500-8716-69cf42c8461f` | unsure | 0.628 | HELD    |
| FP07    | false_positive     | human writing that repeats a phrase deliberately       | 200    | `bdc18a73-a1fc-46cc-b348-dd24127a0ce6` | unsure | 0.590 | HELD    |
| FP08    | false_positive     | very short genuine human submission                    | 200    | `73baad1d-bb0d-4c56-bdbb-b4dd63f055c6` | human  | 0.303 | HELD    |
| PI01    | prompt_injection   | instruction to ignore the check                        | 200    | `ade449ac-8e50-417b-8602-05f5ba08f29c` | unsure | 0.351 | HELD    |
| PI02    | prompt_injection   | instruction disguised as a system message              | 200    | `d9c88fe8-76d5-4c6d-aa4a-8f668bd981e4` | human  | 0.196 | HELD    |
| PI03    | prompt_injection   | instruction wrapped in the writer's voice              | 200    | `f47040a7-d328-42b5-a49d-1f26523bab80` | unsure | 0.490 | HELD    |
| PI04    | prompt_injection   | attempt to make the label text hostile                 | 200    | `94e8a6d4-33fa-40e2-925d-ae2e16b07d46` | unsure | 0.421 | HELD    |
| PI05    | prompt_injection   | attempt to inject into the audit log                   | 200    | `4372b1ac-c736-424b-9e42-23c838357b48` | unsure | 0.457 | HELD    |
| PI06    | prompt_injection   | instruction plus real human text                       | 200    | `abc2380f-ec47-4aa2-a7e9-256d2e1943d6` | unsure | 0.497 | HELD    |
| MF01    | malformed          | text is only whitespace                                | 400    | `—`                                    | —      | —     | HELD    |
| MF02    | malformed          | text is a single character                             | 400    | `—`                                    | —      | —     | HELD    |
| MF03    | malformed          | text is control characters                             | 200    | `9f6c062b-5652-4df2-aaa4-8b4d34e48752` | human  | 0.250 | BROKE   |
| MF04    | malformed          | text is only punctuation                               | 200    | `2c3fd396-d5bf-4b92-a876-2c6690ae07b8` | unsure | 0.506 | BROKE   |
| MF05    | malformed          | text is a very long single word                        | 400    | `—`                                    | —      | —     | HELD    |
| MF06    | malformed          | text is emoji only                                     | 400    | `—`                                    | —      | —     | HELD    |
| MF07    | malformed          | text is right-to-left script                           | 200    | `51d95bfc-055d-48c0-92ac-5a7906005c69` | ai     | 0.953 | BROKE   |
| MF08    | malformed          | text is 60,000 characters                              | 400    | `—`                                    | —      | —     | HELD    |
| RQ01    | malformed          | no text field at all                                   | 400    | `—`                                    | —      | —     | HELD    |
| RQ02    | malformed          | no creator_id                                          | 400    | `—`                                    | —      | —     | HELD    |
| RQ03    | malformed          | text is a number                                       | 400    | `—`                                    | —      | —     | HELD    |
| RQ04    | malformed          | text is a list                                         | 400    | `—`                                    | —      | —     | HELD    |
| RQ05    | malformed          | text is null                                           | 400    | `—`                                    | —      | —     | HELD    |
| RQ06    | malformed          | creator_id is an object                                | 400    | `—`                                    | —      | —     | HELD    |
| RQ07    | malformed          | body is a JSON array, not an object                    | 400    | `—`                                    | —      | —     | HELD    |
| RQ08    | malformed          | body is unparseable JSON                               | 400    | `—`                                    | —      | —     | HELD    |
| RQ09    | malformed          | body is empty                                          | 400    | `—`                                    | —      | —     | HELD    |
| RQ10    | malformed          | body is form-encoded, not JSON                         | 400    | `—`                                    | —      | —     | HELD    |
| RQ11    | malformed          | body is JSON claiming to be plain text                 | 400    | `—`                                    | —      | —     | HELD    |
| RQ12    | malformed          | deeply nested JSON                                     | 400    | `—`                                    | —      | —     | HELD    |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `a2c51d59-d4ff-4f5c-9921-a593e15ec1cd` | human  | 0.290 | BROKE   |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `0f44a44d-7fe1-465c-b7c5-41d5bddfcd1d` | human  | 0.290 | BROKE   |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `20367e09-5a17-45d6-8636-fe2676344a8a` | human  | 0.290 | BROKE   |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `c5a13f7c-072d-43a1-a5df-194afa206df4` | human  | 0.290 | BROKE   |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `e5f21eb9-5b71-46e2-9c47-20ebe900711c` | human  | 0.290 | BROKE   |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `132c3763-b1e0-430a-a2ba-7ecadaae2a78` | human  | 0.290 | BROKE   |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `1d4ddc7b-d0e1-430b-8c52-1ac1daaadd1a` | human  | 0.290 | BROKE   |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `143e7c74-17f7-40cb-b7d4-ce4486f1a6b8` | human  | 0.290 | BROKE   |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `158e00ce-0789-4b1f-b497-d10e00201730` | human  | 0.290 | BROKE   |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `9dd3b310-458a-4b63-973a-214f88dcf90a` | human  | 0.290 | BROKE   |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |

---

## By family

| Family               | Attacks | Auto-BROKE | Left to judge |
| -------------------- | ------- | ---------- | ------------- |
| `evasion`            | 10      | 0          | 10            |
| `false_positive`     | 8       | 0          | 8             |
| `flood_same_creator` | 12      | 0          | 12            |
| `malformed`          | 20      | 0          | 20            |
| `prompt_injection`   | 6       | 0          | 6             |

**Overall verdict:** 32 held, 24 broke.

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

_Targeting:_ signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "20c14df2-547e-473d-9402-333e44feb262",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3247,
  "model_score": 0.1635,
  "style_score": 0.4859,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

_Targeting:_ signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "eb7a137a-1357-4dfd-92d5-d24c46731f62",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3612,
  "model_score": 0.5943,
  "style_score": 0.1281,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

_Targeting:_ signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "54a184d4-19d6-4597-ba90-8effd42d1ac0",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4963,
  "model_score": 0.6662,
  "style_score": 0.3264,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

_Targeting:_ signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "9011e0a5-91a1-4b72-9e0a-43a898e3efc8",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5384,
  "model_score": 0.6114,
  "style_score": 0.4654,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

_Targeting:_ both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "810a6d9f-8ff1-4a33-81f8-71f69998e82f",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2765,
  "model_score": 0.3212,
  "style_score": 0.2319,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

_Targeting:_ signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "5962860c-7212-40a0-b403-0e0911d8ea7a",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.3659,
  "model_score": 0.5727,
  "style_score": 0.159,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

_Targeting:_ signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "8825a490-a30f-4870-9d21-965a38ae926f",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5771,
  "model_score": 0.5862,
  "style_score": 0.568,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

_Targeting:_ signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "82dea6a1-18b0-4c8f-bd94-922c8c46afeb",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3019,
  "model_score": 0.2452,
  "style_score": 0.3586,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

_Targeting:_ both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "f9fa87c9-6301-40f1-b0b3-961c2acc50a2",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5082,
  "model_score": 0.7042,
  "style_score": 0.3122,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

_Targeting:_ signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "0147a812-8adf-4312-96b0-51c1a8b09c96",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8174,
  "model_score": 0.9792,
  "style_score": 0.6556,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

_Targeting:_ plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "e109cedc-00ad-4ae8-ad94-60c661901bd6",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5233,
  "model_score": 0.6175,
  "style_score": 0.4292,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

_Targeting:_ human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "9b38110c-f395-43ef-b3c3-b202fc99b813",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6325,
  "model_score": 0.7387,
  "style_score": 0.5263,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

_Targeting:_ a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "84ef3ebe-e90b-468e-85af-fb77975ca20a",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6559,
  "model_score": 0.8051,
  "style_score": 0.5066,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

_Targeting:_ a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "8c999806-9dbe-4e07-b226-8d23d36aea64",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6152,
  "model_score": 0.8329,
  "style_score": 0.3975,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

_Targeting:_ technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c5d2ba72-cc99-40cd-bafb-ef1c7af8961e",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6574,
  "model_score": 0.8005,
  "style_score": 0.5144,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

_Targeting:_ a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "1f736f81-c361-4500-8716-69cf42c8461f",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6278,
  "model_score": 0.8814,
  "style_score": 0.3742,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

_Targeting:_ human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "bdc18a73-a1fc-46cc-b348-dd24127a0ce6",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5895,
  "model_score": 0.8816,
  "style_score": 0.2973,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

_Targeting:_ very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "73baad1d-bb0d-4c56-bdbb-b4dd63f055c6",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3029,
  "model_score": 0.3223,
  "style_score": 0.2835,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

_Targeting:_ instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "ade449ac-8e50-417b-8602-05f5ba08f29c",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3515,
  "model_score": 0.4625,
  "style_score": 0.2405,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

_Targeting:_ instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "d9c88fe8-76d5-4c6d-aa4a-8f668bd981e4",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1959,
  "model_score": 0.2044,
  "style_score": 0.1874,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

_Targeting:_ instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "f47040a7-d328-42b5-a49d-1f26523bab80",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4902,
  "model_score": 0.5943,
  "style_score": 0.386,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

_Targeting:_ attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "94e8a6d4-33fa-40e2-925d-ae2e16b07d46",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4213,
  "model_score": 0.4998,
  "style_score": 0.3428,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

_Targeting:_ attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "4372b1ac-c736-424b-9e42-23c838357b48",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4572,
  "model_score": 0.6401,
  "style_score": 0.2743,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

_Targeting:_ instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "abc2380f-ec47-4aa2-a7e9-256d2e1943d6",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4968,
  "model_score": 0.5583,
  "style_score": 0.4352,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

_Targeting:_ text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

_Targeting:_ text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

_Targeting:_ text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "9f6c062b-5652-4df2-aaa4-8b4d34e48752",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.25,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

_Targeting:_ text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "2c3fd396-d5bf-4b92-a876-2c6690ae07b8",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5056,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We are not sure whether this was written by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

_Targeting:_ text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

_Targeting:_ text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

_Targeting:_ text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "51d95bfc-055d-48c0-92ac-5a7906005c69",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "We think this was probably written by AI.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

_Targeting:_ text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

_Targeting:_ no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

_Targeting:_ no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

_Targeting:_ text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

_Targeting:_ text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

_Targeting:_ text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

_Targeting:_ creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

_Targeting:_ body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

_Targeting:_ body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

_Targeting:_ body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

_Targeting:_ body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

_Targeting:_ body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

_Targeting:_ deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "a2c51d59-d4ff-4f5c-9921-a593e15ec1cd",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "0f44a44d-7fe1-465c-b7c5-41d5bddfcd1d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "20367e09-5a17-45d6-8636-fe2676344a8a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c5a13f7c-072d-43a1-a5df-194afa206df4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "e5f21eb9-5b71-46e2-9c47-20ebe900711c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "132c3763-b1e0-430a-a2ba-7ecadaae2a78",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "1d4ddc7b-d0e1-430b-8c52-1ac1daaadd1a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "143e7c74-17f7-40cb-b7d4-ce4486f1a6b8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "158e00ce-0789-4b1f-b497-d10e00201730",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "9dd3b310-458a-4b63-973a-214f88dcf90a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2903,
  "model_score": 0.0287,
  "style_score": 0.5519,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
