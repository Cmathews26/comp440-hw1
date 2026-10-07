"""
Part 2: what tags best describe a movie?

    uv run python part2_tags.py

Steps 1 to 4 of the handout's Part 2 live here, plus the scores and the rankings that steps 5
and 6 need. The judge itself runs through `/judge`, and its answer is read through
`agreement.py` and `results_viewer.py`. What this script must print, under the labels shown,
and what it must write:

    == (1) the obvious answer ==
        Your chosen movie's title, its rating count and its tag-application count, then
        every tag applied to it with how many times it was applied, most-applied first.
        Pick a movie with at least 500 ratings and 30 tag applications. The most misleading
        entry in that list is your sentence in `WRITEUP.md`, not this script's.

    == (2) up close ==
        The numbers behind the one required figure and the two tables, so that everything
        shown here has printed output a reader can check it against. Write, to `figures/`:

            figures/part2_when.png          when the tags arrived: tag applications over
                                            time, with the movie's ratings over time behind
                                            them.

        The figure has labeled axes and a caption naming the question it answers. Claude
        may draw and label it; the sentence in `WRITEUP.md` about what it shows is yours.

        Then two tables, each printed under its own label:

            who added each tag              the movie's heaviest taggers, how many tag
                                            applications each made, and what share of the
                                            movie's applications that is.
            how the taggers rated it        for each of the movie's top tags, how the
                                            people who applied it rated the movie, beside
                                            how everyone else rated it.

        Claude prints the tables and says what the columns are. What they show is your two
        interesting details in `WRITEUP.md`, not this script's.

    == (3) my definition ==
        Your `score` over the whole set. Write it in this file as

            score(tags_df, ratings_df, movies_df) -> DataFrame[movieId, tag, score]

        one row per movie-tag pair, higher score meaning the tag describes the movie better.
        Print its top 15 rows for your chosen movie, and the number of rows and distinct
        movies it returned over the whole set. Families you could use, none of them
        preferred: distinct users who applied the tag; a rarity weight, the count times how
        few movies carry the tag; a damped version of either; something of your own. Whatever
        you choose, `WRITEUP.md` gets what you chose, what you rejected, and why.

    == (4) cleaning ==
        Whatever cleaning your `score()` does, and its size: how many raw tag strings went
        in, how many distinct tags came out, and the five mergers that absorbed the most
        applications. If you clean nothing, print that and say why in `WRITEUP.md`.
        Merging `Sci-Fi`, `sci-fi` and `scifi` is a decision, and so is not merging them.

    == (5) scores.csv ==
        `scores.csv` in the repo root, columns `movieId,tag,score`, holding a score for every
        movie and tag the judge will be asked about. That is two sets put together:

            every movie and tag in `judge/movies.csv`, which has one row per movie and a
            `tags` column of tags joined by `|`;
            plus, for each of the ten movies in your "My ten movies" slot, every tag from
            `judge/vocabulary.txt` that appears on it, matched after stripping and
            lowercasing, which is the same rule `judge/movies.csv` used.

        The second set matters because the judge adds your ten movies to its list, and
        `agreement.py` compares exactly what the two files share: a tag you never scored is
        dropped without a number. Print how many were asked for and how many you wrote.

    == (6) the four rankings ==
        For each of the ten movies in your "My ten movies" slot, four rankings of the same tags,
        printed one after another and never in one table:

            the counts: the ten most-used tags, by how many times each was applied;
            your own order, from the `WRITEUP.md` slot you filled before seeing any data;
            the judge's order, from `judge/ratings_movies.csv`;
            your `score()`'s order.

        Print each list under its own heading, best first. `results_viewer.py` builds the same
        four lists as a page you can read. Which tag is the artifact, and what the
        disagreements mean, is your paragraph in `WRITEUP.md`.
"""

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from agreement import my_order_lines
from load_data import load_all

MY_MOVIE = 68157   # Inglourious Basterds (2009)
REPO = Path(__file__).resolve().parent
FIGURES = REPO / "figures"


