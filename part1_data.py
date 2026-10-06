"""
Part 1: whose data is this?

    uv run python part1_data.py

Write your own cut rule and your two checks before you run anything here. Doing it in that
order is what Part 1 is asking for. What this script must print, under the labels shown:

    == (a) how much ==
        Rows in each of the four files, distinct users, distinct movies, and the share of
        all 32,000,204 MovieLens ratings this set holds.

    == (b) spread ==
        Ratings per user and ratings per movie: median, minimum and maximum of each. Tag
        applications per user and per movie: the same three. How many of the users who
        rated anything ever applied a tag, as a count and as a share.

    == (c) top tags, two ways ==
        The 20 most-used tags by number of applications, and the 20 most-used tags by number
        of distinct users who applied them. Print the two lists one after the other, with
        both numbers on every row, so you can see where a tag's two ranks differ.

    == (d) two checks ==
        Two claims from (a) to (c) re-derived by a route that does not reuse the code that
        produced them, printed with both numbers side by side and the word MATCH or DIFFER.
        Targets that exist in this data: the share of all 32M ratings the set holds
        (`data/README.md` says 15.6 percent); the number of distinct users who applied a
        tag (14,019); the rating count of the least-rated kept movie (83); the 6 tag
        rows whose text is literally `NA`, which vanish if a reader is built without
        `keep_default_na=False`.

No figures are required in Part 1. `WRITEUP.md` takes one interesting thing from
`data/README.md`, your own cut rule and the rule you rejected, how `data/make_compact.py`'s
rule differs from yours, and your two checks.
"""

import gzip

from load_data import DATA, load_all

ALL_RATINGS = 32_000_204   # every rating in MovieLens 32M


def three(s):
    """Median, minimum and maximum of a Series, as one line."""
    return f"median {s.median():,.0f}, min {s.min():,}, max {s.max():,}"


def part1_data(ratings, tags, movies, links):
    print("== (a) how much ==")
    print(f"ratings.csv.gz  {len(ratings):>10,} rows")
    print(f"tags.csv.gz     {len(tags):>10,} rows")
    print(f"movies.csv      {len(movies):>10,} rows")
    print(f"links.csv       {len(links):>10,} rows")
    print(f"distinct users (ratings)   {ratings['userId'].nunique():,}")
    print(f"distinct movies (ratings)  {ratings['movieId'].nunique():,}")
    print(f"share of all {ALL_RATINGS:,} MovieLens ratings: {len(ratings) / ALL_RATINGS:.1%}")

    print("== (b) spread ==")
    print("ratings per user:          ", three(ratings.groupby("userId").size()))
    print("ratings per movie:         ", three(ratings.groupby("movieId").size()))
    print("tag applications per user: ", three(tags.groupby("userId").size()))
    print("tag applications per movie:", three(tags.groupby("movieId").size()))
    raters = set(ratings["userId"].unique())
    taggers = raters & set(tags["userId"].unique())
    print(f"users who rated anything and ever applied a tag: "
          f"{len(taggers):,} of {len(raters):,} ({len(taggers) / len(raters):.1%})")

    print("== (c) top tags, two ways ==")
    # Raw tag strings, exactly as people typed them: "Cult classic" and "cult classic" are two rows.
    by_tag = tags.groupby("tag").agg(applications=("userId", "size"), users=("userId", "nunique"))
    for col in ["applications", "users"]:
        print(f"-- top 20 by {col} --")
        print(by_tag.sort_values(col, ascending=False).head(20).to_string())

    print("== (d) two checks ==")
    # Check 1: the share, from the raw file's lines rather than the loaded frame.
    with gzip.open(DATA / "ratings.csv.gz", "rt") as f:
        raw_rows = sum(1 for _ in f) - 1   # minus the header line
    claimed, checked = len(ratings) / ALL_RATINGS, raw_rows / ALL_RATINGS
    print(f"share of 32M ratings: (a) {claimed:.4%}  raw file lines {checked:.4%}  "
          f"{'MATCH' if raw_rows == len(ratings) else 'DIFFER'}")
    # Check 2: taggers, by filtering tag rows to users who rated, then counting distinct users.
    rated_tag_rows = tags[tags["userId"].isin(ratings["userId"])]
    n_check = rated_tag_rows["userId"].nunique()
    print(f"users who rated and tagged: (b) {len(taggers):,}  filtered tag rows {n_check:,}  "
          f"{'MATCH' if n_check == len(taggers) else 'DIFFER'}")


if __name__ == "__main__":
    ratings, tags, movies, links = load_all()
    part1_data(ratings, tags, movies, links)
