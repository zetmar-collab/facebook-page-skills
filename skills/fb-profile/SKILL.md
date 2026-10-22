---
name: fb-profile
description: >-
  Scores a Facebook Page out of 100 and rewrites the parts that lose points: name,
  category, About text, action button, link, profile picture, cover, pinned post,
  featured. Use when the user says "improve my page", "page description", "score my
  page", "why does nobody follow me", "page button", "optimise my profile".
---

# fb-profile

A Page is not a shop window that people browse. It is a **decision screen**, arrived
at from one post or video, with about three seconds to answer one question: is there
more of this here, and is it for me?

## Input

Ask the user to paste or screenshot: the Page name, the @handle, the category, the
About text, the action button, links, the profile picture, the cover, the pinned
post, the Featured section and the six latest posts. Do not log in to Facebook.

From Composio you can safely read `FACEBOOK_GET_PAGE_DETAILS` (fields such as
`name,about,category,link,website,description`; an unsupported field gives error
#100, so start with a short list) and `FACEBOOK_GET_PAGE_POSTS`. This needs an
active connection. The pinned post, button and Featured items are often visible only
in a screenshot.

**A note on profiles.** If the user's presence is a personal profile, not a Page,
this rubric describes the Page they could create; a personal profile has different
fields. Check what you are dealing with first, and say so.

## Score

Twelve elements, 100 points. Score harshly: a first pass usually lands around
30-40, and a generous score is useless.

| Element | Pts | Full marks |
|---------|-----|------------|
| Name | 10 | name + the words people search for, not just a brand name |
| Category | 4 | accurate, not "Public figure" for lack of an idea |
| Profile picture | 6 | a face or logo legible in the small circle |
| Cover | 8 | one promise in one sentence, not a collage |
| About: first line | 14 | for whom and what changes; not a job title or a list of identities |
| About: the rest | 8 | one piece of proof or one plain offer |
| Action button | 8 | one button that answers the promise in the About text |
| Link | 8 | one address matching the promise |
| Pinned post | 12 | the best proof or the clearest explanation of the offer |
| Featured / photos | 6 | tidy, no accidents |
| Consistency of the last 6 posts | 8 | one theme is visible |
| Contact details | 8 | current, no empty fields |

Show the table, the total and one sentence on the biggest loss. If you have not seen
an element (e.g. no screenshot of the pinned post), write "not scored" instead of
guessing.

## Then rewrite, in order of points lost

Not everything at once; the owner has to change each by hand.

1. **Name.** Format `{Name} | {what you do, in searched words}`. Three options. Page
   renames can be subject to Facebook review and change limits; say so, and do not
   promise an instant effect.
2. **First line of About.** For whom and what changes.
3. **Pinned post.** The highest-leverage fix, four clicks: the best proof, the
   clearest explanation, or "who I am". Without a pinned post a visitor sees
   whatever was posted last, which is a coin flip.
4. **Button and link.** One door instead of a menu: a menu converts worse.
5. **Cover and picture.** One sentence of promise. A cover as an image, not a list
   of services.

## Output

The table, then the rewritten fields as ready blocks in "do this first" order, each
through `/fb-human`, then a re-score with an honest delta. If the rewrite gets 76 and
not 98, write 76 and what is left: usually a real photo, regular videos and a pinned
post that does not exist yet. None of that is a rewrite.

The skill changes nothing on Facebook: the owner edits each field. Composio has no
tools for editing a Page here, and do not try to work around that with a browser.
