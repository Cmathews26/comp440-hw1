"""
Part 3: what tags best describe a user?

    uv run python part3_users.py

The handout's Part 3 is the spec. One piece is written for you, the piece that has to agree
with `WRITEUP.md` line for line: reading the 20 ratings out of your "My 20 ratings" slot and
adding you to the ratings table as a user of your own. Everything after that is yours.

You are added under userId 999999. Real userIds in `data/ratings.csv.gz` stop at 200,935, so
that number cannot be a real person's, and it is easy to pick out of a printout.

What this script must print, under the labels shown:

    == (1) my ratings ==
        How many ratings were read out of your slot, how many lines it could not read a
        rating from, and how many rows the ratings table has with yours in it. Twenty
        ratings is what the handout asks for; the script reports what it found and leaves
        the count to you.

    == (2) score(user, tag) ==
        Your `score(user, tag)` over the users you are looking at, your own row included.
        Write it in this file as

            score(ratings_df, tags_df, movies_df) -> DataFrame[userId, tag, score]

        one row per user-tag pair, higher score meaning the tag describes the user better.
        Print your own ten best tags, and the number of rows and distinct users it returned.
        What the score is, and why you started there, is yours and goes in `WRITEUP.md`.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from load_data import load_all

REPO = Path(__file__).resolve().parent
WRITEUP = REPO / "WRITEUP.md"

ME = 999999                 # your userId: above every real one, so it collides with nobody
SLOT = "My 20 ratings"      # the WRITEUP.md slot your ratings are read from


def read_my_ratings(writeup: Path = WRITEUP) -> tuple[pd.DataFrame, int]:
    """Your ratings from the "My 20 ratings" slot in WRITEUP.md, as movieId and rating.

    The same rule the judge uses for "My ten movies": every line in that slot starts with a
    movieId. The rating is the last number on the line, so the title between them is for
    people and may hold anything, the year included. Bare lines only: a bulleted or a
    numbered list reads as no ratings at all, or reads the list numbers as movieIds.

        296, Pulp Fiction (1994), 4.5

    A line whose last number is not a rating between 0.5 and 5.0 is left out and counted,
    because the year in a title is a number too: `296, Pulp Fiction (1994)` with the rating
    forgotten would otherwise be read as a rating of 1994. So is the `XXXX` an unfilled slot
    holds, which is why this is safe to run before you have written anything.

    Returns the ratings and how many lines were left out."""
    rows, skipped, inside = [], 0, False
    for line in writeup.read_text(encoding="utf-8").splitlines():
        if line.startswith("**"):            # a bold label opens the next slot
            inside = SLOT in line
            continue
        if not inside or not re.match(r"\s*\d", line):
            continue
        numbers = re.findall(r"\d+(?:\.\d+)?", line)
        rating = float(numbers[-1]) if len(numbers) > 1 else 0.0
        if not 0.5 <= rating <= 5.0:
            skipped += 1
            continue
        rows.append({"movieId": int(numbers[0].split(".")[0]), "rating": rating})
    return pd.DataFrame(rows, columns=["movieId", "rating"]), skipped


def add_me(ratings: pd.DataFrame, mine: pd.DataFrame) -> pd.DataFrame:
    """Your ratings appended to everybody else's, under userId ME.

    The timestamp is the newest one in the data: you rated these after everyone else did."""
    if mine.empty:
        return ratings
    mine = mine.assign(userId=ME, timestamp=int(ratings["timestamp"].max()))
    return pd.concat([ratings, mine[ratings.columns]], ignore_index=True)


# ------------------------------------------------------------------- yours to write ---

# The student's rule, from this session:
#   a movie counts for a person when they rated it at least LIKED;
#   each counted movie contributes its TOP_N best tags by the Part 2 score() (cleaned tags,
#   distinct users), and when tags tie across the TOP_N-th place, the whole tie is dropped;
#   score(user, tag) is the sum of that tag's Part 2 scores over the person's counted movies.
LIKED = 3.5
TOP_N = 20
USERS = None   # the student's call: every user, their own row included


def movie_top_tags(tags: pd.DataFrame, ratings: pd.DataFrame, movies: pd.DataFrame) -> pd.DataFrame:
    """movieId, tag, score: each movie's TOP_N best tags by the Part 2 score(). A tie that
    crosses the TOP_N-th place is dropped whole, so a movie can keep fewer than TOP_N."""
    from part2_tags import score as movie_score
    m = movie_score(tags, ratings, movies)
    # rank "max": a tag's rank is the last place its tie group reaches.
    last_place = m.groupby("movieId")["score"].rank(method="max", ascending=False)
    return m[last_place <= TOP_N]


def score(ratings: pd.DataFrame, tags: pd.DataFrame, movies: pd.DataFrame):
    """What tags best describe a user: the student's rule above.

    Returns one row per user-tag pair: userId, tag, score."""
    liked = ratings[ratings["rating"] >= LIKED]
    if USERS is not None:
        liked = liked[liked["userId"].isin(USERS)]
    top = movie_top_tags(tags, ratings, movies)
    # Users in chunks, so the user-movie-tag join never sits in memory all at once.
    users = liked["userId"].unique()
    parts = []
    for start in range(0, len(users), 2000):
        chunk = liked[liked["userId"].isin(users[start:start + 2000])]
        pairs = chunk[["userId", "movieId"]].merge(top, on="movieId")
        parts.append(pairs.groupby(["userId", "tag"])["score"].sum().reset_index())
    return pd.concat(parts, ignore_index=True)


# judge/users.csv, by the student's rules:
#   people: 109 drawn at random (seed JUDGE_SEED) from users with at least one movie rated
#   LIKED or higher, plus me;
#   description: the person's recommended movie, by the user viewer's rule (their top
#   RECOMMEND_FROM tags against the top TOP_N tags of each movie they have not rated, most
#   matches wins), its title as movies.csv writes it; a tie is broken by a seeded random pick;
#   tags: the person's top JUDGE_TAGS tags by score(user, tag).
JUDGE_SEED = 440
JUDGE_PEOPLE = 109
RECOMMEND_FROM = 30
JUDGE_TAGS = 5


def write_users_csv(ratings, tags, movies):
    import numpy as np
    global USERS
    pool = np.sort(ratings.loc[(ratings["rating"] >= LIKED) & (ratings["userId"] != ME), "userId"].unique())
    picked = list(pd.Series(pool).sample(JUDGE_PEOPLE, random_state=JUDGE_SEED)) + [ME]
    USERS = picked
    s = score(ratings, tags, movies).sort_values(["userId", "score", "tag"], ascending=[True, False, True])
    USERS = None
    top = s.groupby("userId").head(RECOMMEND_FROM)
    movie_tags = movie_top_tags(tags, ratings, movies)
    seen = ratings.loc[ratings["userId"].isin(picked), ["userId", "movieId"]].assign(seen=1)
    x = top[["userId", "tag"]].merge(movie_tags[["movieId", "tag"]], on="tag")
    x = x.merge(seen, on=["userId", "movieId"], how="left")
    c = x[x["seen"].isna()].groupby(["userId", "movieId"]).size().rename("n").reset_index()
    leaders = c[c["n"] == c.groupby("userId")["n"].transform("max")].sort_values(["userId", "movieId"])
    rng = np.random.default_rng(JUDGE_SEED)
    pick = leaders.groupby("userId")["movieId"].apply(lambda ids: ids.iloc[rng.integers(len(ids))])
    titles = movies.set_index("movieId")["title"]
    tied = int((leaders.groupby("userId").size() > 1).sum())
    rows = [{"id": u, "description": titles[pick[u]],
             "tags": "|".join(s.loc[s["userId"] == u, "tag"].head(JUDGE_TAGS))} for u in picked]
    out = pd.DataFrame(rows)
    out.to_csv(REPO / "judge" / "users.csv", index=False)
    print(f"wrote judge/users.csv: {len(out)} people, {out['tags'].str.count('[|]').add(1).sum()} tags "
          f"to rate; {tied} recommendations broken from a tie")


def part3_users(ratings, tags, movies, links):
    print("== (1) my ratings ==")
    mine, skipped = read_my_ratings()
    print(f'{len(mine)} rating(s) read from the "{SLOT}" slot in WRITEUP.md.')
    if not len(mine):
        print(f'Nothing was read out of the "{SLOT}" slot. It is read one rating to a line, '
              f"with no bullets and no numbering: the movieId first, then the title, then "
              f"your rating, as in `296, Pulp Fiction (1994), 4.5`.")
    if skipped:
        print(f"{skipped} line(s) in that slot had no rating between 0.5 and 5.0 at the "
              f"end and were left out.")
    ratings = add_me(ratings, mine)
    if len(mine):
        print(f"{len(ratings):,} ratings with yours in, as userId {ME}.")
    else:
        print(f"{len(ratings):,} ratings, none of them yours yet.")

    print("== (2) score(user, tag) ==")
    scores = score(ratings, tags, movies)
    me = scores[scores["userId"] == ME].sort_values(["score", "tag"], ascending=[False, True])
    print(f"my ten best tags (userId {ME}):")
    print(me.head(10).to_string(index=False))
    print(f"over every user: {len(scores):,} rows, {scores['userId'].nunique():,} distinct users")

    print("== (3) judge/users.csv ==")
    write_users_csv(ratings, tags, movies)


if __name__ == "__main__":
    ratings, tags, movies, links = load_all()
    part3_users(ratings, tags, movies, links)
