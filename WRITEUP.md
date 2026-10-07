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

README is a guide to the judge; system.md is the fixed system prompt that tells Claude to apply criteria, criterion.md is my definition of what best describes a movie, judge.py is the loop that runs the judge itself, movies.csv is the 100 movies that the judge rates, and vocabulary.txt is the list of tags.

**What happens when I run `/judge`, from the first check to the CSV (about 150 words):**

The judge sends each movie to its own isolated Claude session with a fixed system prompt plus my criterion as a user prompt, and the movie's title/year/genre as well as its vocabulary tags in alphabetical order without counts. It goes through and asks for a 1-5 rating for each tag then goes back through and re asks if any scores are missing.

**Why a skill: what a skill like this gives you that a script or a prompt alone does not, and where you would use one next (about 100 words):**

A prompt or script are instructions with no memory whereas a skill can repeat tasks with minor differences or with some variation. I would use a skill to send out networking emails because they're all more or less the same with some slight variation.

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

**Which of my three predictions were wrong, and what I make of each miss:** The top three tags and my 15/100 taggers per raters were wrong. I just didn't have a real frame of reference for these predictions.

## Part 3. What tags best describe a user?

Code: `part3_users.py`.

The slot below is read by a script, so write it as bare lines: one rating to a line, no bullets
and no numbering, the movieId first and the rating last, as in `296, Pulp Fiction (1994), 4.5`.

**My 20 ratings:**

58559, Dark Knight, The (2008), 5.0
1213, Goodfellas (1990), 4.5
79132, Inception (2010), 4.5
68157, Inglourious Basterds (2009), 4.5
2028, Saving Private Ryan (1998), 4.0
1704, Good Will Hunting (1997), 4.0
55820, No Country for Old Men (2007), 4.0
109487, Interstellar (2014), 4.0
923, Citizen Kane (1941), 4.0
6650, Kind Hearts and Coronets (1949), 3.5
187717, Won't You Be My Neighbor? (2018), 3.5
6936, Elf (2003), 3.5
176, Living in Oblivion (1995), 3.0
4329, Rio Bravo (1959), 3.0
5027, Another 48 Hrs. (1990), 2.5
2034, Black Hole, The (1979), 2.0
4167, 15 Minutes (2001), 2.0
2163, Attack of the Killer Tomatoes! (1978), 1.5
1981, Friday the 13th Part VIII: Jason Takes Manhattan (1989), 1.0
427, Boxing Helena (1993), 0.5

**My `score(user, tag)`, in a sentence, and why I started there (about 100 words):**

Score takes the top 20 tags from a user's favorite movies (3.5 rating or higher) and ranks them by prevalence in those movies. I started there because it made the most sense to me that tags prevalent in people's favorite movies would be their highest rated tags. My personal score(user, tag) is pretty accurate with what I would say for myself (with some exceptions) so I feel good about my starting point.

**What my score says about me: my top ten tags, and whether they describe my taste (about 100 words):**

| tag | score |
| --- | --- |
| thought-provoking | 654 |
| visually appealing | 551 |
| director: christopher nolan | 484 |
| sci-fi | 433 |
| alternate reality | 359 |
| great acting | 309 |
| space | 297 |
| mindfuck movie | 289 |
| twist ending | 287 |
| action | 281 |

My top ten tags generally do describe my taste: I love Chris Nolan movies and thrillers and sci-fi, and movies that make you think. There isn't a tag I would necessarily replace and I'd call this a good representation of the types of movies I like to watch. I think it leaves out my love for comedy films but I also didn't really indicate that love in my list of movies.

**What my user viewer shows and why I chose that (about 100 words):**

My viewer just shows my personal top 30 tags and top 9 movies, as well as one movie that it thinks I would like based off what I have rated and what tags are most relevant to that movie. I chose this to keep it fairly focused and conserve tokens (didn't want to view the whole user dataset), and I added the recommender as a piece of utility.

**What I put in the description column for a person, and why (about 150 words):**

I think that a recommended movie really grabs people's attention, and if the tie is between 5 movies that the algorithm thinks they will like, it shouldn't matter which of those gets recommended.

**My criterion for people: what it asks the judge to do that the movie criterion did not (about 60 words):**

My movie criterion was more concerned with semantics and the spelling of the tags themselves while the people criterion is based on preference and opinion.

**The user-tag pairs I chose to judge, how many, and why those (about 100 words):**

I chose these 110 people because I wanted a somewhat representative amount without using $200 of tokens and 9 hours of time.

**Improvement 1: what I changed in the scoring function, what the judge and the viewer showed before and after (about 150 words):**

I chose not to change it because I see only one issue with my score(user, tag) that I would want to fix, and I have no idea how to fix it. I also am not convinced that it's an error with the score rules themselves or simply a personal disagreement on one specific tag. Not trying at all to get out of filling out those sections of part 3, I just genuinely can't think of a way to improve my score at this time.

**Improvement 2: the same (about 150 words):**

See Improvement 1.

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