def plot_when(when, title):
    """figures/part2_when.png: two panels on one time axis, so neither count is rescaled."""
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    x = when.index.to_timestamp()
    for ax, col, color in [(top, "ratings", "#2a78d6"), (bottom, "tag applications", "#eb6834")]:
        ax.plot(x, when[col], color=color, linewidth=1.5)
        ax.set_ylabel(f"{col} per month")
        ax.grid(axis="y", color="#e5e5e2", linewidth=0.8)
        ax.spines[["top", "right"]].set_visible(False)
    bottom.set_xlabel("month")
    fig.suptitle(f"{title}: when did the ratings and the tags arrive?")
    fig.text(0.5, 0.005, "Ratings (top) and tag applications (bottom) per calendar month, "
             "from ratings.csv.gz and tags.csv.gz. Each panel has its own y-axis.",
             ha="center", fontsize=8, color="#52514e")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(FIGURES / "part2_when.png", dpi=150)
    plt.close(fig)


# The student's cleaning rule, from WRITEUP.md "Which tags I merged":
#   1. tags that differ only in capitalization are one tag (lowercased; nothing else is trimmed);
#   2. a tag of two or more words is a name when, across all movies, at least NAME_CUTOFF of
#      its applications were typed with every word starting with a capital letter;
#   3. on the same movie, a tag whose words are a run of words inside a name merges into
#      that name; if it fits inside several, the longest name wins;
#   4. direct synonyms are merged by the list below (applied right after rule 1, so rules 2
#      and 3 see the corrected tag);
#   5. pairs the student kept apart are never merged by rule 3.
SYNONYMS = {"black comedy": "dark comedy", "quinten tarantino": "quentin tarantino",
            "charles chaplin": "charlie chaplin", "kang-ho song": "song kang-ho",
            "writer: yann martel": "author: yann martel", "thrill crime": "crime sprees"}   # the student's list: lowercased tag -> the tag it merges into


NAME_CUTOFF = 0.66   # the student's cutoff for rule 2
KEPT_APART = {("war", "world war ii"), ("crime", "crime sprees"), ("food", "cuban food"),
              ("food", "food truck"), ("irish", "irish catholics"), ("irish", "irish americans"),
              ("disney", "disney classics"), ("disney", "bearable disney")}   # the student's list: (short tag, name) rule 3 must not merge


def all_caps_words(raw):
    words = raw.split()
    return len(words) >= 2 and all(w[0].isupper() for w in words)


def inside(short, name):
    """True if `short`'s words are a contiguous run of `name`'s words, and short is not name."""
    s, n = short.split(), name.split()
    return 0 < len(s) < len(n) and any(n[i:i + len(s)] == s for i in range(len(n) - len(s) + 1))


def clean(tags_df):
    """tags_df plus a `clean` column holding the tag each row counts as."""
    t = tags_df.copy()
    t["clean"] = t["tag"].str.lower()                                       # rule 1
    t["clean"] = t["clean"].replace(SYNONYMS)                               # rule 4
    multi = t[t["clean"].str.split().str.len() >= 2]                       # rule 2
    share = multi["tag"].map(all_caps_words).groupby(multi["clean"]).mean()
    name_set = set(share[share >= NAME_CUTOFF].index)
    names = t.loc[t["clean"].isin(name_set), ["movieId", "clean"]].drop_duplicates()
    names_by_movie = names.groupby("movieId")["clean"].apply(list)
    pairs = t.loc[t["movieId"].isin(names_by_movie.index), ["movieId", "clean"]].drop_duplicates()
    merge = {}                                                              # rule 3
    for movie, short in pairs.itertuples(index=False):   # a loop over movie-tag pairs, not ratings
        fits = [n for n in names_by_movie[movie] if inside(short, n) and (short, n) not in KEPT_APART]
        if fits:
            longest = max(len(n) for n in fits)
            merge[(movie, short)] = [n for n in fits if len(n) == longest]
    ties = {k: v for k, v in merge.items() if len(v) > 1}
    key = pd.Series(list(zip(t["movieId"], t["clean"])), index=t.index)
    t["clean"] = key.map(lambda k: merge[k][0] if k in merge else k[1])
    return t, ties


