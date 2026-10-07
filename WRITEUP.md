# HW1 writeup

**Name:** Colin Mathews
**Date:** 2026-10-06

Every placeholder below gets your answer, told to Claude or typed in here yourself. Every number
you give comes from a script in this repo; say which one. Claude may format tables and figures
here; the words are yours.

## Part 0. Predictions

Give these to Claude before any analysis runs. One sentence each, plus one sentence on why you
think so.

**(1) A movie you know well, and what its three most-used tags will be:** Inglorious Basterds, Dark-Comedy, Action, Gory

**(1) Why you think so:** Because it's a Quentin Tarantino film, who is known for his gory, over the top, dark comedies.

**(2) Out of every 100 people who rated movies here, how many ever added a tag?** 15

**(2) Why you think so:** Most people, similarly to ratings, are not going to go out of their way to tag or rate a movie after watching it.

**(3) Can one person's tags take over a movie's tag list? Yes or no:** Yes

**(3) Why you think so:** If there's one person who's super empowered to tag every movie they watch multiple times, then they'll have greater influence of the tagging overall.

## Part 1. Whose data is this?

Code: `part1_data.py`.

**My rule for cutting 32 million ratings to 5 million** (written before reading `data/make_compact.py`)**:** I think that I would just pick out movies where Thriller is one of the more common tags.

**One rule I considered and rejected, and why:** I rejected a rule of picking movies by a different genre as I felt like Thrillers would be roughly 10-15% of all movies.

**One interesting thing from `data/README.md`:** Just how much more flushed out the rule in data/README is compared to the rule I made. Really, based on my estimation in part 0, I should have just made my rule about whether people tagged a movie or not.

**How the script's rule differs from mine, and what each keeps that the other drops:** Its rule has far more filtering involved and is more of an algorithm whereas my rule maintains simplicity.

**First check. Which of Claude's numbers, the different route you took, and whether it matched** (one good target: 6 tags are the literal text `NA`, which pandas drops unless told not to)**:** The 15.6% share. Count the rows directly from the raw data file to ensure that nothing got dropped or duplicated. MATCH

**Second check. Which of Claude's numbers, the different route you took, and whether it matched:** The number of taggers. Keep the tag rows where a user also appears in ratings then count number of distinct users. MATCH

## Part 2. What tags best describe a movie?

Code: `part2_tags.py`.

**My movie, and why I picked it:** Inglourious Basterds (2009). Same movie because I like that movie.

**Its most misleading tag in the count-ordered list, and why it misleads:** I don't think any of the tags are misleading as they all accurately describe the film, but I'd say black comedy and dark comedy are redundant and could be combined into one tag.

**What I learned about how MovieLens collects ratings and tags, from rating and tagging my movie myself (about 100 words):** It's interesting that when you enter a tag in MovieLens, it removes the tag from view on your page presumably in an attempt to not have people repeating tags. With that being said, it would be extremely easy for one person to just repeat a tag over and over again and legitimately affect the dataset. The ratings, on the other hand, are far harder to influence if you're just one person, as the site locks you in at one rating per movie.

### Up close

One sentence on the figure written before you saw it and one after. The two tables are where the
details below come from. Say which script made them.

**The figure, when the tags and the ratings arrived. What I expected:** I expect the ratings and tags to go up sharply after release then plateau.
**The figure, what it shows:** There was a huge spike in 2021 of both ratings and tags.

**Two interesting details I learned up close that the counts did not show:** The 9.2% share of movies for user 78213 is surprising, and that dark comedy isn't in the top 3.

**Anything up close that contradicted something I had already written down. Which one, what the data showed, and what you now think. Or "nothing yet":** Nothing yet

### My definition

**My `score(movie, tag)`** (one or two sentences, precise enough that a classmate could code it)**:** Find tags where each user can only count once for a given tag and then take the highest occuring tag and take that as your best, then descend from there.

