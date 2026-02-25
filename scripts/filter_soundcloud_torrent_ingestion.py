import os
import json
import zstandard as zstd
from datetime import datetime

# -------------------------------------------------------
# TARGET SUBREDDITS
# We filter the entire Reddit dump down to just these
# communities. Keeping all columns so we can explore
# the data freely before deciding what to drop later.
# "Filter early, transform late" — core data engineering principle.
# -------------------------------------------------------
TARGET_SUBREDDITS = {
    "musichoarder",
    "musicmarketing",
    "soundcloud",
    "soundcloudhiphop",
    "ug_music",
    "musicproduction",
    "genz",
    "wearethemusicmakers",
    "makinghiphop",
    "edmproduction",
    "music"
}

# -------------------------------------------------------
# PATHS
# os.path.abspath(__file__) = full path to this script file
# os.path.dirname() twice = go up two levels to project root
# This means the script works no matter what folder you run it from
# -------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")

CHUNK_SIZE = 2**24  # Read 16MB at a time — avoids loading 35GB into memory

def read_zst_file(filepath):
    """
    Stream a .zst compressed file line by line.
    
    WHY STREAMING:
    The file is ~35GB. Loading it all at once would crash your computer.
    Instead we read it in 16MB chunks, split into lines, and yield
    one line at a time. "yield" means: give the caller one item,
    pause, wait to be asked for the next one.
    
    The buffer trick handles lines that get cut across two chunks —
    we keep the incomplete line and prepend it to the next chunk.
    """
    with open(filepath, "rb") as f:
        dctx = zstd.ZstdDecompressor(max_window_size=2**31)
        stream_reader = dctx.stream_reader(f)
        buffer = ""
        while True:
            chunk = stream_reader.read(CHUNK_SIZE)
            if not chunk:
                break
            text = chunk.decode("utf-8", errors="ignore")
            buffer += text
            lines = buffer.split("\n")
            buffer = lines.pop()  # keep incomplete last line for next chunk
            for line in lines:
                if line.strip():
                    yield line

def filter_by_subreddit(input_file, output_file):
    """
    Filter the raw Reddit dump to only our target subreddits.
    Keeps ALL columns — no data thrown away yet.
    Saves as newline-delimited JSON (ndjson):
      - one complete JSON object per line
      - if script crashes halfway, all lines written so far are still valid
      - easier to read back line by line later
    """
    os.makedirs(CLEANED_DIR, exist_ok=True)
    out_path = os.path.join(CLEANED_DIR, output_file)

    total = 0      # every line we scan
    kept = 0       # lines we actually keep
    skipped = 0    # lines we skip (wrong subreddit or bad JSON)

    print(f"Starting filter...")
    print(f"Input:  {input_file}")
    print(f"Output: {out_path}")
    print(f"Target subreddits: {sorted(TARGET_SUBREDDITS)}\n")

    with open(out_path, "w", encoding="utf-8") as out:
        for line in read_zst_file(input_file):
            total += 1

            try:
                data = json.loads(line)

                # Check if this comment is from one of our target subreddits
                # .lower() so "SoundCloud" matches "soundcloud"
                subreddit = data.get("subreddit", "").lower()

                if subreddit not in TARGET_SUBREDDITS:
                    skipped += 1
                    continue

                # Write the FULL record as-is — no columns dropped
                # ensure_ascii=False preserves non-English characters
                out.write(json.dumps(data, ensure_ascii=False) + "\n")
                kept += 1

            except (json.JSONDecodeError, ValueError):
                # Some lines may be malformed — skip them silently
                skipped += 1
                continue

            # Progress update every 500k lines
            if total % 500000 == 0:
                print(f"  Scanned {total:,} | Kept {kept:,} | Skipped {skipped:,}")

    print(f"\nDone!")
    print(f"  Total scanned: {total:,}")
    print(f"  Kept:          {kept:,}")
    print(f"  Skipped:       {skipped:,}")
    print(f"  Output file:   {out_path}")

def main():
    """
    Find all .zst files in data/raw/ and filter each one.
    Named main() by convention — this is the entry point of the script.
    The if __name__ == "__main__" block at the bottom calls this
    only when you run the script directly (not when imported).
    """
    zst_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".zst")]

    if not zst_files:
        print(f"No .zst files found in {RAW_DIR}")
        print("Place your RC_2025-12.zst file in data/raw/ and try again.")
        return

    for zst_file in zst_files:
        input_path = os.path.join(RAW_DIR, zst_file)
        output_file = zst_file.replace(".zst", "_music_subreddits.ndjson")
        filter_by_subreddit(input_path, output_file)

if __name__ == "__main__":
    main()