def score(tags_df, ratings_df, movies_df):
    """The student's score: distinct users who applied the (cleaned) tag to the movie."""
    t, _ = clean(tags_df)
    out = t.groupby(["movieId", "clean"])["userId"].nunique().rename("score").reset_index()
    return out.rename(columns={"clean": "tag"})


def judge_pairs(tags_df):
    """Every movie and tag the judge is asked about: judge/movies.csv, plus the vocabulary tags
    on each movie in the "My ten movies" slot, matched after stripping and lowercasing."""
    shipped = pd.read_csv(REPO / "judge" / "movies.csv", keep_default_na=False)
    pairs = shipped.assign(tag=shipped["tags"].str.split("|")).explode("tag")
    pairs = pairs.rename(columns={"id": "movieId"})[["movieId", "tag"]]
    slot = (REPO / "WRITEUP.md").read_text(encoding="utf-8").split("**My ten movies")[-1]
    mine = [int(n) for n in re.findall(r"^\s*(\d+)", slot.split("\n**")[0], re.M)]
    words = {w.strip() for w in (REPO / "judge" / "vocabulary.txt").read_text().splitlines()}
    on_mine = (tags_df.assign(tag=tags_df["tag"].str.strip().str.lower())
               .query("movieId in @mine and tag in @words")[["movieId", "tag"]])
    return pd.concat([pairs, on_mine]).drop_duplicates().reset_index(drop=True)


