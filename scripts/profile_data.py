import json
import os
from collections import Counter, defaultdict

# -------------------------------------------------------
# DATA PROFILING SCRIPT
# Gives a complete picture of what's in our dataset
# before we build anything on top of it.
# This is standard practice before any analysis.
# -------------------------------------------------------

INPUT_FILE = "data/cleaned/RC_2025-12_music_subreddits.ndjson"
OUTPUT_FILE = "data/cleaned/data_profile_report.txt"

def profile_data(filepath):
    
    # Counters we'll track
    total_rows = 0
    rows_by_subreddit = Counter()
    moderator_posts = Counter()
    distinguished_posts = Counter()
    null_counts = defaultdict(int)
    deleted_authors = Counter()
    removed_bodies = Counter()
    score_by_subreddit = defaultdict(list)
    controversiality_by_subreddit = Counter()
    author_counts = Counter()
    subreddit_types = Counter()
    archived_count = Counter()
    locked_count = Counter()
    edited_count = Counter()
    
    # Fields we want to profile for nulls
    key_fields = [
        "id", "author", "body", "score", "subreddit",
        "created_utc", "permalink", "distinguished",
        "removal_reason", "mod_note", "banned_at_utc"
    ]

    print(f"Profiling {filepath}...")
    print("This may take a minute...\n")

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                total_rows += 1
                subreddit = data.get("subreddit", "unknown")
                
                # Row counts per subreddit
                rows_by_subreddit[subreddit] += 1
                
                # Moderator detection
                distinguished = data.get("distinguished")
                if distinguished in ("moderator", "admin"):
                    moderator_posts[subreddit] += 1
                    distinguished_posts[distinguished] += 1
                
                # Deleted/removed content
                author = data.get("author", "")
                if author in ("[deleted]", "AutoModerator", None):
                    deleted_authors[subreddit] += 1
                
                body = data.get("body", "")
                if body in ("[removed]", "[deleted]", None, ""):
                    removed_bodies[subreddit] += 1
                
                # Null counts for key fields
                for field in key_fields:
                    val = data.get(field)
                    if val is None or val == "" or val == []:
                        null_counts[field] += 1
                
                # Score tracking
                score = data.get("score", 0)
                if isinstance(score, (int, float)):
                    score_by_subreddit[subreddit].append(score)
                
                # Controversiality
                if data.get("controversiality", 0) == 1:
                    controversiality_by_subreddit[subreddit] += 1
                
                # Author frequency
                if author and author not in ("[deleted]", "AutoModerator"):
                    author_counts[author] += 1
                
                # Subreddit type
                subreddit_types[data.get("subreddit_type", "unknown")] += 1
                
                # Archived, locked, edited
                if data.get("archived"):
                    archived_count[subreddit] += 1
                if data.get("locked"):
                    locked_count[subreddit] += 1
                if data.get("edited") and data.get("edited") != False:
                    edited_count[subreddit] += 1

            except (json.JSONDecodeError, ValueError):
                continue

    # -------------------------------------------------------
    # BUILD REPORT
    # -------------------------------------------------------
    lines = []
    lines.append("=" * 70)
    lines.append("DATA PROFILE REPORT")
    lines.append(f"File: {filepath}")
    lines.append("=" * 70)
    
    lines.append(f"\nTOTAL ROWS: {total_rows:,}")
    
    lines.append("\n" + "-" * 70)
    lines.append("ROW COUNTS BY SUBREDDIT")
    lines.append("-" * 70)
    for sub, count in rows_by_subreddit.most_common():
        pct = count / total_rows * 100
        lines.append(f"  r/{sub:<30} {count:>8,} rows  ({pct:.1f}%)")
    
    lines.append("\n" + "-" * 70)
    lines.append("MODERATOR & ADMIN POSTS BY SUBREDDIT")
    lines.append("-" * 70)
    if moderator_posts:
        for sub, count in moderator_posts.most_common():
            pct = count / rows_by_subreddit[sub] * 100
            lines.append(f"  r/{sub:<30} {count:>6,} mod posts ({pct:.1f}% of subreddit)")
    else:
        lines.append("  No moderator posts found")
    
    lines.append(f"\n  Distinguished breakdown: {dict(distinguished_posts)}")

    lines.append("\n" + "-" * 70)
    lines.append("DELETED / REMOVED CONTENT BY SUBREDDIT")
    lines.append("-" * 70)
    for sub, count in deleted_authors.most_common():
        pct = count / rows_by_subreddit[sub] * 100
        lines.append(f"  r/{sub:<30} {count:>6,} deleted/bot authors ({pct:.1f}%)")

    lines.append("\n" + "-" * 70)
    lines.append("REMOVED BODY TEXT BY SUBREDDIT")
    lines.append("-" * 70)
    for sub, count in removed_bodies.most_common():
        pct = count / rows_by_subreddit[sub] * 100
        lines.append(f"  r/{sub:<30} {count:>6,} removed bodies ({pct:.1f}%)")

    lines.append("\n" + "-" * 70)
    lines.append("NULL / EMPTY COUNTS FOR KEY FIELDS (across all subreddits)")
    lines.append("-" * 70)
    for field, count in sorted(null_counts.items(), key=lambda x: -x[1]):
        pct = count / total_rows * 100
        lines.append(f"  {field:<30} {count:>8,} nulls ({pct:.1f}%)")

    lines.append("\n" + "-" * 70)
    lines.append("SCORE STATISTICS BY SUBREDDIT")
    lines.append("-" * 70)
    for sub, scores in sorted(score_by_subreddit.items()):
        if scores:
            avg = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)
            lines.append(f"  r/{sub:<30} avg={avg:.1f}  max={max_score:,}  min={min_score:,}")

    lines.append("\n" + "-" * 70)
    lines.append("CONTROVERSIAL POSTS BY SUBREDDIT")
    lines.append("-" * 70)
    for sub, count in controversiality_by_subreddit.most_common():
        pct = count / rows_by_subreddit[sub] * 100
        lines.append(f"  r/{sub:<30} {count:>6,} controversial ({pct:.1f}%)")

    lines.append("\n" + "-" * 70)
    lines.append("TOP 10 MOST ACTIVE AUTHORS (excluding deleted/bots)")
    lines.append("-" * 70)
    for author, count in author_counts.most_common(10):
        lines.append(f"  {author:<35} {count:>6,} comments")

    lines.append("\n" + "-" * 70)
    lines.append("EDITED POSTS BY SUBREDDIT")
    lines.append("-" * 70)
    for sub, count in edited_count.most_common():
        pct = count / rows_by_subreddit[sub] * 100
        lines.append(f"  r/{sub:<30} {count:>6,} edited ({pct:.1f}%)")

    lines.append("\n" + "-" * 70)
    lines.append("SUBREDDIT TYPES")
    lines.append("-" * 70)
    for stype, count in subreddit_types.most_common():
        lines.append(f"  {stype:<20} {count:>8,}")

    lines.append("\n" + "=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)

    return "\n".join(lines)

def main():
    report = profile_data(INPUT_FILE)
    
    # Print to terminal
    print(report)
    
    # Save to file
    os.makedirs("data/cleaned", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\nReport saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()