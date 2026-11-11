"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            "I missed the bus after class and ended up walking home in the cold. It was annoying at first, but the quiet walk gave me time to think.",
            "My roommate bought a plant and forgot to water it. I started taking care of it, and now I check the leaves before I check my phone.",
            "The library was packed today, so I sat near the window. I finished less work than planned, but I liked watching people hurry across the quad.",
            "I tried cooking rice without looking at the instructions. It came out too sticky, but the vegetables were good enough to make dinner work.",
            "A friend sent me a picture from home. It made me miss my family for a minute, then we started joking about the old couch in the background.",
            "I kept putting off a short assignment because I thought it would take forever. It took twenty minutes once I finally opened the document.",
            "The coffee shop played the same song twice while I was studying. I noticed the second time and decided it was probably a sign to leave.",
            "I found a coin under my desk while cleaning. It was not worth much, but finding it made the boring chore feel slightly less pointless.",
            "The weather changed three times before lunch. I carried an umbrella, wore a jacket, and still ended up being completely wrong about what the day wanted.",
            "I called my grandmother after dinner and listened to her explain a recipe I have never managed to make correctly. I wrote down the part about adding patience.",
        ],
    },
    {
        "name": "score spread",
        "criterion": 2,
        "texts": [
            "The implementation of the proposed framework requires careful consideration of several key factors. The system should provide reliable results across a wide range of inputs and maintain consistent performance over time.",
            "The following procedure provides a structured approach to the problem. First, the relevant information is collected. Next, the information is analyzed. Finally, the result is evaluated against the stated requirements.",
            "Effective project management depends on clear communication, consistent planning, and careful attention to measurable outcomes. These principles support reliable execution and improve the quality of the final result.",
            "The proposed solution offers several important benefits. It improves efficiency, reduces unnecessary complexity, and supports a consistent user experience across different operating conditions.",
            "A successful implementation requires appropriate preparation, regular monitoring, and a willingness to make adjustments when new information becomes available. This process helps maintain stable performance.",
            "I left my keys in the fridge again. I found them beside the mustard and laughed so hard that I forgot why I was in the kitchen.",
            "The rain kept changing its mind. I started writing about my bus ride, then remembered the orange cat under the bakery table and forgot where the sentence was going.",
            "My shoes were soaked before I reached the corner, and one sock started sliding under my heel. I bought a newspaper from the shop even though I do not read newspapers.",
            "I planned to clean the whole room, but I found an old ticket under the bed and spent half an hour trying to remember the night it came from. The room stayed messy.",
            "There was a blue mug on the library steps after class. I moved it under the roof, then worried that someone had left it there on purpose and would think I had ruined the plan.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            "The system works. " * 20,
            "Whisper. The rain kept changing its mind, tapping the windows, stopping, then returning with a sharper rhythm; somewhere beyond the laundromat, a violinist practiced the same crooked phrase until it became beautiful. I forgot my umbrella. Ah!",
            "I walked home after class and noticed the same blue mug on the library steps. I do not know who left it there, but it made the whole afternoon feel strangely personal.",
        ],
    },
    {
        "name": "appeal path",
        "criterion": 4,
        "appeal": True,
        "reasoning": "I wrote this piece myself and would like a human review of the result.",
        "texts": [
            "I made dinner late because I lost track of time. The noodles were overcooked, but I ate them anyway while watching the rain.",
            "My notes looked clear until I tried to study from them. I think I understood the lecture, but my handwriting disagrees.",
            "I walked past the gym and heard someone practicing the same song on a piano. They missed one note every time, which somehow made it nicer.",
            "The printer stopped working right before I needed it. I restarted it twice, stared at the screen, and then used the computer lab instead.",
            "I found an old receipt in my jacket and remembered the sandwich I bought that day. It was not a big memory, but it came back very clearly.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_empty", "text": ""},
            {"creator_id": "eval_bad_missing"},
            {"creator_id": "eval_bad_null", "text": None},
            {"creator_id": "eval_bad_huge", "text": "word " * 50000},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
