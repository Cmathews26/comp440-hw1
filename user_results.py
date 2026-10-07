"""User viewer: what my score(user, tag) says about me, as one page.

    uv run python user_results.py            # writes user_results.html
    uv run python user_results.py --text     # the same content as plain text

What the page shows is the student's design:
  * my top TOP_TAGS tags by my score(user, tag) from part3_users.py;
  * my top movies: every movie I rated at least TOP_MOVIES_FROM, best first;
  * one recommended movie: among movies I have not rated, the one whose top 20 tags (the
    same cut my score uses) hold the most of my top TOP_TAGS tags;
  * below my scores and kept separate from them, the judge's ratings of my tags, from
    judge/ratings_users.csv, in the judge's own order (rating, then alphabetical).
"""

import argparse
import html
from pathlib import Path

import pandas as pd

import part3_users
from load_data import load_all
from part3_users import ME, add_me, movie_top_tags, read_my_ratings, score

REPO = Path(__file__).resolve().parent
TOP_TAGS = 30          # the student's choice
TOP_MOVIES_FROM = 4.0  # the student's choice: every movie rated this or higher


def build():
    ratings, tags, movies, _ = load_all()
    mine, _ = read_my_ratings()
    ratings = add_me(ratings, mine)
    titles = movies.set_index("movieId")["title"]

    part3_users.USERS = [ME]
    me = score(ratings, tags, movies).sort_values(["score", "tag"], ascending=[False, True])
    top = me.head(TOP_TAGS)

    best = mine[mine["rating"] >= TOP_MOVIES_FROM].sort_values("rating", ascending=False, kind="stable")
    best = [(titles[m], r) for m, r in zip(best["movieId"], best["rating"])]

    movie_tags = movie_top_tags(tags, ratings, movies)
    unrated = movie_tags[~movie_tags["movieId"].isin(mine["movieId"])]
    hits = unrated[unrated["tag"].isin(set(top["tag"]))]
    overlap = hits.groupby("movieId")["tag"].apply(sorted)
    counts = overlap.map(len).sort_values(ascending=False)
    leaders = counts[counts == counts.max()]
    judge_file = REPO / "judge" / "ratings_users.csv"
    judged = []
    if judge_file.exists():
        j = pd.read_csv(judge_file, keep_default_na=False)
        j = j[j["id"] == ME].sort_values(["rating", "tag"], ascending=[False, True])
        judged = list(zip(j["tag"], j["rating"]))
    return {
        "judge": judged,
        "tags": list(zip(top["tag"], top["score"])),
        "movies": best,
        "leaders": [(titles[m], overlap[m]) for m in leaders.index],
        "most": int(counts.max()),
    }


def render(page):
    def ol(items):
        return "<ol>%s</ol>" % "".join("<li>%s</li>" % html.escape(i) for i in items)
    body = ["<h1>What my score says about me</h1>",
            "<h2>My top %d tags</h2>" % TOP_TAGS, ol(f"{t} ({s})" for t, s in page["tags"]),
            "<hr>",
            "<h2>The judge's ratings of my tags (1 to 5, from judge/ratings_users.csv)</h2>",
            ol(f"{t} ({r})" for t, r in page["judge"]) if page["judge"] else "<p>(no judge ratings yet)</p>",
            "<hr>",
            "<h2>My top movies (rated %.1f or higher)</h2>" % TOP_MOVIES_FROM,
            ol(f"{t} ({r})" for t, r in page["movies"]),
            "<h2>Recommended for me</h2>"]
    for title, hit in page["leaders"]:
        body += ["<p><b>%s</b>: %d of my top %d tags among its top 20: %s</p>"
                 % (html.escape(title), page["most"], TOP_TAGS, html.escape(", ".join(hit)))]
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            "<title>User Viewer</title>\n</head>\n<body>\n" + "\n".join(body) + "\n</body>\n</html>\n")


def render_text(page):
    out = [f"My top {TOP_TAGS} tags"] + [f"  {i:>2}. {t} ({s})" for i, (t, s) in enumerate(page["tags"], 1)]
    out += ["", "-" * 40, "The judge's ratings of my tags (1 to 5, from judge/ratings_users.csv)"]
    out += [f"  {i:>2}. {t} ({r})" for i, (t, r) in enumerate(page["judge"], 1)] or ["  (no judge ratings yet)"]
    out += ["-" * 40, "", f"My top movies (rated {TOP_MOVIES_FROM} or higher)"]
    out += [f"  {i:>2}. {t} ({r})" for i, (t, r) in enumerate(page["movies"], 1)]
    out += ["", "Recommended for me"]
    out += [f"  {t}: {page['most']} of my top {TOP_TAGS} tags among its top 20: {', '.join(h)}"
            for t, h in page["leaders"]]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="What my score(user, tag) says about me.")
    parser.add_argument("--text", action="store_true")
    parser.add_argument("--out", default=str(REPO / "user_results.html"))
    args = parser.parse_args()
    page = build()
    if args.text:
        print(render_text(page))
    else:
        Path(args.out).write_text(render(page), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