def part2_tags(ratings, tags, movies, links):
    print("== (1) the obvious answer ==")
    title = movies.set_index("movieId").loc[MY_MOVIE, "title"]
    my_tags = tags[tags["movieId"] == MY_MOVIE]
    print(f"{title}: {(ratings['movieId'] == MY_MOVIE).sum():,} ratings, "
          f"{len(my_tags):,} tag applications")
    # Raw tag strings, exactly as people typed them: "Cult classic" and "cult classic" are two rows.
    with pd.option_context("display.max_rows", None):
        print(my_tags["tag"].value_counts().rename("applications").to_string())

    print("== (2) up close ==")
    my_ratings = ratings[ratings["movieId"] == MY_MOVIE]
    when = pd.DataFrame({
        "ratings": pd.to_datetime(my_ratings["timestamp"], unit="s").dt.to_period("M").value_counts(),
        "tag applications": pd.to_datetime(my_tags["timestamp"], unit="s").dt.to_period("M").value_counts(),
    }).fillna(0).astype(int).sort_index()
    when = when.reindex(pd.period_range(when.index.min(), when.index.max(), freq="M"), fill_value=0)
    print("per month, first and last month:", when.index.min(), when.index.max())
    print("per year:")
    print(when.groupby(when.index.year).sum().to_string())
    plot_when(when, title)

    # Raw tag strings throughout: no merging has been decided yet.
    print("-- who added each tag --")
    who = my_tags.groupby("userId").size().sort_values(ascending=False).rename("applications").to_frame()
    who["share of movie"] = (who["applications"] / len(my_tags)).map("{:.1%}".format)
    who["distinct tags"] = my_tags.groupby("userId")["tag"].nunique()
    print(f"{len(who):,} distinct taggers; the 15 heaviest:")
    print(who.head(15).to_string())

    print("-- how the taggers rated it --")
    stars = my_ratings.set_index("userId")["rating"]
    rows = []
    for tag in my_tags["tag"].value_counts().head(10).index:
        users = set(my_tags.loc[my_tags["tag"] == tag, "userId"])
        mine, rest = stars[stars.index.isin(users)], stars[~stars.index.isin(users)]
        rows.append({"tag": tag, "taggers": len(users), "taggers who rated": len(mine),
                     "their mean": round(mine.mean(), 2), "everyone else n": len(rest),
                     "everyone else mean": round(rest.mean(), 2)})
    print(pd.DataFrame(rows).set_index("tag").to_string())

    print("== (3) my definition ==")
    scores = score(tags, ratings, movies)
    print(f"{title}, top 15 by score:")
    print(scores[scores["movieId"] == MY_MOVIE].sort_values("score", ascending=False)
          .head(15).to_string(index=False))
    print(f"over the whole set: {len(scores):,} rows, {scores['movieId'].nunique():,} distinct movies")

    print("== (4) cleaning ==")
    cleaned, ties = clean(tags)
    print(f"raw tag strings in: {tags['tag'].nunique():,}   distinct tags out: {cleaned['clean'].nunique():,}")
    print(f"synonym pairs applied: {len(SYNONYMS)}")
    print(f"movie-tag pairs that fit inside two or more equally long names: {len(ties):,}")
    # Absorbed = a cleaned tag's applications minus those of its most-used raw string.
    per_raw = cleaned.groupby(["clean", "tag"]).size()
    groups = per_raw.groupby(level="clean")
    absorbed = (groups.sum() - groups.max()).sort_values(ascending=False)
    print("the five mergers that absorbed the most applications:")
    for tag in absorbed.head(5).index:
        parts = per_raw[tag].sort_values(ascending=False)
        print(f"  {tag!r}: absorbed {absorbed[tag]:,} of {parts.sum():,} applications from "
              f"{len(parts)} raw strings, e.g. " + ", ".join(f"{s!r} {n}" for s, n in parts.head(6).items()))

    print("== (5) scores.csv ==")
    asked = judge_pairs(tags)
    # Each asked tag is a stripped, lowercased vocabulary string. It takes the score of the
    # cleaned tag its raw strings became on that movie, so "black comedy" scores as "dark comedy".
    # If its raw strings landed in more than one cleaned tag, the highest score is kept.
    c = cleaned.assign(key=cleaned["tag"].str.strip().str.lower())
    c = c.merge(asked, left_on=["movieId", "key"], right_on=["movieId", "tag"], suffixes=("_raw", ""))
    c = c[["movieId", "tag", "clean"]].drop_duplicates()
    c = c.merge(scores.rename(columns={"tag": "clean"}), on=["movieId", "clean"])
    out = c.groupby(["movieId", "tag"])["score"].max().reset_index()
    out.to_csv(REPO / "scores.csv", index=False)
    print(f"movie-tag pairs asked for: {len(asked):,}   written to scores.csv: {len(out):,}")

    print("== (6) the four rankings ==")
    slot = (REPO / "WRITEUP.md").read_text(encoding="utf-8").split("**My ten movies")[-1]
    mine = [int(n) for n in re.findall(r"^\s*(\d+)", slot.split("\n**")[0], re.M)]
    orders = my_order_lines()
    judged = pd.read_csv(REPO / "judge" / "ratings_movies.csv", keep_default_na=False)
    titles = movies.set_index("movieId")["title"]
    for movie in mine:
        print(f"\n#### {titles[movie]} ({movie})")
        counts = tags.loc[tags["movieId"] == movie, "tag"].value_counts().head(10)
        j = judged[judged["id"] == movie].sort_values(["rating", "tag"], ascending=[False, True])
        sc = out[out["movieId"] == movie].sort_values(["score", "tag"], ascending=[False, True])
        lists = [
            ("the counts (raw strings, ten most-used)", [f"{t} ({n})" for t, n in counts.items()]),
            ("my own order", orders.get(movie, ["(no line in the slot)"])),
            ("the judge's order (ties alphabetical)", [f"{t} ({r})" for t, r in zip(j["tag"], j["rating"])]),
            ("my score() order (ties alphabetical)", [f"{t} ({v})" for t, v in zip(sc["tag"], sc["score"])]),
        ]
        for heading, items in lists:
            print(f"-- {heading} --")
            for place, item in enumerate(items, 1):
                print(f"  {place:>2}. {item}")


if __name__ == "__main__":
    ratings, tags, movies, links = load_all()
    part2_tags(ratings, tags, movies, links)