**One definition I considered and rejected, and why:** To me, this is the only way to determine the 'best' tag. The nature of the tags/ratings system is community-driven, so why turn away from the community when trying to find the best tags? What even constitutes 'best?'

**Which tags I merged as the same tag, which I kept apart, and why:** Strings with the same letters but different capitalization should count as the same strings, as well as tags with direct synonyms like black comedy and dark comedy. Also, if a string is part of a whole it should be extrapolated into the whole as the same string. If one string contains part of a name or other proper noun, it should be assumed that they're talking about the entire name or proper noun. Capitalized should be names. If you see a tag come up over and over that is part of a capitalized name but is listed as a separate string, that would need to be remedied. Rule 3 should ensure that specifically war should not go into world war II. "quinten tarantino" should always correct into Quentin Tarantino. Charles and charlie should be charlie, crime sprees and thrill crime can merge, song kang-ho is the correct name, author: yann martel is correct, cuban food and food truck can both be allowed if they are in the same movie. Crime can be its own category, thrill crime can go into crime sprees, food can stay on its own, irish can stay on its own. Disney can be on its own. I used the 66% test to cover a large portion of applications while mitigating the extremes. I started with my 3 rules and then went case by case for a collection of ties.

**Why my definition, in about 150 words. Name one thing it gains and one thing it loses:**

I chose this definition because I wanted to eliminate repetition of ideas in the tagging of these movies. I think one thing it gains is the hyper-specific filtering of certain tags that thwarted my umbrella rules for tags. This, however, is also its biggest downside because the odds are that I couldn't apply this set of rules to any dataset of films, and that it really only works well with this movie subset because I kind of brute forced the last handful of tag ties I had.

### The judge

The two slots below are read by scripts, so write them as bare lines: one item to a line, the
movieId first, no bullets and no numbering. A movie line looks like `296, Pulp Fiction (1994)`.
An order line looks like `296: nonlinear, hit men, dark comedy, ...`, the tags best first.

**My ten movies:**

79132, Inception (2010)
6936, Elf (2003)
58559, Dark Knight, The (2008)
1213, Goodfellas (1990)
2028, Saving Private Ryan (1998)
1704, Good Will Hunting (1997)
68157, Inglourious Basterds (2009)
55820, No Country for Old Men (2007)
109487, Interstellar (2014)
923, Citizen Kane (1941)

**My own order of the ten most-used tags, written before looking at any data: my movie from step 1, then my nine others from step 4:**

68157: Quentin Tarantino, dark comedy, World War II, alternate history, black comedy, satire, great acting, Brad Pitt, Christoph Waltz, visually appealing
79132: sci-fi, Leonardo DiCaprio, surreal, visually appealing
6936: Will Ferrell, comedy, Christmas, christmas, funny, cute, New York City, Zooey Deschanel, Peter Dinklage
58559: Batman, action, thriller, superhero, dark, Heath Ledger, Christian Bale, Christopher Nolan, Morgan Freeman, psychology
1213: crime, gangsters, mafia, organized crime, Robert De Niro, Martin Scorsese, gritty, good dialogue
2028: World War II, war, action, history, historical, horrors of war, Steven Spielberg, Tom Hanks, cinematography
1704: feel-good, inspirational, Robin Williams, Matt Damon, intelligent, mathematics, psychology, genius, excellent script, mentor
55820: serial killer, suspense, thriller, tension, atmospheric, Coen Brothers, Tommy Lee Jones, dark, twist ending, great acting
109487: sci-fi, time travel, relativity, visually appealing, physics, Christopher Nolan, artificial intelligence, good science, thought-provoking
923: melancholy, mystery, masterpiece, atmospheric, classic, Orson Welles, cinematography, Amazing Cinematography, black and white, Highly quotable

**One criterion I considered for the judge and rejected, and why** (the one I used is in `judge/criterion.md`)**:** I didn't really consider another criterion for the judge. To me, this is the best way to sort the tags.

