import json
import os
import zstandard as zstd
from datetime import datetime

# Subreddits we care about for music platform experience
TARGET_SUBREDDITS = {
    "WeAreTheMusicMakers",
    "makinghiphop", 
    "edmproduction",
    "Music",
    "soundcloud"
}

# Keywords to filter relevant posts
KEYWORDS = [
    "soundcloud",
    "streaming",
    "platform",
    "payout",
    "upload",
    "distribution",
    "spotify",
    "artist",
    "listener",
    "royalt",
    "monetiz"
]

def is_relevant(text):
    """Check if a comment contains any of our keywords."""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)

def read_zst_file(filepath):
    """Read a Pushshift .zst compressed file line by line."""
    with open(filepath, "rb") as f:
        dctx = zstd.ZstdDecompressor(max_window_size=2**31)
        with dctx.stream_reader(f) as reader:
            buffer = ""
            while True:
                chunk = reader.read(65536).decode("utf-8", errors="ignore")
                if not chunk:
                    break
                buffer += chunk
                lines = buffer.split("\n")
                buffer = lines[-1]  # Keep incomplete line in buffer
                for line in lines[:-1]:
                    if line.strip():
                        yield line

def process_file(filepath):
    """
    Process a Pushshift .zst file and extract relevant comments.
    
    Pushshift files are organized by month and contain ALL subreddits.
    We filter down to just our target subreddits and relevant keywords.
    """
    print(f"Processing {filepath}...")
    results = []
    total = 0
    kept = 0

    for line in read_zst_file(filepath):
        try:
            data = json.loads(line)
            total += 1

            # Filter by subreddit
            subreddit = data.get("subreddit", "")
            if subreddit not in TARGET_SUBREDDITS:
                continue

            # Get the text content
            body = data.get("body", data.get("selftext", ""))
            title = data.get("title", "")
            full_text = f"{title} {body}".strip()

            # Filter by keyword relevance
            if not is_relevant(full_text):
                continue

            # Build clean record
            record = {
                "id": data.get("id", ""),
                "subreddit": subreddit,
                "author": data.get("author", ""),
                "title": title,
                "body": body,
                "score": data.get("score", 0),
                "created_utc": datetime.utcfromtimestamp(
                    data.get("created_utc", 0)
                ).isoformat(),
                "type": "comment" if "body" in data else "post"
            }

            results.append(record)
            kept += 1

            # Progress update every 100k records
            if total % 100000 == 0:
                print(f"  Scanned {total:,} records, kept {kept:,}...")

        except (json.JSONDecodeError, ValueError):
            continue

    print(f"  Done. Kept {kept:,} relevant records from {total:,} total.")
    return results

def save_results(data, output_filename):
    """Save filtered results to data/cleaned/ folder."""
    os.makedirs("data/cleaned", exist_ok=True)
    filepath = f"data/cleaned/{output_filename}"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(data):,} records to {filepath}")

def main():
    """
    Main entry point.
    
    Place your downloaded Pushshift .zst files in data/raw/
    then run this script to filter and clean them.
    
    Download files from:
    https://huggingface.co/datasets/fddemarco/pushshift-reddit-comments
    """
    raw_dir = "data/raw"
    
    # Check if any files exist
    if not os.path.exists(raw_dir):
        print("ERROR: data/raw/ folder not found.")
        return

    zst_files = [f for f in os.listdir(raw_dir) if f.endswith(".zst")]

    if not zst_files:
        print("No .zst files found in data/raw/")
        print("Download Pushshift files from:")
        print("https://huggingface.co/datasets/fddemarco/pushshift-reddit-comments")
        return

    all_results = []

    for filename in zst_files:
        filepath = os.path.join(raw_dir, filename)
        results = process_file(filepath)
        
        # Save each file's results separately
        output_name = filename.replace(".zst", "_filtered.json")
        save_results(results, output_name)
        all_results.extend(results)

    # Save combined output
    if all_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_results(all_results, f"all_filtered_{timestamp}.json")
        print(f"\nDone! Total records collected: {len(all_results):,}")

if __name__ == "__main__":
    main()