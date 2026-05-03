#!/usr/bin/env python3
"""
Fetch Eva's Google Business Profile reviews via DataForSEO.

Two modes:
  1. Default — calls DataForSEO API and saves to data/google-reviews.json
  2. --render-only — skips API, just regenerates HTML from the cached JSON

Used by the GitHub Action that runs weekly to keep reviews fresh.

Env vars (read from GitHub Secrets in CI):
  DATAFORSEO_LOGIN
  DATAFORSEO_PASSWORD

Usage:
  python3 scripts/fetch-reviews.py            # fetch from API + render
  python3 scripts/fetch-reviews.py --render-only  # render from cache only
"""
import json
import os
import sys
import time
import base64
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACE_ID = "ChIJ62ZK3qwBdkgRpFwQSULhNuQ"  # And Chillax Anerley
DATA_FILE = ROOT / "data" / "google-reviews.json"


def fetch_reviews_from_api():
    """Call DataForSEO to refresh reviews data."""
    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        print("ERROR: DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD env vars required.",
              file=sys.stderr)
        sys.exit(1)

    auth = base64.b64encode(f"{login}:{password}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
    }

    body = json.dumps([{
        "place_id": PLACE_ID,
        "location_code": 2826,  # United Kingdom
        "language_code": "en",
        "depth": 50,
        "sort_by": "newest",
    }]).encode()

    # Step 1: post task
    req = urllib.request.Request(
        "https://api.dataforseo.com/v3/business_data/google/reviews/task_post",
        data=body, headers=headers, method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        post = json.loads(r.read().decode())

    if post["status_code"] != 20000 or post["tasks"][0]["status_code"] not in (20000, 20100):
        print(f"task_post failed: {post['tasks'][0]['status_message']}", file=sys.stderr)
        sys.exit(1)

    task_id = post["tasks"][0]["id"]
    print(f"  task posted: {task_id}")

    # Step 2: poll until ready (max ~3 min)
    for attempt in range(18):
        time.sleep(10)
        req = urllib.request.Request(
            f"https://api.dataforseo.com/v3/business_data/google/reviews/task_get/{task_id}",
            headers=headers,
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                got = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            print(f"  poll attempt {attempt+1}: {e}")
            continue

        task = got["tasks"][0]
        msg = task["status_message"]
        print(f"  poll {attempt+1}: {msg}")
        if msg == "Ok." and task.get("result"):
            items = task["result"][0].get("items") or []
            print(f"  retrieved {len(items)} reviews")
            return items
        if "Task Handed" in msg or "In Queue" in msg:
            continue
        if msg == "Task Not Found.":
            continue

    print("ERROR: review task did not complete in time", file=sys.stderr)
    sys.exit(1)


def html_escape(s):
    """Minimal HTML escape for review text + names."""
    if s is None:
        return ""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def render_review_card(r, indent="      "):
    """Render one review as a .review-card HTML block."""
    rating = int(r.get("rating", {}).get("value") or 5)
    stars = "★" * rating
    name = html_escape(r.get("profile_name") or "Verified customer")
    text = html_escape((r.get("review_text") or "").strip().replace("\n\n", " ").replace("\n", " "))
    timestamp = (r.get("timestamp") or "")[:10]  # YYYY-MM-DD only
    return (
        f'{indent}<div class="review-card">\n'
        f'{indent}  <div class="review-card__stars">{stars}</div>\n'
        f'{indent}  <p class="review-card__quote">"{text}"</p>\n'
        f'{indent}  <p class="review-card__attrib"><strong>{name}</strong>Google review · {timestamp}</p>\n'
        f'{indent}</div>'
    )


def render_reviews_section(reviews):
    """Render the main reviews grid (all 13 cards)."""
    cards = "\n\n".join(render_review_card(r) for r in reviews)
    return cards


def update_reviews_html(reviews):
    """Replace the static review cards on reviews.html with the live ones."""
    path = ROOT / "reviews.html"
    html = path.read_text()

    # Find the reviews-grid div and replace its content
    import re
    pattern = r'(<div class="reviews-grid">)([\s\S]*?)(\n    </div>\n\n    <p style="text-align: center)'
    new_inner = "\n\n" + render_reviews_section(reviews) + "\n\n    "
    replacement = r"\1" + new_inner + r"\3"
    new_html, n = re.subn(pattern, replacement, html)

    if n == 0:
        print("WARNING: could not find reviews-grid pattern in reviews.html", file=sys.stderr)
        return False

    # Update the count text to match actual review count
    new_html = re.sub(
        r'5\.0 from \d+ verified Google reviews\.',
        f'5.0 from {len(reviews)} verified Google reviews.',
        new_html,
    )
    new_html = re.sub(
        r'See all \d+ on Google',
        f'See all {len(reviews)} on Google',
        new_html,
    )

    path.write_text(new_html)
    print(f"  ✓ reviews.html updated with {len(reviews)} reviews")
    return True


def update_homepage_testimonials(reviews):
    """Pick 3 short, punchy reviews for the homepage 'About / reviews' section.
    The homepage doesn't currently have a testimonials grid, so we don't update it here.
    Could add later if a testimonials section is created."""
    # Currently homepage shows the 5★/13 review badge in hero.
    # Update count to match actual.
    path = ROOT / "index.html"
    html = path.read_text()
    import re
    new_html = re.sub(r'from \d+ Google reviews', f'from {len(reviews)} Google reviews', html)
    if new_html != html:
        path.write_text(new_html)
        print(f"  ✓ index.html review count updated")


def update_schema_markup(reviews):
    """Update the LocalBusiness schema on every page with the real review count."""
    import re
    count = len(reviews)
    pattern = r'("aggregateRating":\s*\{[^}]*"reviewCount":\s*")\d+(")'
    replacement = rf'\g<1>{count}\g<2>'

    updated = 0
    for path in ROOT.rglob("*.html"):
        if ".git" in str(path):
            continue
        html = path.read_text()
        new_html = re.sub(pattern, replacement, html)
        if new_html != html:
            path.write_text(new_html)
            updated += 1
    if updated:
        print(f"  ✓ schema markup reviewCount updated on {updated} pages")


def update_course_page_testimonials(reviews):
    """Update the testimonial blocks on course pages with the most relevant reviews."""
    # 12-hr Paediatric page — pick paediatric/childminder reviews
    paeds_keywords = ["paediatric", "pediatric", "childminder", "nursery", "nanny", "ofsted"]
    paeds_reviews = [
        r for r in reviews
        if any(k in (r.get("review_text") or "").lower() for k in paeds_keywords)
    ][:3]

    if len(paeds_reviews) >= 3:
        path = ROOT / "courses" / "12-hour-paediatric-first-aid.html"
        if path.exists():
            html = path.read_text()
            import re
            # Match the existing testimonial section's reviews-grid
            pattern = r'(<header class="section-header">\s*<p class="section-header__eyebrow">★ ★ ★ ★ ★[\s\S]*?</header>)\s*\n\s*(<div class="reviews-grid">)([\s\S]*?)(\n    </div>)'
            new_cards = "\n\n" + "\n\n".join(render_review_card(r) for r in paeds_reviews) + "\n    "
            replacement = r"\1\n\n    \2" + new_cards + r"\4"
            new_html, n = re.subn(pattern, replacement, html)
            if n:
                path.write_text(new_html)
                print(f"  ✓ 12-hr Paediatric page updated with 3 real reviews")


def main():
    render_only = "--render-only" in sys.argv

    if render_only:
        print(f"render-only mode → loading from {DATA_FILE}")
        if not DATA_FILE.exists():
            print(f"ERROR: {DATA_FILE} not found", file=sys.stderr)
            sys.exit(1)
        reviews = json.load(DATA_FILE.open())
    else:
        print("Fetching latest reviews from DataForSEO...")
        reviews = fetch_reviews_from_api()
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        json.dump(reviews, DATA_FILE.open("w"), indent=2)
        print(f"  saved to {DATA_FILE}")

    print()
    print("Rendering HTML...")
    update_reviews_html(reviews)
    update_homepage_testimonials(reviews)
    update_schema_markup(reviews)
    update_course_page_testimonials(reviews)
    print()
    print(f"Done. {len(reviews)} reviews live across the site.")


if __name__ == "__main__":
    main()