**Agreement. The number `agreement.py` gives for your `score()`, for popularity and for your own order, and which of the three came closest to the judge:** 3.88, 3.87, and 4.40. So my own order was closest to the judge.

**How the judge skill is built: the files it is made of and what each one does (about 150 words):**

XXXX

**What happens when I run `/judge`, from the first check to the CSV (about 150 words):**

XXXX

**Why a skill: what a skill like this gives you that a script or a prompt alone does not, and where you would use one next (about 100 words):**

XXXX

### The viewer and the disagreements

**One thing `movie_results.html` showed me that was useful, and one thing about it that got in my way:** I think that the column showing the biggest discrepancy between my score() and the judges was really useful, but the huge tables of scores for tags kind of got in my way.

Then three improvements. For each: what the page would not let you see, what you had Claude
change, and what the changed page shows that the first draft did not.

**Improvement 1:** The page wouldn't let me easily see all the movies listed, I had you take out the long tables for readibility, and now the draft is much more digestible.

**Improvement 2:** Couldn't easily jump to a movie so I had claude add an index so that a viewer can easily navigate the html.

**Improvement 3:** I had claude add the judge criteria because I had no basis for how the judge was ranking these tags.

Then the three disagreements. A disagreement is a movie and a tag where your `score()` and the
judge are furthest apart. For each: the movie and the tag, where your `score()` put it and where
the judge put it, and what you think accounts for the gap.

**Disagreement 1:** The Dark Knight, Morgan Freeman. 9 and 45. Morgan Freeman is one of those actors that you can identify a movie from so I had him higher than the judge.

**Disagreement 2:** Goodfellas, Robert De Niro 3 vs 36, Same reasoning as Dark Knight and Morgan Freeman. De Niro is a guy that could identify a movie for some people.

**Disagreement 3:** Inglorious Basterds, Quentin Tarantino, 1 and 46. Similar reasoning, the most defining characteristic of Tarantino's films are that he directed them.

**One other high-level pattern in the results, and what you think is behind it:** A strange pattern is that the judge's lists are largely alphabetical, but I'm not sure whats behind it. There were so many ties that some lists ended up differing to mainly alphabetical.

## Predictions revisited

**Which of my three predictions were wrong, and what I make of each miss:** XXXX

## Part 3. What tags best describe a user?

Code: `part3_users.py`.

The slot below is read by a script, so write it as bare lines: one rating to a line, no bullets
and no numbering, the movieId first and the rating last, as in `296, Pulp Fiction (1994), 4.5`.

**My 20 ratings:**

XXXX

**My `score(user, tag)`, in a sentence, and why I started there (about 100 words):**

XXXX

**What my score says about me: my top ten tags, and whether they describe my taste (about 100 words):**

XXXX

**What my user viewer shows and why I chose that (about 100 words):**

XXXX

**What I put in the description column for a person, and why (about 150 words):**

XXXX

**My criterion for people: what it asks the judge to do that the movie criterion did not (about 60 words):**

XXXX

**The user-tag pairs I chose to judge, how many, and why those (about 100 words):**

XXXX

**Improvement 1: what I changed in the scoring function, what the judge and the viewer showed before and after (about 150 words):**

XXXX

**Improvement 2: the same (about 150 words):**

XXXX

## Part 4. Working with Claude

Give these to Claude the way you gave it the rest. Graded on the catch and the candor, not on
making Claude look good or bad.

**A moment where Claude was wrong or overconfident, how you caught it, and where it
happened. Name the part and the step, so the moment can be found:** XXXX

**One call where you overrode Claude, and why:** XXXX

**What you would hand to Claude sooner next time:** XXXX

**Did Claude name the misleading tag in Part 2 step 1 before you did? What happened:** XXXX

**The figure. Would asking Claude "what does this show?" have produced your sentence, and what
would have been missing from it:** XXXX

**Hours spent:** XXXX

**Anyone who helped you, or "no one":** XXXX
