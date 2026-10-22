---
name: fb-reply
description: >-
  Handles comments under the page owner's own posts: pulls them through Composio
  or takes pasted ones, sorts them by value, and drafts replies for the ones that
  deserve one, including critics and potential customers. Also covers Messenger
  etiquette. Use when the user says "reply to comments", "what did they write",
  "someone wrote", "I have a troll", "comments under my post", "handle my comments".
---

# fb-reply

The thread under your own post is where part of reach is decided. Every reply is
another interaction, and those in the first hour do the most work. Comments are not
equally valuable, so this skill sorts first and writes second.

## Input

- **Through Composio:** `FACEBOOK_GET_PAGE_POSTS` -> pick a post ->
  `FACEBOOK_GET_COMMENTS` (`object_id` of the post; `order`, `limit` as needed;
  replies to a comment: use the comment's id as `object_id`). Error #10 = no
  permission to read engagement: say so and ask for pasted comments. A wrong
  `object_id` returns an empty `{data: []}` even though the call succeeded.
- **Pasted** comments, ideally with names. Screenshots are fine.

Do not scrape the thread with a browser.

## Triage (say the counts out loud)

| Bucket | What it is | What it gets |
|--------|-----------|--------------|
| **LEAD / CUSTOMER** | someone describing the problem you solve | a full public answer, with one sentence of "door" at the end |
| **SUBSTANCE** | adds data, disagrees, extends | the longest reply on the thread |
| **QUESTION** | a question many people have | an answer, and if it keeps coming up: a topic for the next post or video (hand to `/fb-post` / `/fb-reel` as the "verbatim question" hook) |
| **KEYWORD** | if the post asked for a specific word | the promised thing, sent by hand |
| **SUPPORT** | "great", "thanks", a tag | a reaction, maybe 3-8 words |
| **NOISE** | advert, spam, bait | nothing, or hide/report |

Write in that order and stop when the value stops.

## How to reply

- **Answer the actual question.** If someone asks "how", say how, here, now. Do not
  push them to private messages for an answer you could have given.
- **Use the name once**, at the start, no exclamation mark.
- **Match the length.** Four words do not get four sentences.
- **To a critic:** concede the true part first, in their words, then hold your line.
  Do not delete, do not get defensive, do not reply twice in the same thread.
- **To a troll:** nothing. A reply is reach for them. Hiding an abusive comment is
  allowed and is not losing. Facebook has its own reporting tools.
- **To a customer:** answer fully in public. The door is one sentence, an offer of
  help, not a pitch. The public answer is what makes the next person write.
- Promise nothing the owner has not promised. Do not invent prices or dates.
- Always run replies through `/fb-human` (a comment is short, so a cliche or a dash is
  louder than in a post).

## Messenger

Private messages follow different rules. When the owner writes to someone:

1. **A reply to a raised hand** (they messaged the Page, answered a post, asked for
   a resource) converts best because it is not outreach. Deliver what they asked
   for at once, with no "first tell me what you do" gate.
2. **A warm approach:** someone you have already talked to in comments. Two to four
   sentences, refer to the specific thing, give before you ask, one small ask.
3. **Cold messages to strangers** are the lowest-yield thing you can do and the
   fastest route to account restrictions. If asked, say so and suggest two weeks of
   commenting first.
4. Two follow-ups at most: after 4 days with something new, after 10 days a
   closing note. Then stop.
5. Never automated, never in bulk. The skill drafts; the owner sends. Composio has
   no Messenger tools here and nothing is done through that channel.

## Sending replies

By default **the owner pastes replies themselves**. If they ask you to send through
Composio (`FACEBOOK_CREATE_COMMENT`, `object_id` + `message`):

- the same gate as `fb-publish`: show the full set (to whom, under which comment,
  the text) and wait for "yes" over **that** set;
- one call per comment, no blind retries; composite ids with an underscore can
  return `successful:false` even with status 200, so verify with
  `FACEBOOK_GET_COMMENTS` before trying again;
- direct a reply to the comment, not the post;
- do not edit or delete comments (`UPDATE_COMMENT`, `DELETE_COMMENT`) without a
  separate, specific instruction.

## Output

One block grouped by bucket, every reply ready to paste and already through
`fb-human`:

```
REPLIES  |  42 comments  |  3 CUSTOMER, 2 SUBSTANCE, 2 QUESTION, 30 SUPPORT, 5 NOISE

CUSTOMER
Anna K. - "I had exactly this in June"
> Anna, what fixed it for us was moving the payment trigger from approval to delivery.
> Happy to share the wording if it helps.

QUESTION -> POST
Peter - "what if they refuse to sign?"  (11 reactions). That is a video topic, not a reply.

NOISE (5)  skipped
```

Then the gate: nothing is sent until the owner says "yes".
