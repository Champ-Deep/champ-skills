# Discovery Prep

Builds the pre-call brief for a discovery call: hypothesis, five questions, likely objections and what a win looks like.

## Give Claude
- Who you are meeting, their title, the company, and how the call was booked
- What you sell and the outcome it produces, in two lines
- Optional: pasted research: news, job posts, their site copy, a previous call note
- Optional: the last touch: what you sent and what they replied
- Optional: who else will be on the call

## Claude does
1. Write a three-line hypothesis: what is probably broken, why now, what it costs them if unchanged. Label it hypothesis.
2. Write five questions ordered from situation to payoff, each with what a strong answer would reveal.
3. Draft the three objections most likely for this account, each with a one-line acknowledgment and the question that follows it.
4. Define the win in one sentence: what they have after buying that they lack now, in words they would use.
5. List what you must not assume going in: headcount, budget, tool, timeline, unless pasted.
6. Give the next step to ask for, and the fallback ask if they are not ready to commit.
7. Add one question about a person not yet met, so the committee gap closes early.
8. Flag any fact you would normally look up before a call, with the search to run.

## Output
- Hypthesis: three labelled lines.
- Question table: `question | what a strong answer reveals`, five rows in ask order.
- Objections: objection, acknowledgment, follow-up question, three sets.
- Win sentence, the ask, and the fallback ask, each verbatim.
- Assumptions list: the facts you do not have and must not pretend to.

## Rules
- The hypothesis stays labelled until the call confirms it. Never present it as their stated problem.
- Five questions only. A longer list kills the conversation.
- Objections must follow from this account's input, not generic fears.
- Do not invent their tools, headcount, budget or timeline.
- No pricing promises, discounts or competitive claims in a prep note.
- Never write a question whose answer you could have looked up in two minutes.
